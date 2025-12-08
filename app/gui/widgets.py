# app/gui/widgets.py
from PyQt5.QtWidgets import (QTreeWidget, QTreeWidgetItem, QTextEdit, QWidget, 
                             QVBoxLayout, QLabel, QListWidget, QListWidgetItem, 
                             QHBoxLayout, QPushButton, QMessageBox)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
from app.gui.syntax import highlight_code

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import matplotlib.pyplot as plt

class FileTreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderLabels(["Файл", "Рядки", "Розмір (KB)"])
        self.setColumnWidth(0, 280)
        self.setAlternatingRowColors(True)

    def populate(self, data):
        self.clear()
        for lang_name, files in data.items():
            lang_item = QTreeWidgetItem(self)
            lang_item.setText(0, f"{lang_name} ({len(files)})")
            lang_item.setFont(0, QFont("Segoe UI", 10, QFont.Bold))
            for f in files:
                item = QTreeWidgetItem(lang_item)
                item.setText(0, f[0]); item.setText(1, str(f[1])); item.setText(2, f"{f[2]/1024:.1f}")
                item.setData(0, Qt.UserRole, f[3])
            self.expandItem(lang_item)

class CodeEditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_path = None
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Тулбар редактора
        tool_layout = QHBoxLayout()
        self.label = QLabel("Редактор коду")
        self.label.setStyleSheet("font-weight: bold; color: #444;")
        tool_layout.addWidget(self.label)
        
        # Кнопка збереження (Пункт 6)
        self.save_btn = QPushButton("💾 Зберегти зміни")
        self.save_btn.clicked.connect(self.save_file)
        self.save_btn.setEnabled(False)
        tool_layout.addWidget(self.save_btn)
        
        layout.addLayout(tool_layout)
        
        self.editor = QTextEdit()
        self.editor.setFont(QFont("Consolas", 11))
        # Дозволяємо редагування!
        self.editor.setReadOnly(False) 
        layout.addWidget(self.editor)

    def load_file(self, path):
        self.current_path = path
        self.label.setText(f"📝 {path}")
        self.save_btn.setEnabled(True)
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read() # Читаємо все для редагування
                # Тут можна було б використати highlight_code, але для редактора 
                # краще чистий текст, бо HTML в QTextEdit важко редагувати коректно без складного парсера.
                # Тому ми завантажуємо як текст.
                self.editor.setPlainText(content)
        except Exception as e:
            self.editor.setPlainText(f"Помилка: {e}")

    def save_file(self):
        if not self.current_path: return
        try:
            content = self.editor.toPlainText()
            with open(self.current_path, 'w', encoding='utf-8') as f:
                f.write(content)
            QMessageBox.information(self, "Збережено", "Файл успішно оновлено!")
        except Exception as e:
            QMessageBox.critical(self, "Помилка", str(e))

# ... (SearchResultsWidget і StatsWidget залишаються такими ж, як були в попередньому кроці)
class SearchResultsWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlternatingRowColors(True)
    def add_result(self, title, subtitle, data):
        item = QListWidgetItem()
        item.setText(f"{title}\n   ↳ {subtitle}")
        item.setFont(QFont("Segoe UI", 10))
        item.setData(Qt.UserRole, data) 
        self.addItem(item)

class StatsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def show_charts(self, lang_dist, top_files):
        self.figure.clear()
        ax1 = self.figure.add_subplot(121)
        if lang_dist:
            labels = [x[0] for x in lang_dist]
            sizes = [x[1] for x in lang_dist]
            ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax1.set_title("Distribution")
        
        ax2 = self.figure.add_subplot(122)
        if top_files:
            names = [x[0][:10] for x in top_files[:8]]
            lines = [x[1] for x in top_files[:8]]
            y_pos = range(len(names))
            ax2.barh(y_pos, lines, align='center', color='#3498db')
            ax2.set_yticks(y_pos); ax2.set_yticklabels(names); ax2.invert_yaxis()
            ax2.set_title("Top Files (LOC)")
        self.figure.tight_layout()
        self.canvas.draw()

class StatsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        
        # ВМИКАЄМО ТЕМНУ ТЕМУ ДЛЯ ГРАФІКІВ
        plt.style.use('dark_background')
        
        self.figure = Figure(figsize=(5, 4), dpi=100)
        # Колір фону самого віджета графіку (#1e1e1e - темно-сірий)
        self.figure.patch.set_facecolor('#1e1e1e')
        
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def show_charts(self, lang_dist, top_files):
        self.figure.clear()
        
        # Графік 1: Пиріг
        ax1 = self.figure.add_subplot(121)
        if lang_dist:
            labels = [x[0] for x in lang_dist]
            sizes = [x[1] for x in lang_dist]
            # Кольорова палітра "Pastel" виглядає краще на темному
            colors = plt.cm.Set3(range(len(labels)))
            
            wedges, texts, autotexts = ax1.pie(sizes, labels=labels, autopct='%1.1f%%', 
                                               startangle=90, colors=colors)
            ax1.set_title("Distribution by Language", color='white', fontsize=12)
            # Колір тексту відсотків
            for text in texts + autotexts:
                text.set_color('white')
        
        # Графік 2: Стовпчики
        ax2 = self.figure.add_subplot(122)
        if top_files:
            names = [x[0][:15] for x in top_files[:10]] # Тільки топ-10
            lines = [x[1] for x in top_files[:10]]
            
            y_pos = range(len(names))
            bars = ax2.barh(y_pos, lines, align='center', color='#3498db')
            ax2.set_yticks(y_pos)
            ax2.set_yticklabels(names, color='white')
            ax2.invert_yaxis()
            ax2.set_xlabel('Lines of Code (LOC)', color='white')
            ax2.set_title("Top Largest Files", color='white', fontsize=12)
            
            # Прибираємо рамки
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            ax2.spines['bottom'].set_color('#555')
            ax2.spines['left'].set_color('#555')
            ax2.tick_params(colors='white')

        self.figure.tight_layout()
        self.canvas.draw()