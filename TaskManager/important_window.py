# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QDialog, QLabel, QScrollArea, QHBoxLayout, QMessageBox, QComboBox, QTextEdit, QLineEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sqlite3

from form_tasks import AddImportantEventForm


class ImportantWindow(QMainWindow):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setWindowTitle("Планировщик задач")
        self.resize(600, 400)

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.main_layout = QVBoxLayout(self.main_widget)

        add_task_button = QPushButton("Добавить событие")
        add_task_button.clicked.connect(self.open_add_task_dialog)
        add_task_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4287f5;
                color: #ffffff;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0052cc;
            }
            """
        )

        self.main_layout.addWidget(add_task_button)

        self.task_blocks_container = QWidget()  # Контейнер для блоков задач
        self.task_blocks_layout = QVBoxLayout(self.task_blocks_container)
        self.task_blocks_layout.setAlignment(Qt.AlignTop)  # Выравнивание блоков задач по верхнему краю

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.task_blocks_container)

        self.main_layout.addWidget(scroll_area)

        self.database_connection = sqlite3.connect("BD.db")  # Подключение к базе данных SQLite
        cursor = self.database_connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS important_events (event_name TEXT, event_date DATE, location TEXT, note TEXT)")
        self.load_tasks()

    def open_add_task_dialog(self):
        form_tasks_dialog = AddImportantEventForm(self)
        form_tasks_dialog.exec_()

        self.load_tasks()  # Обновление блоков задач

    def display_task_block(self, task_data):
        event_name = task_data
        existing_blocks = self.task_blocks_container.findChildren(QWidget)
        for block in existing_blocks:
            if block.property("event_name") == event_name:
                # Обновление содержимого существующего блока
                event_label = block.findChild(QLabel)
                event_label.setText(event_name)
                return

        # Создание нового блока задач
        task_block = QWidget()
        task_block.setFixedSize(400, 100)
        task_block.setStyleSheet(
            """
            QWidget {
                background-color: %s;
                border-radius: 5px;
                border: 1px inset black;
            }
            """
            % self.get_category_color(event_name)
        )
        task_block.setProperty("event_name", event_name)  # Установка свойства "event_name" для блока задач

        event_label = QLabel(event_name)
        event_label.setAlignment(Qt.AlignCenter)

        delete_button = QPushButton("Удалить")
        delete_button.setStyleSheet(
            """
            QPushButton {
                background-color: #FF6F61;
                color: #ffffff;
                font-size: 12px;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #CC5B51;
            }
            """
        )
        delete_button.clicked.connect(self.delete_task)

        details_button = QPushButton("Детали")
        details_button.setStyleSheet(
            """
            QPushButton {
                background-color: #7a8aff;
                color: #ffffff;
                font-size: 12px;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #515bcc;
            }
            """
        )
        details_button.clicked.connect(lambda _, event=event_name: self.show_details(event))

        task_layout = QVBoxLayout()
        task_layout.addWidget(event_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(details_button)
        button_layout.addWidget(delete_button)

        task_layout.addLayout(button_layout)
        task_block.setLayout(task_layout)

        self.task_blocks_layout.addWidget(task_block)

    def load_tasks(self):
        cursor = self.database_connection.cursor()
        cursor.execute("SELECT event_name FROM important_events")
        events = cursor.fetchall()

        self.clear_task_blocks()

        for event in events:
            self.display_task_block(event[0])

    def delete_task(self):
        sender_button = self.sender()
        event_name = sender_button.parentWidget().property("event_name")

        confirm_dialog = QMessageBox.question(
            self,
            "Подтверждение удаления",
            "Вы уверены, что хотите удалить событие?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirm_dialog == QMessageBox.Yes:
            cursor = self.database_connection.cursor()
            cursor.execute("DELETE FROM important_events WHERE event_name=?", (event_name,))
            self.database_connection.commit()

            self.load_tasks()

    def get_category_color(self, category):
        d = {
            "Завтрак": "#ffa07a",  # Лососевый
            "Обед": "#00ced1",  # Темно-бирюзовый
            "Ужин": "#9370db",  # Средне-пурпурный
        }  # Белый, если категория не найдена
        for i in d.keys():
            if i in category:
                return d.get(i, '#fffff')

    def clear_task_blocks(self):
        for i in reversed(range(self.task_blocks_layout.count())):
            self.task_blocks_layout.itemAt(i).widget().setParent(None)

    def show_details(self, event_name):
        cursor = self.database_connection.cursor()
        cursor.execute("SELECT event_date, location, note FROM important_events WHERE event_name=?", (event_name,))
        result = cursor.fetchone()

        if result:
            event_date, location, note = result
            details_dialog = QDialog(self)
            details_dialog.setWindowTitle("Детали события")

            details_layout = QVBoxLayout(details_dialog)

            event_date_label = QLabel(f"Дата события: {event_date}")
            event_date_label.setAlignment(Qt.AlignCenter)

            location_label = QLabel(f"Место: {location}")
            location_label.setAlignment(Qt.AlignCenter)

            note_label = QLabel(f"Заметка: {note}")
            note_label.setAlignment(Qt.AlignCenter)

            close_button = QPushButton("Закрыть")
            close_button.clicked.connect(details_dialog.close)

            details_layout.addWidget(event_date_label)
            details_layout.addWidget(location_label)
            details_layout.addWidget(note_label)
            details_layout.addWidget(close_button)

            details_dialog.setLayout(details_layout)
            details_dialog.exec_()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось получить детали события.")


