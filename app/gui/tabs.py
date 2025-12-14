# app/gui/tabs.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QTextEdit, QMessageBox, QLabel)
from PyQt5.QtGui import QFont, QColor
import sqlite3

class SQLConsoleWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        # Підказка
        tips = QLabel("Введіть повний SQL запит. Таблиці: <b>files</b> (name, path, size, lines, language_id), <b>languages</b> (name, file_count)")
        tips.setStyleSheet("color: #555; margin-bottom: 5px;")
        layout.addWidget(tips)
        
        # Поле вводу
        self.txt = QTextEdit()
        self.txt.setPlaceholderText("SELECT * FROM files ORDER BY lines DESC LIMIT 10")
        self.txt.setMaximumHeight(100)
        self.txt.setFont(QFont("Consolas", 11))
        self.txt.setStyleSheet("border: 1px solid #ccc; border-radius: 4px; padding: 5px; background: white;")
        layout.addWidget(self.txt)
        
        # Кнопка
        btn = QPushButton("Виконати запит (RUN)")
        btn.clicked.connect(self.run)
        btn.setStyleSheet("""
            QPushButton { background-color: #0078d4; color: white; border: none; padding: 8px; border-radius: 4px; font-weight: bold; }
            QPushButton:hover { background-color: #106ebe; }
        """)
        layout.addWidget(btn)
        
        # Таблиця результатів
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Стиль таблиці
        self.table.setStyleSheet("""
            QTableWidget { gridline-color: #ddd; background: white; }
            QHeaderView::section { background-color: #f0f0f0; border: none; border-bottom: 1px solid #ccc; padding: 4px; }
        """)
        layout.addWidget(self.table)

    def run(self):
        query = self.txt.toPlainText().strip()
        if not query: return
        try:
            conn = sqlite3.connect("code_base.db")
            c = conn.cursor()
            c.execute(query)
            
            # 1. Якщо це SELECT (повертає дані)
            if c.description:
                cols = [d[0] for d in c.description]
                data = c.fetchall()
                
                self.table.setColumnCount(len(cols))
                self.table.setHorizontalHeaderLabels(cols)
                self.table.setRowCount(len(data))
                
                for i, row in enumerate(data):
                    for j, val in enumerate(row):
                        self.table.setItem(i, j, QTableWidgetItem(str(val)))
                
                QMessageBox.information(self, "Успіх", f"Знайдено записів: {len(data)}")
            
            # 2. Якщо це UPDATE, DELETE, INSERT, DROP (змінює дані)
            else:
                conn.commit()
                QMessageBox.information(self, "Успіх", f"Запит виконано. Змінено рядків: {c.rowcount}")
                
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "SQL Error", f"Помилка у запиті:\n{str(e)}")