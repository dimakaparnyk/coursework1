from PyQt5.QtCore import QThread, pyqtSignal
from app.core.scanner import Scanner
from app.database.store_sqlite import SQLiteStore
import traceback

class ScanWorker(QThread):
    status_signal = pyqtSignal(str)   
    progress_signal = pyqtSignal(int) 
    finished_signal = pyqtSignal(dict) 
    error_signal = pyqtSignal(str)
    
    def __init__(self, repo_path, scan_options):
        super().__init__()
        self.repo_path = repo_path
        self.scan_options = scan_options

    def run(self):
        try:
            self.status_signal.emit("⏳ Ініціалізація сканера...")
            scanner = Scanner(self.repo_path)
            
            def on_progress(count):
                self.progress_signal.emit(count)

            min_kb = self.scan_options.get('min_size_kb', 0)
            self.status_signal.emit(f"🔍 Сканування (Фільтр > {min_kb} KB)...")
            
            # Передаємо опції в метод scan
            data = scanner.scan(self.scan_options, progress_callback=on_progress)
            
            self.status_signal.emit("💾 Збереження в базу даних...")
            db = SQLiteStore() 
            db.save_scan_result(data)
            
            self.status_signal.emit("✅ Підготовка результатів...")
            
            # Отримуємо дані з урахуванням ліміту відображення
            limit = self.scan_options.get('display_limit', 500)
            tree_data = db.get_tree_data(limit=limit)
            
            self.finished_signal.emit(tree_data)
            
        except Exception as e:
            error_msg = f"Помилка: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            self.error_signal.emit(error_msg)