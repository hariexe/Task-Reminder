import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from database import Database

class DeveloperDialog(QDialog):
    def __init__(self, database, parent=None):
        super().__init__(parent)

        self.database = database

        self.setWindowTitle("Developer")
        self.setFixedSize(500, 500)

        self.widget = QLabel(self)
        self.widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.nama = QLabel('Batman')
        self.nama.setObjectName('namaLabel')
        self.nama.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.teks = QLabel("Mohon do'akan saya agar mendapatkan ridho dan rahmat Tuhan")
        self.teks.setObjectName('teksLabel')
        self.teks.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pixmap = QPixmap("widgets/image/theripper2.jpeg")

        scaled_pixmap = pixmap.scaled(QSize(500, 500), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)

        self.widget.setPixmap(scaled_pixmap)


        self.setup_ui()
        self.qss()


    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.widget)
        layout.addWidget(self.nama)
        layout.addWidget(self.teks)
        self.setLayout(layout)

    def qss(self):
        style_sheet = """
            QDialog {
                background-color: black;
            }
            QLabel#namaLabel  {
                color: white;
                font-weight: bold;
                font-size: 18px;
            }
            QLabel#teksLabel  {
                color: white;
                font-weight: bold;
                font-size: 12px;
            }
        """
        self.setStyleSheet(style_sheet)