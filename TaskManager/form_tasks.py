import datetime
import sqlite3
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QPushButton, QMessageBox, QTextEdit, \
    QHBoxLayout, QSpinBox, QGroupBox, QComboBox, QDialogButtonBox, QDateEdit


class AddShopForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить продукты")
        self.setModal(True)
        self.resize(400, 300)

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        name_label = QLabel("Имя:")
        self.name_line_edit = QLineEdit()
        form_layout.addRow(name_label, self.name_line_edit)

        food_label = QLabel("Покупка:")
        self.food_text_edit = QTextEdit()
        form_layout.addRow(food_label, self.food_text_edit)

        amount_label = QLabel("Сумма чека:")
        self.amount_line_edit = QLineEdit()
        self.amount_line_edit.setValidator(QDoubleValidator())
        form_layout.addRow(amount_label, self.amount_line_edit)

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_food)
        button_layout.addWidget(save_button)

        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.database_connection = sqlite3.connect("BD.db")
        self.create_table()

    def create_table(self):
        cursor = self.database_connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS shop (name TEXT, items TEXT, amount REAL)")

    def save_food(self):
        name = self.name_line_edit.text().strip() + '\n( ' + str(
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' )'
        food = self.food_text_edit.toPlainText().strip()
        amount = self.amount_line_edit.text().strip()

        if not name or not food or not amount:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        try:
            amount = float(amount)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите корректную сумму.")
            return

        cursor = self.database_connection.cursor()

        cursor.execute("INSERT INTO shop VALUES (?, ?, ?)", (name, food, amount))

        self.database_connection.commit()
        self.close()
        print('Сохранено')

    def closeEvent(self, event):
        self.database_connection.close()


class AddTrainingForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить тренировку")
        self.setModal(True)
        self.resize(400, 300)

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        name_label = QLabel("Название:")
        self.name_line_edit = QLineEdit()
        form_layout.addRow(name_label, self.name_line_edit)

        exercise_label = QLabel("Упражнения:")
        self.exercise_line_edit = QTextEdit()
        form_layout.addRow(exercise_label, self.exercise_line_edit)

        fatigue_label = QLabel("Оценка усталости (от 1 до 10):")
        self.fatigue_line_edit = QLineEdit()
        form_layout.addRow(fatigue_label, self.fatigue_line_edit)

        layout.addLayout(form_layout)

        button_layout = QVBoxLayout()

        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_training)
        button_layout.addWidget(save_button)

        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.database_connection = sqlite3.connect("BD.db")
        self.create_table()

    def create_table(self):
        cursor = self.database_connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS fitness (name TEXT, exercises TEXT, fatigue INTEGER)")

    def save_training(self):
        name = self.name_line_edit.text().strip() + '\n( ' + str(
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' )'
        exercises = self.exercise_line_edit.toPlainText().strip()
        fatigue = self.fatigue_line_edit.text().strip()

        if not name or not exercises or not fatigue:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        try:
            fatigue = int(fatigue)
            if fatigue < 1 or fatigue > 10:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите корректную оценку усталости (от 1 до 10).")
            return

        cursor = self.database_connection.cursor()

        cursor.execute("INSERT INTO fitness VALUES (?, ?, ?)", (name, exercises, fatigue))

        self.database_connection.commit()
        self.close()
        print('Сохранено')

    def closeEvent(self, event):
        self.database_connection.close()


class AddFoodForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить прием пищи")
        self.resize(400, 300)

        self.layout = QVBoxLayout(self)

        self.meal_combo_box = QComboBox()
        self.meal_combo_box.addItem("Завтрак")
        self.meal_combo_box.addItem("Обед")
        self.meal_combo_box.addItem("Ужин")

        self.food_items_text_edit = QTextEdit()

        self.calories_line_edit = QLineEdit()

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(QLabel("Название приема пищи:"))
        self.layout.addWidget(self.meal_combo_box)
        self.layout.addWidget(QLabel("Что съели:"))
        self.layout.addWidget(self.food_items_text_edit)
        self.layout.addWidget(QLabel("Количество калорий:"))
        self.layout.addWidget(self.calories_line_edit)
        self.layout.addWidget(self.button_box)

    def accept(self):
        meal_name = self.meal_combo_box.currentText() + '\n( ' + str(
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' )'
        food_items = self.food_items_text_edit.toPlainText()
        calories = self.calories_line_edit.text()

        if meal_name and food_items and calories:
            if calories.isdigit():  # Проверка на числовое значение калорий
                cursor = self.parent().database_connection.cursor()
                cursor.execute("INSERT INTO food VALUES (?, ?, ?)", (meal_name, food_items, int(calories)))
                self.parent().database_connection.commit()
                self.parent().load_tasks()  # Обновление блоков задач

                super().accept()
            else:
                QMessageBox.warning(self, "Ошибка", "Количество калорий должно быть числом.")
        else:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля формы.")


class AddImportantEventForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить важное мероприятие")
        self.resize(400, 300)

        self.layout = QVBoxLayout(self)

        self.event_name_line_edit = QLineEdit()
        self.event_date_edit = QDateEdit()
        self.location_line_edit = QLineEdit()
        self.note_text_edit = QTextEdit()

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(QLabel("Название мероприятия:"))
        self.layout.addWidget(self.event_name_line_edit)
        self.layout.addWidget(QLabel("Дата мероприятия:"))
        self.layout.addWidget(self.event_date_edit)
        self.layout.addWidget(QLabel("Место проведения:"))
        self.layout.addWidget(self.location_line_edit)
        self.layout.addWidget(QLabel("Заметка:"))
        self.layout.addWidget(self.note_text_edit)
        self.layout.addWidget(self.button_box)

    def accept(self):
        event_name = self.event_name_line_edit.text()+ '\n( ' + str(
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' )'
        event_date = self.event_date_edit.date().toString("dd.MM.yyyy")
        location = self.location_line_edit.text()
        note = self.note_text_edit.toPlainText()

        if event_name and event_date:
            cursor = self.parent().database_connection.cursor()
            cursor.execute("INSERT INTO important_events VALUES (?, ?, ?, ?)", (event_name, event_date, location, note))
            self.parent().database_connection.commit()
            self.parent().load_tasks()

            super().accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните обязательные поля формы.")
