import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from datetime import *
from add_task import AddTaskDialog
from database import Database
from task_notification import TaskNotification
from widgets.login import LoginWidget
from widgets.personal_task_history_dialog import PersonalTaskHistoryDialog
from widgets.developer import DeveloperDialog

class MainMenuWidget(QWidget):
    completed_task_signal = pyqtSignal()    

    def __init__(self, database, stack, parent=None):
        super().__init__()

        self.database = database
        self.notification_instance = None  # Reference to the notification object
        self.stack = stack

        # Tambahkan properti untuk menyimpan status terakhir priority dan category
        self.last_selected_priority = "Low"  # Default priority
        self.last_selected_category = ""
            
        self.welcome_label = QLabel()
        self.personal_task_tab = QWidget()
        self.personal_task_tab.setObjectName('PTab')
        self.group_workspace_tab = QWidget()

        self.setup_personal_task_tab()
        self.setup_group_workspace_tab()

        tab_widget = QTabWidget()
        tab_widget.addTab(self.personal_task_tab, 'Personal Task')
        tab_widget.addTab(self.group_workspace_tab, 'Group Workspace')

        tab_widget.setTabPosition(QTabWidget.TabPosition.North)

        menubar = QMenuBar(self)
        menubar.setObjectName('menubar') 

        # Setting Menu
        setting_menu = menubar.addMenu('Setting')

        info_action = QAction('My Info', self)
        info_action.triggered.connect(self.account_info)

        dark_mode_action = QAction('Dark Mode', self)
        # dark_mode_action.setCheckable(True)
        dark_mode_action.triggered.connect(self.toggle_dark_mode)

        reset_history_action = QAction('Reset History', self)
        reset_history_action.triggered.connect(self.reset_history)

        developer_action = QAction('Developer', self)
        developer_action.triggered.connect(self.developer_ganteng)
        
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.setting_app)
        
        # Filter Menu
        filter_menu = menubar.addMenu('Filter')

        deadline_action = QAction('Deadline', self)
        deadline_action.triggered.connect(self.filter_task)
        
        priority_action = QAction('Priority', self)
        priority_action.triggered.connect(self.filter_task)
        
        category_action = QAction('Category', self)
        category_action.triggered.connect(self.filter_task)
        
        # History Menu
        history_menu = menubar.addMenu('History')
        
        history_action = QAction('Personal Task History', self)
        history_action.triggered.connect(self.history)
        

        # Setting triggered
        setting_menu.addAction(info_action)
        setting_menu.addAction(dark_mode_action)
        setting_menu.addAction(reset_history_action)
        setting_menu.addAction(developer_action)
        setting_menu.addAction(exit_action)

        # Filter triggered
        filter_menu.addAction(deadline_action)
        filter_menu.addAction(priority_action)
        filter_menu.addAction(category_action)
        
        # History Triggered
        history_menu.addAction(history_action)


        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Adjust margins
        # layout.setSpacing(0)  # Adjust spacing
        layout.addWidget(menubar)
        layout.addWidget(self.welcome_label)
        layout.addWidget(tab_widget)
        self.setLayout(layout)

        tab_widget.setStyleSheet("""
            #PTab {
                background-color: black;
                border-radius: 15px;
            }
        """)

        menubar.setStyleSheet("""
            QMenuBar {
                max-width: 152px;
                margin: 0;
                padding: 0;
                background-color: black;
            }
            QMenuBar::item {
                color: white;
                background-color: black;    
            }
        """)

        self.task_notepad.textChanged.connect(self.update_task_note)

        self.refresh_personal_tasks()

        # Set up a QTimer to update the time remaining every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time_remaining)
        self.timer.start(1000)  # Update every 1000 milliseconds (1 second)


    def developer_ganteng(self):
        dialog = DeveloperDialog(self.database, self)
        result = dialog.exec()


    def account_info(self):
        QMessageBox.information(self, 'Information', 'Under Development')
  

    def history(self):
        dialog = PersonalTaskHistoryDialog(self.database, self)
        result = dialog.exec()


    def reset_history(self):
        history = self.database.get_completed_personal_tasks()
        confirmation = QMessageBox.question(
            self, 'Confirmation', 'Are you sure want to reset history?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirmation == QMessageBox.StandardButton.Yes:
            if history:
                self.database.reset_history()
                QMessageBox.information(self, 'Information', 'History reset complete')
            else:
                QMessageBox.warning(self, 'Warning', 'History is already empty')
            
        else:
            QMessageBox.warning(self, 'Warning', 'Reset history cancelled')                

        
    def toggle_dark_mode(self):
        QMessageBox.information(self, 'Information', 'Under Development')
          

    def setting_app(self):
        confirmation = QMessageBox.question(
            self, 'Confirmation', 'Are you sure you want to exit?', 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirmation == QMessageBox.StandardButton.Yes:
            # If the user confirms, hide the current widget (MainMenuWidget)
            self.hide()
            self.stack.setCurrentIndex(0)


    def filter_task(self):
        action = self.sender()
        if action is None or not isinstance(action, QAction):
            return

        filter_type = action.text()  # Get the text of the selected QAction

        if filter_type == 'Deadline':
            # Get the list of personal tasks
            personal_tasks = self.database.get_personal_tasks()

            # Sort tasks by deadline (time remaining)
            personal_tasks.sort(key=lambda task: self.calculate_time_remaining(task))

            # Display the sequential task list in a message box
            task_list_text = "\n".join(personal_tasks)
            QMessageBox.information(self, 'Sequential Task List', f'Sequential Task List based on Deadline:\n\n{task_list_text}')

        if filter_type == 'Priority':
            # Get the list of personal tasks
            personal_tasks = self.database.get_personal_tasks()

            # Sort tasks by priority level
            personal_tasks.sort(key=lambda task: self.get_priority_level(task), reverse=True)

            # Display the sorted task list in a message box
            task_list_text = "\n".join(personal_tasks)
            QMessageBox.information(self, 'Sorted Task List by Priority', f'Sorted Task List based on Priority:\n\n{task_list_text}')

        if filter_type == 'Category':
            # Get the list of personal tasks
            personal_tasks = self.database.get_personal_tasks()

            # Group tasks by category
            category_groups = {}
            for task_name in personal_tasks:
                category = self.database.get_task_category(task_name)
                if category not in category_groups:
                    category_groups[category] = []
                category_groups[category].append(task_name)

            # Tampilkan grup task information di message box
            category_info = "\n".join([f"{category}: {', '.join(tasks)}" for category, tasks in category_groups.items()])
            QMessageBox.information(self, 'Task List Grouped by Category', f'Task List Grouped by Category:\n\n{category_info}')

    def get_priority_level(self, task_name):
        # Get the priority level from the database
        priority_level = self.database.get_task_priority(task_name)

        # Return a numeric value based on the priority level (higher value for higher priority)
        priority_mapping = {"Low": 0, "Medium": 1, "High": 2}
        return priority_mapping.get(priority_level, -1)  # Default to -1 if priority level is not recognized

    def calculate_time_remaining(self, task_name):
        # Get the task details from the database
        task_details = self.database.get_task_details(task_name)

        if task_details is not None:
            task_name, task_datetime = task_details

            task_datetime_obj = datetime.strptime(task_datetime, "%Y-%m-%d %H:%M:%S")
            time_remaining = task_datetime_obj - datetime.now()

            # Return the total seconds as a key for sorting
            return time_remaining.total_seconds()

        return float('inf')  # Return a large value for tasks without valid details


    def update_time_remaining(self):
        selected_items = self.personal_task_table.selectedItems()
        if selected_items:
            selected_task = selected_items[0].text()
            task_details = self.database.get_task_details(selected_task)

            if task_details is not None:
                task_name, task_datetime = task_details

                task_datetime_obj = datetime.strptime(task_datetime, "%Y-%m-%d %H:%M:%S")
                time_remaining = task_datetime_obj - datetime.now()

                # Only set the color to red if the task is overdue
                time_remaining_color = '<font color="red">' if time_remaining.total_seconds() < 0 else '<font color="white">'

                days, seconds = time_remaining.days, time_remaining.seconds
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                seconds = seconds % 60

                time_remaining_str = f"\nWaktu Tersisa: {days} hari, {hours} jam, {minutes} menit, {seconds} detik"
                time_remaining_str = f"{time_remaining_color}{time_remaining_str}</font>"


                task_details_text = f"<h1>{task_name}</h1>\nTanggal dan Waktu Tugas: {task_datetime}"
                task_details_text += f"<br>{time_remaining_str}"

                self.task_details_label.setText(task_details_text)

                # Check if the task is overdue and show notification
                if time_remaining.total_seconds() < 0 and AddTaskDialog.toggle_notification_controls(self, task_name):
                    show_notif = AddTaskDialog.show_notification(self, task_name)     
                            
        else:
            # Clear the displayed information if no task is selected
            self.clear_task_details()


    def update_task_note_display(self):
        selected_items = self.personal_task_table.selectedItems()
        if selected_items:
            selected_task = selected_items[0].text()
            note = self.database.get_task_note(selected_task)
            self.task_notepad.setPlainText(note)


    def update_task_note(self):
        selected_items = self.personal_task_table.selectedItems()
        if selected_items:
            selected_task = selected_items[0].text()
            note = self.task_notepad.toPlainText()
            self.database.set_task_note(selected_task, note)
            self.database.commit_changes()
            self.personal_task_table.itemSelectionChanged.connect(self.update_task_note_display)


    def set_welcome_message(self, nickname):
        self.welcome_label.setText(f"<h3>Welcome {nickname}!</h3>")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        

    def setup_personal_task_tab(self):
        
        personal_task_layout = QVBoxLayout()

        splitter = QSplitter(Qt.Orientation.Horizontal)  # Membuat splitter horizontal
        splitter.setStyleSheet('background-color: black;')        
        # QTableWidget buat List Task
        self.personal_task_table = QTableWidget(self)
        self.personal_task_table.setStyleSheet('background-color: transparent;')
        self.personal_task_table.setObjectName('tableWidget')
        self.personal_task_table.setColumnCount(1)
        self.personal_task_table.setHorizontalHeaderLabels(["Task Name"])
        self.personal_task_table.horizontalHeader().setStretchLastSection(True)
        self.personal_task_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.personal_task_table.itemClicked.connect(self.show_task_details)

        # Widget buat Task Details
        task_details_widget = QWidget(self)
        task_details_layout = QVBoxLayout()

        # Widget buat Task Details
        task_details_widget = QWidget(self)
        task_details_layout = QVBoxLayout()

        task_details_label = QLabel("<h2>Task Details</h2>")
        task_details_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        task_details_label.setStyleSheet("font-weight: bold; color: white;")
        
        self.task_details_label = QLabel()  # update label di task details
        self.task_details_label.setStyleSheet('color: white;')

        self.task_notepad = QTextEdit() # Notepad
        self.task_notepad = CleanPasteTextEdit()
        self.task_notepad.setStyleSheet("QTextEdit { color: white; border-radius: 10px; border-style: solid; border-width: 4px; border-color: white; border-radius: 10px; padding: 4px, 4px, 4px, 4px;} QTextEdit:hover {border-color: blue;}")
        self.task_notepad.setObjectName('noteObject')
        self.task_notepad.setPlaceholderText('Masukan Catatan')

        self.complete_task_button = QPushButton('Task Complete')
        self.complete_task_button.setObjectName('completeButton')
        self.complete_task_button.setFixedWidth(200)
        self.complete_task_button.setFixedHeight(30)
        self.complete_task_button.clicked.connect(self.complete_task)

        self.category_button = QPushButton('Category', self)
        self.category_button.setObjectName('categoryButton')
        self.category_button.setFixedWidth(200)
        self.category_button.setFixedHeight(30)
        self.category_button.clicked.connect(self.show_category_menu)

        self.priority_button = QPushButton('Priority', self)
        self.priority_button.setObjectName('priorityButton')
        self.priority_button.setFixedWidth(200)
        self.priority_button.setFixedHeight(30)
        self.priority_button.clicked.connect(self.show_priority_menu)

        # Buat menu prioritas dan tambahkan aksi
        self.priority_menu = QMenu(self)
        low_priority_action = self.priority_menu.addAction("Low Priority")
        medium_priority_action = self.priority_menu.addAction("Medium Priority")
        high_priority_action = self.priority_menu.addAction("High Priority")

        low_priority_action.triggered.connect(lambda: self.set_priority("Low"))
        medium_priority_action.triggered.connect(lambda: self.set_priority("Medium"))
        high_priority_action.triggered.connect(lambda: self.set_priority("High"))

        task_details_layout.addWidget(task_details_label)
        task_details_layout.addWidget(self.task_details_label)
        task_details_layout.addWidget(self.task_notepad)
        task_details_layout.addWidget(self.priority_button)
        task_details_layout.addWidget(self.category_button)
        task_details_layout.addWidget(self.complete_task_button)
        task_details_layout.setContentsMargins(50, 0, 50, 25)

        task_details_widget.setLayout(task_details_layout)

        splitter.addWidget(self.personal_task_table)
        splitter.addWidget(task_details_widget)

        splitter.setSizes([400, 900])  # Menetapkan lebar awal untuk List Task dan Task Details)
 
        add_task_button = QPushButton('Add Task')
        add_task_button.setShortcut(QKeySequence(Qt.Key.Key_Tab))
        add_task_button.setObjectName('addButton')
        # add_task_button.setFixedWidth(300)
        add_task_button.setFixedHeight(30)
        add_task_button.clicked.connect(self.show_add_task_dialog)

        personal_task_layout.addWidget(splitter)
        personal_task_layout.addWidget(add_task_button)

        self.personal_task_tab.setLayout(personal_task_layout)
        
        # Sembunyikan Notepad dan tombol Task Complete saat menambahkan tugas baru
        # self.task_notepad.setVisible(False)
        # self.complete_task_button.setVisible(False)
        # self.priority_button.setVisible(False)


        self.setStyleSheet("""
        
                        
        #tableWidget {
            color: white;
            border-style: solid;
            border-width: 5px;
            border-color: white;
            border-radius: 1px;
            font-weight: bold;
            margin-left: 15px;
            margin-top: 20px;
            margin-bottom: 20px;
            margin-right: 15px;
        }
        #tableWidget:hover {
            border-color: blue;
        }
        #completeButton, #priorityButton, #categoryButton {
            color: white;
            background-color: transparent;
            border-style: solid;
            border-width: 3px;
            border-color: white;
            border-radius: 10px;
            font-weight: bold;
        }
        #completeButton:hover, #priorityButton:hover, #categoryButton:hover {
            color: blue;
            background-color: black;
            border-color: blue;
            border-radius: 10px;
            font-weight: bold;
        }
        #addButton {
            color: white;
            border-style: solid;
            border-color: white;
            border-width: 3px;
            border-radius: 10px;
            background-color: transparent;
            font-weight: bold;
        }
        #addButton:hover {
            color: black;
            background-color: blue;
            border-radius: 10px;
            font-weight: bold;
        }
        #addButton:pressed {
            color: red;
            background-color: blue;
            border-radius: 10px;
            font-weight: bold;
        }
    """)
        self.update()


    def set_last_selected_priority(self, priority):
        self.last_selected_priority = priority

    def set_last_selected_category(self, category):
        self.last_selected_category = category


    def show_category_menu(self):
        menu = QMenu(self)
        # Tambahkan beberapa kategori atau tambahkan logika untuk mendapatkan kategori dari database
        work_category_action = menu.addAction('Work')
        personal_category_action = menu.addAction('Personal')
        study_category_action = menu.addAction('Study')
        # Jika ingin menambahkan kategori lain secara manual, tambahkan QAction dan sambungkan ke metode yang sesuai
        add_category_action = menu.addAction('Add Category...')

        # Menghubungkan setiap aksi dengan metode untuk menetapkan prioritas
        work_category_action.triggered.connect(lambda: self.set_category(0))
        personal_category_action.triggered.connect(lambda: self.set_category(1))
        study_category_action.triggered.connect(lambda: self.set_category(2))
        add_category_action.triggered.connect(lambda: self.set_category('Add Category'))
        
        # Set checked state based on last selected category
        for action in menu.actions():
            if action.text() == self.last_selected_category:
                action.setChecked(True)

        # Save references to priority actions for later access
        self.work_category_action = work_category_action
        self.personal_category_action = personal_category_action
        self.study_category_action = study_category_action
        self.add_category_action = add_category_action

        # Menampilkan menu di sebelah tombol kategori
        position = self.category_button.mapToGlobal(self.category_button.rect().bottomLeft())
        menu.exec(position)


    def set_category(self, category):
        # Reset all category actions to unchecked
        self.work_category_action.setChecked(False)
        self.personal_category_action.setChecked(False)
        self.study_category_action.setChecked(False)
        self.add_category_action.setChecked(False)

        # Initialize category_str
        category_str = ""

        # Set the selected category action to checked
        if category == 0:
            self.work_category_action.setChecked(True)
            category_str = "Work"
        elif category == 1:
            self.personal_category_action.setChecked(True)
            category_str = "Personal"
        elif category == 2:
            self.study_category_action.setChecked(True)
            category_str = "Study"
        elif category == 'Add Category':
            self.add_category_action.setChecked(True)

        # Convert integer category to string representation
        category_mapping = {0: "Work", 1: "Personal", 2: "Study"}

        if category in category_mapping.values():
            # Existing category selected
            category_str = category
        elif category == 'Add Category':
            # Handle the case where the user wants to add a new category
            category_str, ok_pressed = QInputDialog.getText(self, "Add Category", "Enter new category:")
            if not ok_pressed or not category_str:
                # If the user cancels or doesn't enter a category, set to an empty string
                category_str = ""
            else:
                # Save the new category to the database or perform any other necessary actions
                # Add the new category to the category_mapping if needed
                category_mapping[len(category_mapping)] = category_str

        # Set the selected category and update the text of the category button
        self.selected_category = category_str
        self.category_button.setText(f'Category: {self.selected_category}')

        # Update the database if a task is selected
        selected_items = self.personal_task_table.selectedItems()
        if selected_items:
            selected_task = selected_items[0].text()
            self.database.set_task_category(selected_task, category_str)
            self.database.commit_changes()

        # Update the view of the remaining time
        self.update_time_remaining()

        # Simpan status terakhir
        self.set_last_selected_category(category_str)


    def show_priority_menu(self):
        menu = QMenu(self)
        low_priority_action = menu.addAction('Low Priority')
        medium_priority_action = menu.addAction('Medium Priority')
        high_priority_action = menu.addAction('High Priority')

        # Menghubungkan setiap aksi dengan metode untuk menetapkan prioritas
        low_priority_action.triggered.connect(lambda: self.set_priority(0))
        medium_priority_action.triggered.connect(lambda: self.set_priority(1))
        high_priority_action.triggered.connect(lambda: self.set_priority(2))

        # Set checked state based on last selected priority
        for action in menu.actions():
            if action.text() == self.last_selected_priority:
                action.setChecked(True)

        # Save references to priority actions for later access
        self.low_priority_action = low_priority_action
        self.medium_priority_action = medium_priority_action
        self.high_priority_action = high_priority_action

        # Menampilkan menu di sebelah tombol prioritas
        position = self.priority_button.mapToGlobal(self.priority_button.rect().bottomLeft())
        menu.exec(position)


    def set_priority(self, priority):
        # Reset all priority actions to unchecked
        self.low_priority_action.setChecked(False)
        self.medium_priority_action.setChecked(False)
        self.high_priority_action.setChecked(False)

        # Set the selected priority action to checked
        if priority == 0:
            self.low_priority_action.setChecked(True)
        elif priority == 1:
            self.medium_priority_action.setChecked(True)
        elif priority == 2:
            self.high_priority_action.setChecked(True)

        # Convert integer priority to string representation
        priority_mapping = {0: "Low", 1: "Medium", 2: "High"}
        priority_str = priority_mapping.get(priority, "Low")  # Default to "Low" if not found

        # Set the priority property in the class
        self.selected_priority = priority_str

         # Update the text of the priority button
        self.priority_button.setText(f'Priority: {priority_str}')

        # Update the priority in the database if a task is selected
        selected_items = self.personal_task_table.selectedItems()
        if selected_items:
            selected_task = selected_items[0].text()
            self.database.set_task_priority(selected_task, priority_str)
            self.database.commit_changes()

            # Update the view of the remaining time
            self.update_time_remaining()

        # Simpan status terakhir
        self.set_last_selected_priority(priority_str)

    def complete_task(self):
        selected_items = self.personal_task_table.selectedItems()
        if selected_items:
            selected_task = selected_items[0].text()
            task_details = self.database.get_task_details(selected_task)
            
            # Get the note from the notepad
            note = self.task_notepad.toPlainText()

            # Update the note in the database
            self.database.set_task_note(selected_task, note)
            
            if task_details is not None:
                task_name, task_datetime = task_details
                priority = getattr(self, 'selected_priority', "Low")  # Default: Low
                category = self.selected_category if hasattr(self, 'selected_category') else ""


                # Move the task to history
                self.database.move_to_history_table(task_name, task_datetime, note, priority, category)
                self.completed_task_signal.emit()  # Emit signal when a task is completed
                # print("Complete task:", task_name, task_datetime, note, priority, category)  # Tambahkan pernyataan cetak di sini

                # Remove the task from personal tasks
                self.database.remove_personal_task(selected_task)
                self.refresh_personal_tasks()
                self.clear_task_details()
                
                # Update the task status in the database
                self.database.get_completed_personal_tasks()
                self.database.commit_changes()

                # Stop the notification when the task is complete
                if hasattr(self, 'notification_instance') and self.notification_instance:
                    self.notification_instance.remove()
        #     else:
        #         print(f"Task details for '{selected_task}' not found.")
        # else:
        #     print("No task selected to complete.")


    def refresh_personal_tasks(self):
        tasks = self.database.get_personal_tasks()
        
        # Clear existing rows in the table
        self.personal_task_table.setRowCount(0)

        # Populate the table with tasks
        for row, task in enumerate(tasks):
            task_item = QTableWidgetItem(task)
            task_item.setFlags(task_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make the item non-editable
            self.personal_task_table.insertRow(row)
            self.personal_task_table.setItem(row, 0, task_item)


    def show_add_task_dialog(self):
        dialog = AddTaskDialog(self.database, self)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            task_name, task_datetime = dialog.get_task_details()  # No priority returned
            priority = "Low"  # Default priority for new tasks
            category = ""

            self.database.add_personal_task(task_name, task_datetime, priority, category)
            self.database.commit_changes()
            self.refresh_personal_tasks()


    def show_task_details(self, item):
        selected_task = item.text()
        task_details = self.database.get_task_details(selected_task)

        if task_details is not None:
            task_name, task_datetime = task_details

            task_details_text = f"<h1>{task_name}</h1>\nTanggal dan Waktu Tugas: {task_datetime}"

            # Set the initial text without time remaining (will be updated by the timer)
            self.task_details_label.setText(task_details_text)
            
            # Show notepad and completion button only if item is selected
            if item.isSelected():
                self.task_notepad.setVisible(True)
                note = self.database.get_task_note(selected_task)
                self.task_notepad.setPlainText(note)
                self.priority_button.setVisible(True)
                self.category_button.setVisible(True)
                self.complete_task_button.setVisible(True)
            else:
                self.task_notepad.setVisible(False)
                self.priority_button.setVisible(False)
                self.category_button.setVisible(False)
                self.complete_task_button.setVisible(False)
        # else:
        #     # print(f"Task details for '{selected_task}' not found.")

        # Start the timer when a task is selected
        self.timer.start(1000)
    

    def clear_task_details(self):
        # hapusinformasi di Task Details
        self.task_details_label.clear()
        self.task_notepad.clear()
        self.task_notepad.setVisible(False)
        self.priority_button.setVisible(False)
        self.category_button.setVisible(False)
        self.complete_task_button.setVisible(False)
        # Stop the timer when no task is selected
        self.timer.stop()


    def setup_group_workspace_tab(self):
        group_workspace_layout = QVBoxLayout()

        label = QLabel('Upgrade to Premium to access this feature!')
        # add_workspace_button = QPushButton('Add Workspace')

        group_workspace_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter)
        # group_workspace_layout.addWidget(add_workspace_button)

        self.group_workspace_tab.setLayout(group_workspace_layout)


class CleanPasteTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptRichText(False)

    def insertFromMimeData(self, source):
        if source.hasText():
            cleaned_text = source.text().strip()
            cursor = self.textCursor()
            cursor.insertText(cleaned_text)
            self.setTextCursor(cursor)
        else:
            super().insertFromMimeData(source)