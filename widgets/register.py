from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from database import Database

class RegisterWidget(QWidget):
    def __init__(self, database, stack):
        super().__init__()

        self.database = database
        self.stack = stack
        
        self.nickname_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.email_edit = QLineEdit()

        self.title_label = QLabel('<h1>Register</h1>')
        self.title_label.setObjectName('titLabel')

        self.nickname_label = QLabel('Nickname:')
        self.nickname_label.setObjectName('nickLabel')
        
        self.password_label = QLabel('Password:')
        self.password_label.setObjectName('passLabel')
        
        self.email_label = QLabel('Email:')
        self.email_label.setObjectName('mailLabel')

        register_button = QPushButton('Register')
        register_button.setObjectName('regBtn')
        register_button.clicked.connect(self.register_user)

        back_button = QPushButton('Back to Login')
        back_button.setObjectName('backBtn')
        back_button.clicked.connect(self.show_login_form)


        self.nickname_edit.setContentsMargins(0, 0, 0, 10)
        self.password_edit.setContentsMargins(0, 0, 0, 10)
        self.email_edit.setContentsMargins(0, 0, 0, 10)

        layout = QVBoxLayout()
        layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.nickname_label)
        layout.addWidget(self.nickname_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_edit)
        layout.addWidget(register_button) 
        layout.addWidget(back_button) 

        layout.setContentsMargins(100, 100, 100, 100)

        self.setLayout(layout)

        self.qss()

    
    def qss(self):
        style_sheet = """
            QLabel#nickLabel, #passLabel, #mailLabel{
                color: black;
                font-weight: bold;
                min-width: 100px;
                max-width: 100px;
                min-height: 13px;
                max-height: 13px;
            }
            QLabel#titLabel  {
                min-height: 13px;
            }
            QPushButton#fgtBtn  {
                background-color: transparent;
            }
            QPushButton#fgtBtn:hover  {
                color: red;
            }
            QPushButton#backBtn, #regBtn  {
                background-color: black;
                color: white;
            }
            QPushButton#backBtn:hover, #regBtn:hover  {
                background-color: grey;
                color: black;
            }
        """
        self.setStyleSheet(style_sheet)


    def register_user(self):
        nickname = self.nickname_edit.text()
        password = self.password_edit.text()
        email = self.email_edit.text()

        if not nickname or not password or not email:
            QMessageBox.warning(self, 'Error', 'Please fill in all fields.')
            return

        self.database.register_user(nickname, password, email)
        QMessageBox.information(self, 'Success', 'User registered successfully.')
        self.stack.setCurrentIndex(0)  # Switch back to the login form

    def show_login_form(self):
        self.stack.setCurrentIndex(0)  # Switch to the login form