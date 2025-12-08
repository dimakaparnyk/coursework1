# main.py
import sys
import os
from PyQt5.QtWidgets import QApplication

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.gui.main_window import MainWindow
from app.gui.themes import apply_dark_theme

def main():
    app = QApplication(sys.argv)
    
    # Стартуємо з темною темою
    apply_dark_theme(app)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()