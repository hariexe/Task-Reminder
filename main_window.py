import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from database import Database
from widgets.login import LoginWidget
from widgets.register import RegisterWidget
from widgets.main_menu import MainMenuWidget
from widgets.forget import ForgetWidget
from widgets.developer import DeveloperDialog

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.database = Database()

        self.stack = QStackedWidget(self)
        self.login_widget = LoginWidget(self.database, self.stack)
        self.main_menu_widget = MainMenuWidget(self.database, self.stack, parent=self.stack)
        self.register_widget = RegisterWidget(self.database, self.stack)
        self.forgot_widget = ForgetWidget(self.database, self.stack)
        self.developer_widget = ForgetWidget(self.database, self.stack)
        

        self.stack.addWidget(self.login_widget)
        self.stack.addWidget(self.main_menu_widget)
        self.stack.addWidget(self.register_widget)
        self.stack.addWidget(self.forgot_widget)
        self.stack.addWidget(self.developer_widget)

        layout = QVBoxLayout(self)
        layout.addWidget(self.stack)
        self.setLayout(layout)

        self.setMinimumSize(600, 500)