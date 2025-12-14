import os
import json
from PyQt5.QtWidgets import (QMainWindow, QSplitter, QMessageBox, QAction, 
                             QToolBar, QTabWidget, QWidget, QVBoxLayout, 
                             QLineEdit, QPushButton, QHBoxLayout, QFileDialog, 
                             QProgressBar, QComboBox, QLabel)
from PyQt5.QtCore import Qt
from app.gui.widgets import FileTreeWidget, CodeEditorWidget, SearchResultsWidget, StatsWidget
from app.gui.tabs import SQLConsoleWidget
from app.gui.workers import ScanWorker
from app.gui.styles import APP_THEME
from app.gui.dialogs import ScanOptionsDialog
from app.database.store_sqlite import SQLiteStore
from app.core.search import SearchEngine
from app.analysis.stats import Analytics

SETTINGS_FILE = "settings.json"

class MainWindow(QMainWindow):
    """
    Головне вікно програми. Об'єднує всі віджети та керує логікою.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CodeAnalyzer") 
        self.resize(1300, 900)
        self.setStyleSheet(APP_THEME)

        # Ініціалізація бекенду
        self.db = SQLiteStore()
        self.search_engine = SearchEngine()
        self.analytics = Analytics()
        self.last_options = {}
        
        self.init_ui()
        
        # Завантаження останньої робочої папки
        self.repo_path = self.load_settings()
        if self.repo_path: 
            self.refresh_data()
            self.update_search_filters() 

    def init_ui(self):
        """Побудова інтерфейсу: спліттер, панелі, тулбар."""
        self.splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(self.splitter)
        
        # --- ЛІВА ПАНЕЛЬ (Дерево файлів) ---
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        header_label = QLabel("📂 Структура проекту:")
        header_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 5px; color: #333;")
        left_layout.addWidget(header_label)
        
        self.tree = FileTreeWidget()
        self.tree.itemClicked.connect(self.on_tree_click)
        left_layout.addWidget(self.tree)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        left_layout.addWidget(self.progress_bar)
        
        self.splitter.addWidget(left_widget)
        
        # --- ПРАВА ПАНЕЛЬ (Вкладки) ---
        self.tabs = QTabWidget()
        self.splitter.addWidget(self.tabs)
        
        self.preview = CodeEditorWidget()
        self.tabs.addTab(self.preview, "📝 Редактор")
        
        self.search_tab = QWidget()
        self.setup_search_tab()
        self.tabs.addTab(self.search_tab, "🔍 Пошук")
        
        self.sql_console = SQLConsoleWidget()
        self.tabs.addTab(self.sql_console, "💻 SQL")
        
        self.stats_tab = StatsWidget()
        self.tabs.addTab(self.stats_tab, "📊 Статистика")
        
        self.splitter.setSizes([350, 950])
        self.create_toolbar()

    def create_toolbar(self):
        toolbar = QToolBar("Main")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        toolbar.addAction(QAction("📂 Відкрити папку", self, triggered=self.open_folder))
        toolbar.addAction(QAction("🚀 Сканувати...", self, triggered=self.run_scan_dialog)) 

    def run_scan_dialog(self):
        if not self.repo_path:
            QMessageBox.warning(self, "Увага", "Спочатку оберіть папку!")
            return self.open_folder()
            
        dialog = ScanOptionsDialog(self)
        if dialog.exec_():
            options = dialog.get_options()
            self.last_options = options
            self.start_scan_process(options)

    def start_scan_process(self, options):
        self.worker = ScanWorker(self.repo_path, options)
        self.worker.status_signal.connect(lambda m: self.statusBar().showMessage(m))
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.finished_signal.connect(self.on_scan_finished)
        self.worker.error_signal.connect(lambda e: QMessageBox.critical(self, "Помилка", e))
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.worker.start()

    def update_progress(self, count):
        self.statusBar().showMessage(f"Оброблено файлів: {count}")

    def on_scan_finished(self, data):
        self.progress_bar.setVisible(False)
        self.tree.populate(data)
        self.refresh_tabs()
        self.update_search_filters()
        
        total = sum(len(files) for files in data.values())
        QMessageBox.information(self, "Успіх", f"Сканування завершено!\nЗнайдено: {total} файлів")

    def open_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Оберіть папку з кодом")
        if path:
            self.repo_path = path
            self.save_settings(path)
            self.run_scan_dialog() 

    def refresh_tabs(self):
        """Оновлює графіки статистики."""
        dist = self.analytics.get_language_distribution()
        top = self.analytics.get_top_large_files()
        self.stats_tab.show_charts(dist, top)

    def refresh_data(self):
        """Оновлює дерево файлів з БД при запуску."""
        if hasattr(self.db, 'get_tree_data'):
            limit = self.last_options.get('display_limit', 500)
            data = self.db.get_tree_data(limit=limit)
            if data:
                self.tree.populate(data)
            self.refresh_tabs()

    def open_file_safe(self, path, target_line=None):
        """
        Безпечно відкриває файл у вбудованому редакторі.
        Якщо файл великий (>50KB), читає тільки початок.
        """
        if not path or not os.path.exists(path): return
        
        try:
            MAX_SIZE = 50 * 1024 
            file_size = os.path.getsize(path)
            content = ""
            is_cut = False
            
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                if file_size > MAX_SIZE:
                    content = f.read(MAX_SIZE)
                    is_cut = True
                else:
                    content = f.read()
            
            if is_cut: 
                content += f"\n\n{'='*60}\n⚠️ УВАГА: Файл занадто великий ({file_size/1024:.1f} KB).\nПоказано перші 50 KB. Використовуйте кнопку 'Відкрити у...' для повного перегляду.\n{'='*60}"
            
            self.preview.load_file(path)
            self.preview.editor.setPlainText(content)
            self.tabs.setCurrentIndex(0) 

            # Стрибок до рядка (якщо вказано)
            if target_line and target_line > 0:
                self.preview.scroll_to_line(target_line)

        except Exception as e:
            print(f"Error opening file: {e}")

    def on_tree_click(self, item, column):
        path = item.data(0, Qt.UserRole)
        self.open_file_safe(path, target_line=1)

    def on_search_click(self, item):
        data = item.data(Qt.UserRole)
        if isinstance(data, dict):
            self.open_file_safe(data.get('path'), target_line=data.get('line', 1))
        else:
            self.open_file_safe(data, target_line=1)

    def setup_search_tab(self):
        layout = QVBoxLayout(self.search_tab)
        top_panel = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введіть назву файлу або частину коду...")
        self.search_input.returnPressed.connect(self.run_search)
        
        self.search_lang_combo = QComboBox()
        self.search_lang_combo.addItem("Всі мови")
        
        self.search_sort_combo = QComboBox()
        self.search_sort_combo.addItems(["За розміром", "За рядками", "За назвою"])
        
        search_btn = QPushButton("🔍 Знайти")
        search_btn.clicked.connect(self.run_search)
        
        top_panel.addWidget(self.search_input, 1)
        top_panel.addWidget(self.search_lang_combo)
        top_panel.addWidget(self.search_sort_combo)
        top_panel.addWidget(search_btn)
        
        layout.addLayout(top_panel)
        
        self.results_list = SearchResultsWidget()
        self.results_list.itemClicked.connect(self.on_search_click) 
        layout.addWidget(self.results_list)

    def update_search_filters(self):
        curr = self.search_lang_combo.currentText()
        self.search_lang_combo.clear()
        self.search_lang_combo.addItem("Всі мови")
        self.search_lang_combo.addItems(self.search_engine.get_languages())
        if self.search_lang_combo.findText(curr) >= 0:
            self.search_lang_combo.setCurrentText(curr)

    def run_search(self):
        q = self.search_input.text().strip()
        self.results_list.clear()
        
        lang_filter = self.search_lang_combo.currentText()
        sort_mode = "size"
        if "рядк" in self.search_sort_combo.currentText(): sort_mode = "lines"
        elif "назв" in self.search_sort_combo.currentText(): sort_mode = "name"
        
        # 1. Пошук файлів
        files = self.search_engine.search_files(q, lang_filter, sort_mode)
        
        if files:
            msg = f"Знайдено файлів: {len(files)}"
            if not q: msg += " (Фільтр по категорії)"
            self.results_list.addItem(f"--- {msg} ---")
            for name, path, size, lines in files:
                item_data = {"path": path, "line": 1}
                self.results_list.add_result(f"📄 {name}", f"{lines} рядків • {size/1024:.1f} KB", item_data)
        else:
            self.results_list.addItem("--- Файлів не знайдено ---")

        # 2. Пошук в коді
        if len(q) >= 3:
            code_matches = self.search_engine.search_code(q, lang_filter=lang_filter)
            if code_matches:
                self.results_list.addItem(f"\n--- Знайдено в коді: {len(code_matches)} ---")
                for m in code_matches:
                    item_data = {"path": m['path'], "line": m['line']}
                    self.results_list.add_result(f"📝 {m['file']} (рядок {m['line']})", m['content'], item_data)
            elif not files:
                self.results_list.addItem("(У коді теж нічого не знайдено)")

    def load_settings(self):
        try: return json.load(open(SETTINGS_FILE)).get('repo_path')
        except: return None
        
    def save_settings(self, path):
        try: json.dump({'repo_path': path}, open(SETTINGS_FILE, 'w'))
        except: pass