import os
import sys
import subprocess
from PyQt5.QtWidgets import (QTreeWidget, QTreeWidgetItem, QTextEdit, QWidget, 
                             QVBoxLayout, QLabel, QListWidget, QListWidgetItem, 
                             QHBoxLayout, QPushButton, QMessageBox, QRadioButton)
from PyQt5.QtGui import QFont, QColor, QTextCursor
from PyQt5.QtCore import Qt
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patheffects as path_effects 

# ДЕРЕВО ФАЙЛІВ
class FileTreeWidget(QTreeWidget):
    """Віджет для відображення ієрархічної структури файлів."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderLabels(["Файл", "Рядки", "Розмір (KB)"])
        self.setColumnWidth(0, 300)
        self.setAlternatingRowColors(True) 
    
    def populate(self, data):
        self.clear()
        for lang_name, files in data.items():
            lang_item = QTreeWidgetItem(self)
            lang_item.setText(0, f"{lang_name} ({len(files)})")
            lang_item.setFont(0, QFont("Segoe UI", 10, QFont.Bold))
            lang_item.setForeground(0, QColor("#0078d4")) 
            
            for f in files:
                item = QTreeWidgetItem(lang_item)
                item.setText(0, f[0]) # Name
                item.setText(1, str(f[1])) # Lines
                item.setText(2, f"{f[2]/1024:.1f}") # Size
                item.setData(0, Qt.UserRole, f[3]) # Path
            self.expandItem(lang_item)

# РЕДАКТОР КОДУ
class CodeEditorWidget(QWidget):
    """Віджет для перегляду коду з можливістю відкриття у зовнішньому редакторі."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_path = None
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        tool_layout = QHBoxLayout()
        self.label = QLabel("Редактор коду")
        self.label.setStyleSheet("color: #333; font-weight: bold; font-size: 14px;")
        tool_layout.addWidget(self.label)
        tool_layout.addStretch() 
        
        # КНОПКА: Відкрити зовні
        self.open_ext_btn = QPushButton("↗️ Відкрити у...")
        self.open_ext_btn.setToolTip("Вибрати програму для відкриття файлу")
        self.open_ext_btn.clicked.connect(self.open_external)
        self.open_ext_btn.setEnabled(False)
        self.open_ext_btn.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
        tool_layout.addWidget(self.open_ext_btn)
        
        # КНОПКА: Зберегти
        self.save_btn = QPushButton("💾 Зберегти")
        self.save_btn.setFixedWidth(120)
        self.save_btn.clicked.connect(self.save_file)
        self.save_btn.setEnabled(False)
        tool_layout.addWidget(self.save_btn)
        
        layout.addLayout(tool_layout)
        
        self.editor = QTextEdit()
        self.editor.setFont(QFont("Consolas", 11))
        self.editor.setStyleSheet("background-color: #ffffff; color: #333; border: 1px solid #ccc; border-radius: 4px;")
        self.editor.setReadOnly(False)
        layout.addWidget(self.editor)
        
    def load_file(self, path):
        self.current_path = path
        filename = os.path.basename(path)
        self.label.setText(f"📝 {filename}")
        self.save_btn.setEnabled(True)
        self.open_ext_btn.setEnabled(True)
        
    def save_file(self):
        if not self.current_path: return
        try:
            with open(self.current_path, 'w', encoding='utf-8') as f:
                f.write(self.editor.toPlainText())
            QMessageBox.information(self, "Збережено", "Файл успішно оновлено!")
        except Exception as e:
            QMessageBox.critical(self, "Помилка", str(e))

    def open_external(self):
        """Викликає системне вікно 'Відкрити за допомогою'."""
        if not self.current_path: return
        try:
            if sys.platform == 'win32':
                subprocess.Popen(['rundll32', 'shell32.dll,OpenAs_RunDLL', self.current_path])
            elif sys.platform == 'darwin':
                subprocess.call(('open', self.current_path))
            else:
                subprocess.call(('xdg-open', self.current_path))
        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося відкрити діалог:\n{str(e)}")

    def scroll_to_line(self, line_num):
        """Прокручує редактор до вказаного рядка і виділяє його."""
        if line_num <= 0: return
        
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.Start)
        # Рухаємось вниз на line_num - 1 рядків
        cursor.movePosition(QTextCursor.Down, QTextCursor.MoveAnchor, line_num - 1)
        cursor.select(QTextCursor.LineUnderCursor)
        
        self.editor.setTextCursor(cursor)
        self.editor.centerCursor()

# СПИСОК РЕЗУЛЬТАТІВ
class SearchResultsWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def add_result(self, title, subtitle, data):
        item = QListWidgetItem()
        item.setText(f"{title}\n   ↳ {subtitle}")
        item.setFont(QFont("Segoe UI", 10))
        item.setData(Qt.UserRole, data)
        self.addItem(item)

# СТАТИСТИКА
class StatsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.lang_data = [] 
        self.top_files_data = []

        # Налаштування Matplotlib
        plt.style.use('default') 
        plt.rcParams['font.family'] = 'Segoe UI'
        plt.rcParams['font.size'] = 9
        plt.rcParams['text.color'] = '#333'
        plt.rcParams['axes.labelcolor'] = '#333'
        plt.rcParams['xtick.color'] = '#666'
        plt.rcParams['ytick.color'] = '#666'
        
        self.figure = Figure(figsize=(8, 4), dpi=100)
        self.figure.patch.set_facecolor('#f9f9f9')
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas, stretch=2)
        
        # Контроли
        controls = QHBoxLayout()
        controls.addWidget(QLabel("Детальна статистика:"))
        self.radio_langs = QRadioButton("Мови"); self.radio_langs.setChecked(True)
        self.radio_langs.toggled.connect(self.update_details_text)
        self.radio_files = QRadioButton("Топ файлів"); self.radio_files.toggled.connect(self.update_details_text)
        controls.addWidget(self.radio_langs); controls.addWidget(self.radio_files); controls.addStretch()
        self.layout.addLayout(controls)
        
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setStyleSheet("background-color: white; color: #333; border: 1px solid #ccc; font-family: 'Consolas'; padding: 5px;")
        self.info_text.setMaximumHeight(200)
        self.layout.addWidget(self.info_text, stretch=1)

    def show_charts(self, lang_dist, top_files):
        self.lang_data = lang_dist
        self.top_files_data = top_files
        self.figure.clear()
        
        # 1. ПОНЧИК
        ax1 = self.figure.add_subplot(121)
        grouped_data = []
        other = 0
        sorted_dist = sorted(lang_dist, key=lambda x: x[1], reverse=True)
        for l, c in sorted_dist:
            if c < 100: other += c
            else: grouped_data.append((l,c))
        if other > 0: grouped_data.append(("Інше", other))
            
        if grouped_data:
            sizes = [x[1] for x in grouped_data]
            colors = ['#0078d4', '#ea4300', '#107c10', '#ffb900', '#b4009e', '#008272', '#a0aeb2']
            wedges, texts, autotexts = ax1.pie(sizes, labels=None, autopct='%1.1f%%', pctdistance=0.75, startangle=90, colors=colors, wedgeprops=dict(width=0.4, edgecolor='white'))
            
            for t in autotexts: 
                t.set_color('white')
                t.set_weight('bold')
                try: 
                    t.set_path_effects([path_effects.withStroke(linewidth=2, foreground='#333')])
                except: pass
            
            ax1.legend(wedges, [x[0] for x in grouped_data], title="Мови", loc="center left", bbox_to_anchor=(0.9, 0, 0.5, 1), frameon=False)
            ax1.set_title("Розподіл файлів", color='#333', fontweight='bold')

        # 2. СТОВПЧИКИ
        ax2 = self.figure.add_subplot(122)
        if top_files:
            data = top_files[:8]
            names = [x[0] for x in data]
            lines = [x[1] for x in data]
            y_pos = np.arange(len(names))
            
            cmap = plt.get_cmap('Blues')
            colors = cmap(np.linspace(0.4, 0.9, len(names)))
            
            ax2.barh(y_pos, lines, align='center', color=colors, height=0.6)
            ax2.set_xlim(0, max(lines)*1.35)
            
            for i, v in enumerate(lines):
                ax2.text(v + (max(lines)*0.02), i, f"{v:,}".replace(",", " "), color='black', va='center', fontweight='bold')
            
            ax2.set_yticks(y_pos)
            short_names = [(n[:18] + '..') if len(n)>18 else n for n in names]
            ax2.set_yticklabels(short_names, color='#333')
            ax2.invert_yaxis()
            ax2.set_title("Найбільші файли (LOC)", color='#333', fontweight='bold')
            ax2.spines['top'].set_visible(False); ax2.spines['right'].set_visible(False)
            ax2.spines['bottom'].set_visible(False); ax2.spines['left'].set_visible(False)
            ax2.set_xticks([])

        self.figure.tight_layout()
        self.canvas.draw()
        self.update_details_text()

    def update_details_text(self):
        html = "<table width='100%' border='0' cellspacing='5'>"
        if self.radio_langs.isChecked():
            html += "<tr><td><b>Мова</b></td><td><b>Файлів</b></td><td><b>%</b></td></tr>"
            total = sum([x[1] for x in self.lang_data])
            for l, c in sorted(self.lang_data, key=lambda x: x[1], reverse=True):
                color = "#0078d4" if c > 100 else "#666"
                html += f"<tr><td style='color:{color}'>{l}</td><td>{c}</td><td style='color:#777'>{(c/total*100):.1f}%</td></tr>"
        else:
            html += "<tr><td><b>Файл</b></td><td><b>Рядки</b></td><td><b>Шлях</b></td></tr>"
            for item in self.top_files_data[:50]:
                path = item[3] if len(item)>3 else "..."
                html += f"<tr><td style='color:#d83b01'>{item[0]}</td><td>{item[1]}</td><td style='color:#777; font-size:11px'>{path}</td></tr>"
        html += "</table>"
        self.info_text.setHtml(html)