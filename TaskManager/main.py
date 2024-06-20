import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget

from welcome_window import WelcomeWindow
from main_window import MainWindow

from PyQt5.QtCore import QTimer

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)


        stacked_widget = QStackedWidget()

        welcome_window = WelcomeWindow()
        stacked_widget.addWidget(welcome_window)

        main_window = MainWindow(stacked_widget)
        stacked_widget.addWidget(main_window)

        stacked_widget.setCurrentWidget(welcome_window)
        stacked_widget.show()

        QTimer.singleShot(3000, lambda: stacked_widget.setCurrentWidget(main_window))  # Переход к основному окну через 4 секунды

        sys.exit(app.exec_())
    except Exception as e:
        print(e)