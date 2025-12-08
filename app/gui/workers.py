# app/gui/workers.py
from PyQt5.QtCore import QThread, pyqtSignal
from app.core.scanner import Scanner
from app.database.store_sqlite import SQLiteStore
import traceback

class ScanWorker(QThread):
    status_signal = pyqtSignal(str)   # Текст (наприклад "Сканування...")
    progress_signal = pyqtSignal(int) # Число файлів
    finished_signal = pyqtSignal(dict) # Результат
    error_signal = pyqtSignal(str)
    
    def __init__(self, repo_path):
        super().__init__()
        self.repo_path = repo_path

    def run(self):
        try:
            self.status_signal.emit("⏳ Ініціалізація...")
            scanner = Scanner(self.repo_path)
            
            # Ця функція викликається зі сканера раз на 500 файлів
            def on_progress(count):
                self.progress_signal.emit(count)

            self.status_signal.emit("🔍 Сканування файлової системи...")
            # Передаємо callback у сканер
            data = scanner.scan(progress_callback=on_progress)
            
            self.status_signal.emit("💾 Збереження в базу даних...")
            # Нове підключення до БД для цього потоку
            db = SQLiteStore() 
            db.save_scan_result(data)
            
            self.status_signal.emit("✅ Готово!")
            self.finished_signal.emit(db.get_tree_data())
            
        except Exception as e:
            error_msg = f"Помилка: {str(e)}\n{traceback.format_exc()}"
            print(error_msg) # Дублюємо в консоль
            self.error_signal.emit(error_msg)