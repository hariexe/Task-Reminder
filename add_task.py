from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from database import Database
from task_notification import TaskNotification

class AddTaskDialog(QDialog):
    def __init__(self, database, parent=None):
        super().__init__(parent)

        self.database = database

        self.setWindowTitle('Add Task')
        # self.setMinimumSize(400, 400)

        self.task_name_edit = QLineEdit(self)
        self.task_datetime_edit = QDateTimeEdit(self)
        self.task_datetime_edit.setCalendarPopup(True)

        # Atur waktu minimum 3 menit kedepan
        min_datetime = QDateTime.currentDateTime().addSecs(10)
        self.task_datetime_edit.setMinimumDateTime(min_datetime)

        self.notification_checkbox = QCheckBox('Enable Notification', self)
        self.notification_checkbox.setChecked(True)

        add_button = QPushButton('Add Task')
        add_button.setObjectName('addbtn')
        add_button.clicked.connect(self.validate_and_accept)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('Task Name:'))
        layout.addWidget(self.task_name_edit)
        layout.addWidget(QLabel('Reminder Date and Time:'))
        layout.addWidget(self.task_datetime_edit)
        layout.addWidget(self.notification_checkbox)
        layout.addWidget(add_button)

        self.setLayout(layout)

#         self.setStyleSheet("""
#             QDialog {
#                 background-color: blue;
#             }
#             #addbtn {
#                 color: white;
#                 background-color: black;
#             }
#             QPushButton {
#                 color: white;
#                 font-weight: bold;
#                 background-color: transparent;
#                 border-style: solid;
#                 border-radius: 10px;
#                 border-color: white;
#                 border-width: 3px;
#             }
# """)

        self.notification_checkbox.stateChanged.connect(self.toggle_notification_controls)

    def toggle_notification_controls(self, state):
        # Enable or disable controls related to notification based on the checkbox state
        is_enabled = state == Qt.CheckState.Checked
        # Additional controls can be added here if needed
        # For example, you might want to enable/disable a field for custom notification message
        # self.custom_message_edit.setEnabled(is_enabled)

    def validate_and_accept(self):
        task_name = self.task_name_edit.text().strip()

        if not task_name:
            QMessageBox.warning(self, 'Error', 'Task Name cannot be empty.')
        elif self.task_exists(task_name):
            QMessageBox.warning(self, 'Error', 'Task with the same name already exists.')
        else:
            task_datetime = self.task_datetime_edit.dateTime().toPyDateTime()
            now = QDateTime.currentDateTime().toPyDateTime()

            if task_datetime <= now:
                QMessageBox.warning(self, 'Error', 'Reminder datetime should be in the future.')
            else:
                enable_notification = self.notification_checkbox.isChecked()

                if enable_notification:
                    self.schedule_notification(task_name, task_datetime)

                self.accept()

    def task_exists(self, task_name):
        # Periksa ketika nama sudah ada dalam database
        return task_name in self.database.get_personal_tasks()

    def schedule_notification(self, task_name, task_datetime):
        # Menghitung selisih waktu
        time_difference = task_datetime - QDateTime.currentDateTime().toPyDateTime()

        # konversi waktu ke detik
        seconds_until_notification = time_difference.total_seconds()

        # Jadwal notifikasi pake QTimer
        self.notification_timer = QTimer(self)
        self.notification_timer.timeout.connect(lambda: self.show_notification(task_name))
        self.notification_timer.start(int(seconds_until_notification * 1000))  # QTimer works with milliseconds

    def show_notification(self, task_name):
        # # Only show notification if there is no existing notification for the task
        # existing_notification = getattr(self, 'notification_instance', None)
        # if existing_notification and existing_notification.task_name == task_name:
        #     return  # Skip showing the notification if it already exists for the same task

        # # Remove existing notification if any
        # if existing_notification:
        #     existing_notification.remove()

        # # Show new notification
        # self.notification_instance = TaskNotification(
        #     title='Task Reminder',
        #     message=f"It's time to complete the task: {task_name}",
        #     app_name='Tasker',
        #     app_icon='image/icon.ico',
        #     timeout=10,  # seconds
        #     task_name=task_name,
        # )
        QMessageBox.information(self, 'Task Reminder', f"It's time to complete the task: {task_name}")


    def get_task_details(self):
        task_name = self.task_name_edit.text()
        task_datetime = self.task_datetime_edit.dateTime().toString('yyyy-MM-dd HH:mm:ss')
        return task_name, task_datetime