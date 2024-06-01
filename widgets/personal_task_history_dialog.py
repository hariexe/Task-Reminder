from widgets.main_menu import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from database import Database

class PersonalTaskHistoryDialog(QDialog):
    completed_task_signal = pyqtSignal()

    def __init__(self, database, parent=None):
        super().__init__(parent)
        self.database = database

        self.setWindowTitle("Personal Task History")
        self.setMinimumWidth(400)
        self.setMinimumHeight(450)

        self.task_list_widget = QListWidget(self)
        self.setup_ui()

        # Add debug prints
        # print("Connecting signal to slot")
        self.completed_task_signal.connect(self.update_task_list)
        self.completed_task_signal.emit()
        # print("Signal connected successfully")


    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.task_list_widget)
        self.setLayout(layout)
        # Where you want to emit the signal (for example, in a method of some class)


    def update_task_list(self):
        # print("Update Task List Called.")
        # Retrieve completed tasks from the database
        completed_tasks = self.database.get_completed_personal_tasks()

        # Update the task list widget
        self.task_list_widget.clear()
        for task_details in completed_tasks:
            task_text = ", ".join(map(str, task_details))  # Combine all fields with " - " separator
            item = QListWidgetItem(task_text)
            self.task_list_widget.addItem(item)