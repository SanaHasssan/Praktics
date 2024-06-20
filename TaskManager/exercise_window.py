from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QDialog, QLabel, QScrollArea, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sqlite3

from form_tasks import AddTrainingForm

class TrainingWindow(QMainWindow):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setWindowTitle("Планировщик тренировок")
        self.resize(600, 400)

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.main_layout = QVBoxLayout(self.main_widget)

        add_task_button = QPushButton("Добавить тренировку")
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
        self.task_blocks_layout.setAlignment(Qt.AlignTop)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.task_blocks_widget)

        self.main_layout.addWidget(scroll_area)
        print('2')
        self.database_connection = sqlite3.connect("BD.db")
        cursor = self.database_connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS fitness (name TEXT, exercises TEXT, fatigue INTEGER)")

        self.load_tasks()
        print('1')

    def open_add_task_dialog(self):
        try:
            form_tasks_dialog = AddTrainingForm()
            form_tasks_dialog.exec_()

            self.load_tasks()
        except Exception as e:
            print(e)

    def display_task_block(self, task_data):
        name, exercises, fatigue = task_data
        existing_blocks = self.task_blocks_widget.findChildren(QWidget)
        for block in existing_blocks:
            if block.property("name") == name:
                task_label = block.findChild(QLabel)
                task_label.setText(name)
                return

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
            % self.get_category_color(name)
        )
        task_block.setProperty("name", name)

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
            cursor.execute("DELETE FROM fitness WHERE name=?", (category,))
            self.database_connection.commit()
            task_block.setParent(None)

    def load_tasks(self):
        for i in reversed(range(self.task_blocks_layout.count())):
            self.task_blocks_layout.itemAt(i).widget().setParent(None)

        cursor = self.database_connection.cursor()
        cursor.execute("SELECT name, exercises, fatigue FROM fitness")
        trainings = cursor.fetchall()

        for training in trainings:
            self.display_task_block(training)

    def closeEvent(self, event):
        self.database_connection.close()
        event.accept()

    def show_task_details(self):
        try:
            sender = self.sender()
            task_block = sender.parentWidget()
            category = task_block.property("name")

            cursor = self.database_connection.cursor()
            cursor.execute("SELECT name, exercises, fatigue FROM fitness WHERE name=?", (category,))
            training_data = cursor.fetchall()

            details_dialog = QDialog()
            details_dialog.setWindowTitle("Детали тренировки")
            details_dialog.setModal(True)
            details_dialog.resize(400, 300)

            layout = QVBoxLayout()

            category_label = QLabel(f"Категория: Тренировки")
            category_label.setFont(QFont("Arial", 14, QFont.Bold))
            category_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(category_label)
            training = training_data[0]
            exercises_label = QLabel("Упражнения:"+training[0])
            exercises_label.setFont(QFont("Arial", 12, QFont.Bold))
            layout.addWidget(exercises_label)


            exercises_str = training[1].replace('\n', '<br>')
            exercises_label = QLabel(exercises_str)
            layout.addWidget(exercises_label)

            fatigue_label = QLabel(f"Оценка усталости: {training[2]}")
            layout.addWidget(fatigue_label)

            layout.addSpacing(10)

            details_dialog.setLayout(layout)
            details_dialog.exec_()
        except Exception as e:
            print(e)
