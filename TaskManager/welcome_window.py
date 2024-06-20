from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QApplication
from PyQt5.QtGui import QPixmap, QPainter, QPalette, QColor
from PyQt5.QtCore import Qt, QDate, QTime

class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Планировщик")
        self.resize(800, 600)  # Увеличение размеров окна

        layout = QVBoxLayout()

        self.date_label = QLabel()
        self.date_label.setAlignment(Qt.AlignCenter)
        self.date_label.setStyleSheet("font-size: 48px; color: #333;")  # Изменение стиля текста
        layout.addWidget(self.date_label)

        self.greeting_label = QLabel()
        self.greeting_label.setAlignment(Qt.AlignCenter)
        self.greeting_label.setStyleSheet("font-size: 48px; color: #333;")  # Изменение стиля текста
        layout.addWidget(self.greeting_label)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.show_current_date()
        self.show_greeting()
        self.set_background_image()

    def show_current_date(self):
        current_date = QDate.currentDate().toString(Qt.DefaultLocaleLongDate)
        self.date_label.setText(current_date)

    def show_greeting(self):
        current_hour = QTime.currentTime().hour()

        if current_hour < 12:
            greeting = "Доброе утро"
        elif current_hour < 18:
            greeting = "Добрый день"
        else:
            greeting = "Добрый вечер"

        self.greeting_label.setText(greeting)

    def set_background_image(self):
        current_hour = QTime.currentTime().hour()

        if current_hour < 12:
            image_path = "images/morning.jpg"
        elif current_hour < 18:
            image_path = "images/afternoon.jpg"
        else:
            image_path = "images/evening.jpeg"

        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # Прозрачный фон для текста
        pal = self.image_label.palette()
        pal.setColor(QPalette.Foreground, QColor(255, 255, 255, 200))
        self.greeting_label.setPalette(pal)
        self.date_label.setPalette(pal)

    def center_window(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
