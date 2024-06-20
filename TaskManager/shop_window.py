# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QDialog, QLabel, QScrollArea, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sqlite3

from form_tasks import AddShopForm
class ShopWindow(QMainWindow):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setWindowTitle("Планировщик задач")
        self.resize(600, 400)

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.main_layout = QVBoxLayout(self.main_widget)

        add_task_button = QPushButton("Добавить покупку")
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

        self.task_blocks_widget = QWidget()
        self.task_blocks_layout = QVBoxLayout()
        self.task_blocks_layout.setAlignment(Qt.AlignTop)  # Выравнивание блоков задач по верхнему краю

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.task_blocks_widget)

        self.main_layout.addWidget(scroll_area)

        self.database_connection = sqlite3.connect("BD.db")  # Подключение к базе данных SQLite
        cursor = self.database_connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS shop (name TEXT, items TEXT, amount REAL)")
        self.load_tasks()




    def open_add_task_dialog(self):
        form_tasks_dialog = AddShopForm()
        form_tasks_dialog.exec_()

        self.load_tasks()  # Обновление блоков задач

    def display_task_block(self, task_data):
        name = task_data
        existing_blocks = self.task_blocks_widget.findChildren(QWidget)
        for block in existing_blocks:
            if block.property("name") == name:
                # Обновление содержимого существующего блока
                task_label = block.findChild(QLabel)
                task_label.setText(name)
                return

        # Создание нового блока задач
        task_block = QWidget()
        task_block.setFixedSize(400, 100)
        task_block.setStyleSheet(
            """
            QWidget {
                background-color: %s;
                border-radius: 5px;
                border:1px inset black;
                
            }
            """
            % self.get_category_color(name)
        )
        task_block.setProperty("name", name)  # Установка свойства "name" для блока задач

        task_label = QLabel(name)
        task_label.setAlignment(Qt.AlignCenter)

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

        task_layout = QHBoxLayout()
        task_layout.addWidget(task_label)
        task_layout.addWidget(delete_button)
        task_block.setLayout(task_layout)

        self.task_blocks_layout.addWidget(task_block)

        self.task_blocks_widget.setLayout(self.task_blocks_layout)
        task_block = QWidget()
        # ...

        details_button = QPushButton("Детали")
        details_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4287f5;
                color: #ffffff;
                font-size: 12px;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #0052cc;
            }
            """
        )
        details_button.clicked.connect(self.show_task_details)
        task_layout.addWidget(details_button)

        # ...

    def get_category_color(self, category):
        category_colors = {
            "Питание": "#FF6F61",
            "Тренировки": "#6EC664",
            "Покупки": "#FECD52",
            "Расписание": "#75D0F4",
            "Важное": "#AB8AFF",
        }
        return category_colors.get(category, "#f0f0f0")


    def delete_task(self):
        sender = self.sender()
        task_block = sender.parentWidget()
        category = task_block.property("name")

        reply = QMessageBox.question(
            self,
            "Удаление задачи",
            f"Вы уверены, что хотите удалить задачу в категории '{category}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            cursor = self.database_connection.cursor()

            # Удаление задачи из таблицы tasks
            cursor.execute("DELETE FROM shop WHERE name=?", (category,))

            self.database_connection.commit()

            task_block.setParent(None)  # Удаление блока задач из интерфейса

    def load_tasks(self):
        # Очистка блоков задач перед загрузкой новых данных
        for i in reversed(range(self.task_blocks_layout.count())):
            self.task_blocks_layout.itemAt(i).widget().setParent(None)

        cursor = self.database_connection.cursor()

        # Получение всех задач из таблицы tasks
        # Получение всех продуктов из таблицы food
        cursor.execute("SELECT name FROM shop")
        foods = cursor.fetchall()

        for food in foods:
            self.display_task_block(food[0])


    def closeEvent(self, event):
        self.database_connection.close()  # Закрытие подключения к базе данных SQLite
        event.accept()

    def show_task_details(self):
        try:
            sender = self.sender()
            task_block = sender.parentWidget()
            category = task_block.property("name")

            cursor = self.database_connection.cursor()

            # Получение информации о продуктах из таблицы food
            cursor.execute("SELECT name, items, amount FROM shop WHERE name=?", (category,))
            food_data = cursor.fetchall()
            food = food_data[0]
            # Создание и отображение диалогового окна с полной информацией о задаче
            details_dialog = QDialog()
            details_dialog.setWindowTitle("Детали задачи")
            details_dialog.setModal(True)
            details_dialog.resize(400, 300)

            layout = QVBoxLayout()

            category_label = QLabel(f"Категория: Покупки")
            category_label.setFont(QFont("Arial", 14, QFont.Bold))
            layout.addWidget(category_label)
            name = food[0].split('\n')
            foods_label = QLabel("Название: "+name[0])
            foods_label.setFont(QFont("Arial", 12, QFont.Bold))
            layout.addWidget(foods_label)


            food_name_label = QLabel(f"Дата добавления: {name[1]}")
            layout.addWidget(food_name_label)

            food_item_label = QLabel(f"{food[1]}")
            layout.addWidget(food_item_label)

            amount_label = QLabel(f"Сумма чека: {food[2]}")
            layout.addWidget(amount_label)

            layout.addSpacing(10)

            details_dialog.setLayout(layout)
            details_dialog.exec_()
        except Exception as e:
            print(e)