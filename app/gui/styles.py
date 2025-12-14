APP_THEME = """
/* 1. Глобальні налаштування */
QMainWindow, QWidget {
    background-color: #ffffff;
    color: #333333;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
}

/* 2. Таблиці та Дерева */
QTreeWidget, QListWidget, QTableWidget {
    background-color: #ffffff;
    alternate-background-color: #f9f9f9; /* Ледь сірий для парних рядків */
    color: #333333;
    border: 1px solid #e0e0e0;
    selection-background-color: #e5f3ff;
    selection-color: #0078d4;
    outline: none;
}

QTreeWidget::item, QListWidget::item {
    height: 28px; /* Фіксована висота рядка */
    color: #333333;
    border: none;
}

QTreeWidget::item:hover, QListWidget::item:hover {
    background-color: #f0f0f0;
    color: #000000;
}

QTreeWidget::item:selected, QListWidget::item:selected {
    background-color: #cce8ff; /* Світло-синій фон виділення */
    color: #005a9e; /* Темно-синій текст */
    border: none;
}

/* 3. Заголовки (Header) */
QHeaderView::section {
    background-color: #f5f5f5;
    color: #333333;
    padding: 6px;
    border: none;
    border-bottom: 2px solid #e0e0e0;
    border-right: 1px solid #e0e0e0;
    font-weight: bold;
    font-size: 12px;
}

/* 4. Кнопки */
QPushButton {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    color: #333333;
    padding: 6px 15px;
    border-radius: 4px;
}
QPushButton:hover {
    background-color: #f0faff;
    border-color: #0078d4;
    color: #0078d4;
}
QPushButton:pressed {
    background-color: #0078d4;
    color: #ffffff;
}

/* 5. Поля вводу */
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 4px;
    color: #333333;
    padding: 5px;
}
QLineEdit:focus, QTextEdit:focus {
    border: 1px solid #0078d4;
}

/* 6. Вкладки (Tabs) */
QTabWidget::pane {
    border: 1px solid #e0e0e0;
    top: -1px;
}
QTabBar::tab {
    background-color: #f5f5f5;
    color: #555555;
    padding: 8px 20px;
    border: 1px solid transparent;
    border-bottom: none;
}
QTabBar::tab:selected {
    background-color: #ffffff;
    color: #0078d4;
    border: 1px solid #e0e0e0;
    border-bottom: 1px solid #ffffff; /* Зливається з контентом */
    font-weight: bold;
}
QTabBar::tab:hover {
    background-color: #eef;
}

/* 7. Скролбари */
QScrollBar:vertical {
    border: none;
    background: #f0f0f0;
    width: 10px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #c1c1c1;
    min-height: 20px;
    border-radius: 5px;
}
QScrollBar::handle:vertical:hover {
    background: #a8a8a8;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* 8. ToolBar */
QToolBar {
    background-color: #ffffff;
    border-bottom: 1px solid #e0e0e0;
    spacing: 5px;
}
"""