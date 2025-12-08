# app/gui/main_window.py
import os
import json
import csv
from PyQt5.QtWidgets import (QMainWindow, QSplitter, QMessageBox, QAction, 
                             QToolBar, QTabWidget, QWidget, QVBoxLayout, 
                             QLineEdit, QPushButton, QHBoxLayout, QFileDialog, 
                             QProgressBar, QComboBox, QLabel)
from PyQt5.QtCore import Qt
from app.gui.widgets import FileTreeWidget, CodeEditorWidget, SearchResultsWidget, StatsWidget
from app.gui.tabs import LanguageCardWidget, ComparisonWidget, SQLConsoleWidget
from app.gui.workers import ScanWorker
from app.gui.styles import DARK_THEME, LIGHT_THEME
from app.database.store_sqlite import SQLiteStore
from app.core.search import SearchEngine
from app.analysis.stats import Analytics

SETTINGS_FILE = "settings.json"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Code Analyzer Pro 2025")
        self.resize(1300, 900)
        self.is_dark = True
        self.setStyleSheet(DARK_THEME)

        self.db = SQLiteStore()
        self.search_engine = SearchEngine()
        self.analytics = Analytics()
        
        self.init_ui()
        self.repo_path = self.load_settings()
        if self.repo_path: self.refresh_data()

    def init_ui(self):
        self.splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(self.splitter)
        
        # --- ЛІВА ПАНЕЛЬ ---
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # Фільтр
        filter_box = QHBoxLayout()
        filter_box.addWidget(QLabel("Фільтр:"))
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Всі файли", "Тільки код"])
        filter_box.addWidget(self.filter_combo)
        left_layout.addLayout(filter_box)
        
        # Дерево
        self.tree = FileTreeWidget()
        self.tree.itemClicked.connect(self.on_file_click)
        left_layout.addWidget(self.tree)
        
        # Прогрес
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        left_layout.addWidget(self.progress_bar)
        
        self.splitter.addWidget(left_widget)
        
        # --- ПРАВА ПАНЕЛЬ ---
        self.tabs = QTabWidget()
        self.splitter.addWidget(self.tabs)
        
        self.preview = CodeEditorWidget()
        self.tabs.addTab(self.preview, "📝 Редактор")
        self.search_tab = QWidget(); self.setup_search_tab()
        self.tabs.addTab(self.search_tab, "🔍 Пошук")
        self.lang_card = LanguageCardWidget()
        self.tabs.addTab(self.lang_card, "📇 Профіль")
        self.comparison = ComparisonWidget()
        self.tabs.addTab(self.comparison, "⚖️ Порівняння")
        self.sql_console = SQLConsoleWidget()
        self.tabs.addTab(self.sql_console, "💻 SQL")
        self.stats_tab = StatsWidget()
        self.tabs.addTab(self.stats_tab, "📊 Статистика")
        
        self.splitter.setSizes([300, 1000])
        self.create_toolbar()

    def create_toolbar(self):
        toolbar = QToolBar("Main"); toolbar.setMovable(False)
        self.addToolBar(toolbar)
        toolbar.addAction(QAction("📂 Відкрити папку", self, triggered=self.open_folder))
        toolbar.addAction(QAction("🚀 Сканувати", self, triggered=self.run_scan))
        toolbar.addSeparator()
        toolbar.addAction(QAction("📊 Експорт CSV", self, triggered=self.export_csv))
        empty = QWidget(); empty.setSizePolicy(1|4, 1|4); toolbar.addWidget(empty)
        self.theme_btn = QAction("☀ Світла тема", self, triggered=self.toggle_theme)
        toolbar.addAction(self.theme_btn)

    def toggle_theme(self):
        if self.is_dark:
            self.setStyleSheet(LIGHT_THEME); self.theme_btn.setText("🌙 Темна тема"); self.is_dark = False
        else:
            self.setStyleSheet(DARK_THEME); self.theme_btn.setText("☀ Світла тема"); self.is_dark = True

    def run_scan(self):
        if not self.repo_path or not os.path.exists(self.repo_path): return
        self.worker = ScanWorker(self.repo_path)
        self.worker.status_signal.connect(lambda m: self.statusBar().showMessage(m))
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.finished_signal.connect(self.on_scan_finished)
        self.progress_bar.setVisible(True); self.progress_bar.setRange(0, 0); self.worker.start()

    def update_progress(self, count):
        self.statusBar().showMessage(f"Оброблено файлів: {count}")

    def on_scan_finished(self, data):
        self.progress_bar.setVisible(False)
        self.tree.populate(data)
        self.refresh_tabs()
        QMessageBox.information(self, "Готово", "Сканування завершено!")

    def open_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Оберіть папку")
        if path:
            self.repo_path = path; self.save_settings(path); self.run_scan()

    def refresh_tabs(self):
        self.lang_card.refresh_list(); self.comparison.refresh_list()
        dist = self.analytics.get_language_distribution()
        top = self.analytics.get_top_large_files()
        self.stats_tab.show_charts(dist, top)

    def refresh_data(self):
        if hasattr(self.db, 'get_tree_data'):
            data = self.db.get_tree_data(); self.tree.populate(data); self.refresh_tabs()

    def on_file_click(self, item, column):
        path = item.data(0, Qt.UserRole)
        if path:
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f: code = f.read()
                self.preview.editor.setPlainText(code); self.preview.current_path = path
                self.preview.label.setText(f"📝 {path}"); self.preview.save_btn.setEnabled(True)
                self.tabs.setCurrentIndex(0)
            except Exception as e: self.preview.editor.setPlainText(str(e))

    def setup_search_tab(self):
        layout = QVBoxLayout(self.search_tab)
        h = QHBoxLayout()
        self.search_input = QLineEdit(); self.search_input.setPlaceholderText("Пошук...")
        self.search_input.returnPressed.connect(self.run_search)
        btn = QPushButton("Знайти"); btn.clicked.connect(self.run_search)
        h.addWidget(self.search_input); h.addWidget(btn); layout.addLayout(h)
        self.results_list = SearchResultsWidget(); self.results_list.itemClicked.connect(self.on_search_click)
        layout.addWidget(self.results_list)

    def run_search(self):
        q = self.search_input.text(); 
        if not q: return
        self.results_list.clear()
        files = self.search_engine.search_files(q)
        for name, path, size, lines in files: self.results_list.add_result(f"📄 {name}", path, path)
        res = self.search_engine.search_code(q)
        for m in res: self.results_list.add_result(f"📝 {m['file']} ({m['line']})", m['content'].strip(), m['path'])

    def on_search_click(self, item):
        path = item.data(Qt.UserRole)
        if path: self.on_file_click(item, 0)

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save", "report.csv", "CSV (*.csv)")
        if path:
            try:
                with open(path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Language", "Count"])
                    writer.writerows(self.analytics.get_language_distribution())
                QMessageBox.information(self, "OK", "Saved!")
            except Exception as e: QMessageBox.critical(self, "Error", str(e))

    def load_settings(self):
        try: return json.load(open(SETTINGS_FILE)).get('repo_path')
        except: return None
    def save_settings(self, path):
        with open(SETTINGS_FILE, 'w') as f: json.dump({'repo_path': path}, f)