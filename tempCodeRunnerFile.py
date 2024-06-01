import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)  # Prevent the application from quitting when the last window is closed
    window = MainWindow()
    window.setWindowTitle("Task Reminder")
    window.show()
    sys.exit(app.exec())