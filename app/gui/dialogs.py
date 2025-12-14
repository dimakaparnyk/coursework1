# app/gui/dialogs.py
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QSpinBox, 
                             QCheckBox, QDialogButtonBox, QListWidget, 
                             QListWidgetItem, QGroupBox, QFormLayout)
from PyQt5.QtCore import Qt
from app.utils.consts import LANGUAGE_META

class ScanOptionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Налаштування сканування")
        self.resize(450, 550)
        self.layout = QVBoxLayout(self)
        
        # 1. Секція фільтрів
        self.group_limits = QGroupBox("Фільтри та Ліміти")
        form = QFormLayout()
        
        self.min_size_spin = QSpinBox()
        self.min_size_spin.setRange(0, 102400) # до 100 МБ
        self.min_size_spin.setValue(10) # Дефолт: шукаємо від 10 КБ
        self.min_size_spin.setSuffix(" KB")
        self.min_size_spin.setToolTip("Файли, менші за цей розмір, будуть пропущені")
        form.addRow("Мін. розмір файлу:", self.min_size_spin)
        
        self.limit_spin = QSpinBox()
        self.limit_spin.setRange(100, 100000)
        self.limit_spin.setValue(500) # Дефолт: показувати 500 файлів
        self.limit_spin.setSuffix(" файлів")
        self.limit_spin.setToolTip("Максимальна кількість файлів для відображення в списку")
        form.addRow("Ліміт відображення:", self.limit_spin)
        
        self.group_limits.setLayout(form)
        self.layout.addWidget(self.group_limits)
        
        # 2. Секція мов
        self.group_langs = QGroupBox("Мови програмування")
        l_layout = QVBoxLayout()
        
        self.check_all = QCheckBox("Обрати всі")
        self.check_all.setChecked(True)
        self.check_all.stateChanged.connect(self.toggle_all)
        l_layout.addWidget(self.check_all)
        
        self.lang_list = QListWidget()
        # Завантажуємо список відомих нам мов
        popular_langs = sorted(list(LANGUAGE_META.keys()))
        for lang in popular_langs:
            item = QListWidgetItem(lang)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked)
            self.lang_list.addItem(item)
            
        l_layout.addWidget(self.lang_list)
        self.group_langs.setLayout(l_layout)
        self.layout.addWidget(self.group_langs)
        
        # Кнопки ОК/Скасувати
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)

    def toggle_all(self, state):
        is_checked = (state == Qt.Checked)
        for i in range(self.lang_list.count()):
            item = self.lang_list.item(i)
            item.setCheckState(Qt.Checked if is_checked else Qt.Unchecked)

    def get_options(self):
        selected_langs = []
        for i in range(self.lang_list.count()):
            item = self.lang_list.item(i)
            if item.checkState() == Qt.Checked:
                selected_langs.append(item.text())
        
        return {
            "min_size_kb": self.min_size_spin.value(),
            "display_limit": self.limit_spin.value(),
            "languages": selected_langs
        }