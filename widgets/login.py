from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from database import Database
from widgets.forget import ForgetWidget

class LoginWidget(QWidget):
    def __init__(self, database, stack):
        super().__init__()

        self.database = database
        self.stack = stack

        self.title_label = QLabel('<h1>Login</h1>')
        self.title_label.setObjectName('titLabel')
        self.nickname_label = QLabel('Nickname:')
        self.nickname_label.setObjectName('nickLabel')
        self.password_label = QLabel('Password:')
        self.password_label.setObjectName('passLabel')

        self.nickname_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton('Login')
        self.login_button.setShortcut(QKeySequence(Qt.Key.Key_E))
        self.login_button.setObjectName('logBtn')
        self.login_button.clicked.connect(self.login_user)

        self.register_button = QPushButton('Register')
        self.register_button.setObjectName('regBtn')
        self.register_button.clicked.connect(self.show_register_form)

        self.remember_checkbox = QCheckBox('Keep login on this device')
        # self.remember_checkbox.clicked.connect(self.checked_button)
        
        self.forget_button = QPushButton('Forgot Password')
        self.forget_button.setFixedWidth(100)
        self.forget_button.setObjectName('fgtBtn')
        self.forget_button.clicked.connect(self.show_forget_form)

        layout = QVBoxLayout()
        layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.nickname_label)
        layout.addWidget(self.nickname_edit,)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.remember_checkbox)
        layout.addWidget(self.login_button)
        layout.addWidget(self.forget_button, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.register_button)

        self.nickname_edit.setContentsMargins(0, 0, 0, 10)
        self.password_edit.setContentsMargins(0, 0, 0, 10)

        layout.setContentsMargins(100, 100, 100, 100)

        self.setLayout(layout)

        self.qss()

        self.load_saved_credentials()


    def qss(self):
        style_sheet = """
            QLabel#nickLabel, #passLabel{
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
            QPushButton#logBtn, #regBtn  {
                background-color: black;
                color: white;
            }
            QPushButton#logBtn:hover, #regBtn:hover  {
                background-color: grey;
                color: black;
            }
        """
        self.setStyleSheet(style_sheet)


    def load_saved_credentials(self):
        settings = QSettings("MyApp", "MyAppSettings")
        remember_me = settings.value("remember_me", False, type=bool)

        if remember_me:
            nickname = settings.value("nickname", "")
            password = settings.value("password", "")
            self.nickname_edit.setText(nickname)
            self.password_edit.setText(password)
            self.remember_checkbox.setChecked(True)


    def login_user(self):
        nickname = self.nickname_edit.text()
        password = self.password_edit.text()
        remember_me = self.remember_checkbox.isChecked()

        if not self.database.authenticate_user(nickname, password):
            QMessageBox.warning(self, 'Error', 'Invalid nickname or password')
            return

        if remember_me:
            self.save_credentials(nickname, password)

        QMessageBox.information(self, 'Information', 'Login successful!')
        self.stack.setCurrentIndex(1)  # pindah ke main menu    
        self.stack.currentWidget().set_welcome_message(nickname)

    def authenticate_user(self, nickname, password):
        # Check if the user is registered
        if self.is_user_registered(nickname):
            # Now check the password
            stored_password = self.get_stored_password(nickname)
            if stored_password == password:
                # Password is correct, user is authenticated
                return True
            else:
                # Incorrect password
                return False
    
        else:
            # User is not registered
            return False

    def clear_saved_credentials(self):
        settings = QSettings("MyApp", "MyAppSettings")
        settings.remove("nickname")
        settings.remove("password")
        settings.setValue("remember_me", False)        
    
    def save_credentials(self, nickname, password):
        settings = QSettings("MyApp", "MyAppSettings")
        settings.setValue("nickname", nickname)
        settings.setValue("password", password)
        settings.setValue("remember_me", True)

    
    def show_register_form(self):
        self.stack.setCurrentIndex(2)  # pindah ke register form


    def checked_button(self):
        pass


    def show_forget_form(self):
        # self.forgot_password_widget = ForgetWidget(self.database, self.stack)
        # self.forgot_password_widget.show()
        self.stack.setCurrentIndex(3)   

