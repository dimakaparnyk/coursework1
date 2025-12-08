# app/gui/themes.py
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

def apply_dark_theme(app):
    app.setStyle("Fusion")
    palette = QPalette()
    dark_gray = QColor(45, 45, 45)
    gray = QColor(53, 53, 53)
    black = QColor(25, 25, 25)
    text = QColor(220, 220, 220)
    
    palette.setColor(QPalette.Window, gray)
    palette.setColor(QPalette.WindowText, text)
    palette.setColor(QPalette.Base, black)
    palette.setColor(QPalette.AlternateBase, dark_gray)
    palette.setColor(QPalette.ToolTipBase, text)
    palette.setColor(QPalette.ToolTipText, text)
    palette.setColor(QPalette.Text, text)
    palette.setColor(QPalette.Button, dark_gray)
    palette.setColor(QPalette.ButtonText, text)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

def apply_light_theme(app):
    app.setStyle("Fusion")
    palette = QPalette()
    # Стандартні світлі кольори Fusion
    palette.setColor(QPalette.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.WindowText, Qt.black)
    palette.setColor(QPalette.Base, Qt.white)
    palette.setColor(QPalette.AlternateBase, QColor(233, 231, 227))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.black)
    palette.setColor(QPalette.Text, Qt.black)
    palette.setColor(QPalette.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ButtonText, Qt.black)
    palette.setColor(QPalette.Link, QColor(0, 0, 255))
    palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
    palette.setColor(QPalette.HighlightedText, Qt.white)
    app.setPalette(palette)