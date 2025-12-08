# app/gui/tabs.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QComboBox, QTextBrowser, QPushButton, QGroupBox, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QTextEdit, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from app.database.store_sqlite import SQLiteStore
from app.utils.consts import LANGUAGE_META
import importlib
import sqlite3
# === БЕЗПЕЧНИЙ ІМПОРТ API ===
try:
    api_module = importlib.import_module("app.utils.api")
    WikiClient = getattr(api_module, "WikiClient")
    HAS_API = True
except (ImportError, AttributeError):
    HAS_API = False
    WikiClient = None
    HAS_API = False

# Воркер для Вікіпедії
class WikiWorker(QThread):
    finished = pyqtSignal(dict)
    def __init__(self, lang): super().__init__(); self.lang = lang
    def run(self):
        if HAS_API:
            client = WikiClient()
            self.finished.emit(client.get_info(self.lang) or {})
        else:
            self.finished.emit({})

class LanguageCardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.db = SQLiteStore()
        self.layout = QVBoxLayout(self)
        
        # Панель вибору
        top = QHBoxLayout()
        top.addWidget(QLabel("Мова:"))
        self.combo = QComboBox()
        self.combo.currentTextChanged.connect(self.load_info)
        top.addWidget(self.combo)
        self.layout.addLayout(top)
        
        self.info_box = QTextBrowser()
        self.info_box.setOpenExternalLinks(True)
        self.layout.addWidget(self.info_box)

    def refresh_list(self):
        self.combo.blockSignals(True)
        self.combo.clear()
        conn = sqlite3.connect(self.db.db_path)
        c = conn.cursor()
        c.execute("SELECT name FROM languages ORDER BY name")
        langs = [r[0] for r in c.fetchall()]
        conn.close()
        self.combo.addItems(langs)
        self.combo.blockSignals(False)

    def load_info(self, lang):
        if not lang: return
        conn = sqlite3.connect(self.db.db_path); c = conn.cursor()
        c.execute("SELECT l.file_count, SUM(f.lines) FROM languages l JOIN files f ON l.id=f.language_id WHERE l.name=?", (lang,))
        res = c.fetchone(); conn.close()
        count, lines = res if res else (0,0)
        
        # HTML Заглушка
        html = f"""<h1 style='color:#0078d4'>{lang}</h1>
        <p><b>Файлів:</b> {count} | <b>Рядків:</b> {lines}</p>
        <hr><p>⏳ Завантаження з Вікіпедії...</p>"""
        self.info_box.setHtml(html)
        
        # Запуск завантаження
        self.worker = WikiWorker(lang)
        self.worker.finished.connect(lambda d: self.update_ui(lang, count, lines, d))
        self.worker.start()

    def update_ui(self, lang, c, l, data):
        meta = LANGUAGE_META.get(lang, {})
        summary = data.get("summary", "Немає даних.")
        img = data.get("image", "")
        img_tag = f'<img src="{img}" width="150" align="right">' if img else ""
        
        html = f"""
        <h1 style='color:#0078d4'>{lang}</h1>
        {img_tag}
        <div style='background:#333; color:#fff; padding:10px; border-radius:6px;'>
            <b>📊 Статистика:</b> {c} файлів, {l} рядків
        </div>
        <h3>Інформація:</h3>
        <p>{summary}</p>
        <p><b>Автор:</b> {meta.get('author','?')}<br><b>Рік:</b> {meta.get('year','?')}</p>
        """
        self.info_box.setHtml(html)

class ComparisonWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        h = QHBoxLayout()
        self.c1 = QComboBox(); self.c2 = QComboBox()
        btn = QPushButton("Порівняти")
        btn.clicked.connect(self.compare)
        h.addWidget(QLabel("А:")); h.addWidget(self.c1)
        h.addWidget(QLabel("Б:")); h.addWidget(self.c2); h.addWidget(btn)
        layout.addLayout(h)
        self.table = QTableWidget(); self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Критерій", "Мова А", "Мова Б"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

    def refresh_list(self):
        self.c1.clear(); self.c2.clear()
        langs = sorted(list(LANGUAGE_META.keys()))
        self.c1.addItems(langs); self.c2.addItems(langs)

    def compare(self):
        l1 = self.c1.currentText(); l2 = self.c2.currentText()
        m1 = LANGUAGE_META.get(l1, {}); m2 = LANGUAGE_META.get(l2, {})
        rows = [("Рік", 'year'), ("Автор", 'author'), ("Тип", 'typing'), ("Парадигма", 'paradigm')]
        self.table.setRowCount(len(rows))
        for i, (name, key) in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(name))
            self.table.setItem(i, 1, QTableWidgetItem(str(m1.get(key, '-'))))
            self.table.setItem(i, 2, QTableWidgetItem(str(m2.get(key, '-'))))

class SQLConsoleWidget(QWidget):
    def __init__(self):
        super().__init__()
        l = QVBoxLayout(self)
        self.txt = QTextEdit(); self.txt.setPlaceholderText("SELECT * FROM files LIMIT 5"); self.txt.setMaximumHeight(80)
        l.addWidget(self.txt)
        btn = QPushButton("Run SQL"); btn.clicked.connect(self.run); l.addWidget(btn)
        self.table = QTableWidget(); l.addWidget(self.table)
    def run(self):
        try:
            conn = sqlite3.connect("code_base.db"); c = conn.cursor()
            c.execute(self.txt.toPlainText())
            cols = [d[0] for d in c.description]; data = c.fetchall()
            self.table.setColumnCount(len(cols)); self.table.setHorizontalHeaderLabels(cols); self.table.setRowCount(len(data))
            for i, row in enumerate(data):
                for j, val in enumerate(row): self.table.setItem(i, j, QTableWidgetItem(str(val)))
            conn.close()
        except Exception as e: QMessageBox.critical(self, "Error", str(e))