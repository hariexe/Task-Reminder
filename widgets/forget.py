from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from database import Database

class ForgetWidget(QWidget):
    def __init__(self, database, stack):
        super().__init__()

        self.database = database
        self.stack = stack

        self.title_label = QLabel('<h1>Under Developmentt</h1>')
        # self.title_label = QLabel('<h1>Forgot Password</h1>')

        self.email_label = QLabel('Search for email:')
        self.email_label.setObjectName('searchemailLabel')
        self.email_label.setStyleSheet("""
            #searchemailLabel{
                color: black;
                min-width: 100px;
                max-width: 100px;
                min-height: 13px;
                max-height: 13px;
            }
        """)
        
        self.email_edit = QLineEdit()
        self.email_edit.setDisabled(True)
        self.email_edit.setObjectName('emailLineEdit')
        self.email_edit.setPlaceholderText('Harap ingat password sampai fitur ini dipublish')

        self.search_button = QPushButton('Search')
        self.search_button.setObjectName('searchButton')
        self.search_button.clicked.connect(self.search_email)

        self.back_button = QPushButton('Back To Login')
        self.back_button.setObjectName('backButton')
        self.back_button.clicked.connect(self.back_login)

        layout = QVBoxLayout()
        layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_edit)
        layout.addWidget(self.search_button)
        layout.addWidget(self.back_button)

        
        layout.setContentsMargins(100, 100, 100, 200)
        # layout.setSpacing(0)

        self.setLayout(layout)
        self.setStyleSheet("""
            ForgetWidget {
                background-color: black;
                color: black;
            }
            QPushButton:hover { background-color: grey; color: blue; }
            QPushButton:hover:!pressed { background-color: black; color: white; }
""")


    def search_email(self):
        pass

    def back_login(self):
        self.stack.setCurrentIndex(0)