# app/gui/styles.py

# === ТЕМНА ТЕМА (MODERN DARK) ===
DARK_THEME = """
/* Загальний фон */
QMainWindow, QWidget {
    background-color: #1e1e1e;
    color: #cccccc;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
}

/* Сайдбар і списки (Дерево, Результати пошуку) */
QTreeWidget, QListWidget, QTableWidget {
    background-color: #252526;
    border: none;
    outline: none;
    border-radius: 4px;
}
QTreeWidget::item, QListWidget::item {
    padding: 6px;
    border-radius: 4px;
}
QTreeWidget::item:hover, QListWidget::item:hover {
    background-color: #2a2d2e;
}
QTreeWidget::item:selected, QListWidget::item:selected {
    background-color: #37373d;
    color: white;
    border-left: 3px solid #007acc;
}

/* Заголовки таблиць/дерев */
QHeaderView::section {
    background-color: #252526;
    color: #aaaaaa;
    border: none;
    padding: 6px;
    font-weight: bold;
    border-bottom: 1px solid #333;
}

/* Кнопки (Windows 11 style) */
QPushButton {
    background-color: #3a3a3a;
    color: white;
    border: 1px solid #454545;
    padding: 6px 16px;
    border-radius: 6px;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #454545;
    border-color: #606060;
}
QPushButton:pressed {
    background-color: #007acc;
    border-color: #007acc;
}
/* Спеціальні кнопки (акцентні) */
QPushButton[class="accent"] {
    background-color: #007acc;
    border: none;
}
QPushButton[class="accent"]:hover {
    background-color: #0062a3;
}

/* Поля вводу */
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox {
    background-color: #3c3c3c;
    border: 1px solid #3c3c3c;
    border-radius: 4px;
    color: #e0e0e0;
    padding: 6px;
    selection-background-color: #264f78;
}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border: 1px solid #007acc;
    background-color: #252526;
}

/* Вкладки (Tabs) */
QTabWidget::pane {
    border-top: 1px solid #333;
    background-color: #1e1e1e;
}
QTabBar::tab {
    background-color: #1e1e1e;
    color: #888;
    padding: 10px 20px;
    border: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}
QTabBar::tab:selected {
    color: white;
    background-color: #1e1e1e;
    border-bottom: 2px solid #007acc;
}
QTabBar::tab:hover {
    background-color: #2d2d2d;
    color: #ccc;
}

/* Прогрес бар */
QProgressBar {
    background-color: #252526;
    border: none;
    border-radius: 2px;
    height: 6px;
    text-align: center;
}
QProgressBar::chunk {
    background-color: #007acc;
    border-radius: 2px;
}

/* Скроллбар */
QScrollBar:vertical {
    border: none;
    background: #1e1e1e;
    width: 10px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #424242;
    min-height: 20px;
    border-radius: 5px;
}
QScrollBar::handle:vertical:hover {
    background: #4f4f4f;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""

# === СВІТЛА ТЕМА (MODERN LIGHT) ===
LIGHT_THEME = """
/* Загальний фон */
QMainWindow, QWidget {
    background-color: #f3f3f3;
    color: #333333;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
}

/* Списки */
QTreeWidget, QListWidget, QTableWidget {
    background-color: #ffffff;
    border: 1px solid #e5e5e5;
    border-radius: 4px;
    outline: none;
}
QTreeWidget::item, QListWidget::item {
    padding: 6px;
    border-radius: 4px;
}
QTreeWidget::item:hover, QListWidget::item:hover {
    background-color: #f0f0f0;
}
QTreeWidget::item:selected, QListWidget::item:selected {
    background-color: #e5f3ff;
    color: #0078d4;
    border-left: 3px solid #0078d4;
}

/* Кнопки */
QPushButton {
    background-color: #ffffff;
    border: 1px solid #d1d1d1;
    border-radius: 6px;
    color: #333;
    padding: 6px 16px;
}
QPushButton:hover {
    background-color: #fbfbfb;
    border-color: #c0c0c0;
}
QPushButton:pressed {
    background-color: #0078d4;
    color: white;
    border-color: #0078d4;
}

/* Поля вводу */
QLineEdit, QTextEdit, QComboBox {
    background-color: #ffffff;
    border: 1px solid #d1d1d1;
    border-radius: 4px;
    color: #333;
    padding: 6px;
}
QLineEdit:focus {
    border: 1px solid #0078d4;
}

/* Вкладки */
QTabWidget::pane {
    border-top: 1px solid #e0e0e0;
}
QTabBar::tab {
    background-color: #f3f3f3;
    color: #666;
    padding: 10px 20px;
    border: none;
}
QTabBar::tab:selected {
    background-color: #f3f3f3;
    color: #000;
    border-bottom: 2px solid #0078d4;
}
QTabBar::tab:hover {
    background-color: #e9e9e9;
}

/* Прогрес */
QProgressBar {
    background-color: #e0e0e0;
    border: none;
    height: 6px;
    border-radius: 2px;
}
QProgressBar::chunk {
    background-color: #0078d4;
    border-radius: 2px;
}
"""