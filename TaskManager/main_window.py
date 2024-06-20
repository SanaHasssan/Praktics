from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QGridLayout, QLabel, QDialog, \
    QStackedWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from exercise_window import TrainingWindow
from important_window import ImportantWindow
from shop_window import ShopWindow
from food_window import FoodWindow


class MainWindow(QMainWindow):
    def __init__(self, s):
        super().__init__()
        self.setWindowTitle("Планировщик задач")
        self.resize(600, 400)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        categories_label = QLabel("Выберите категорию:")
        categories_label.setFont(QFont("Arial", 14, QFont.Bold))
        categories_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(categories_label)

        categories_grid_layout = QGridLayout()

        categories = ["Питание", "Тренировки", "Покупки","Важное"]
        row, col = 0, 0
        for category in categories:
            category_button = QPushButton(category)
            category_button.clicked.connect(self.category_selected)
            category_button.setStyleSheet(
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
            categories_grid_layout.addWidget(category_button, row, col)
            col += 1
            if col == 2:
                col = 0
                row += 1

        layout.addLayout(categories_grid_layout)

        # Create a stacked widget to manage the different category windows
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # Create instances of the category windows
        self.shop_window = ShopWindow(self.stacked_widget)
        self.training_window = TrainingWindow(self.stacked_widget)
        self.food_window = FoodWindow(self.stacked_widget)
        self.im_window = ImportantWindow(self.stacked_widget)
        # Add the category windows to the stacked widget
        self.stacked_widget.addWidget(self.shop_window)
        self.stacked_widget.addWidget(self.training_window)
        self.stacked_widget.addWidget(self.food_window)
        self.stacked_widget.addWidget(self.im_window)


    def category_selected(self):
        sender = self.sender()
        selected_category = sender.text()

        if selected_category == "Покупки":
            self.stacked_widget.setCurrentWidget(self.shop_window)
        elif selected_category == "Тренировки":
            self.stacked_widget.setCurrentWidget(self.training_window)
        elif selected_category == "Питание":
            self.stacked_widget.setCurrentWidget(self.food_window)
        elif selected_category == "Важное":
            try:
                self.stacked_widget.setCurrentWidget(self.im_window)
            except Exception as e:
                print(e)

