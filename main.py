import sys
import os
from PyQt5.QtWidgets import QApplication

# Додаємо кореневу папку в шлях пошуку модулів, щоб Python бачив пакет 'app'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.gui.main_window import MainWindow

def main():
    """
    Точка входу в програму CodeAnalyzer.
    """
    app = QApplication(sys.argv)
    app.setApplicationName("CodeAnalyzer")
    
    # Запуск головного вікна
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()