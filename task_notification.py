from plyer import notification

class TaskNotification:
    def __init__(self, title, message, app_name, app_icon, timeout, task_name):
        self.title = title
        self.message = message
        self.app_name = app_name
        self.app_icon = app_icon
        self.timeout = timeout
        self.task_name = task_name
        self.instance = None

        self.show()

    def show(self):
        self.instance = notification.notify(
            title=self.title,
            message=self.message,
            app_name=self.app_name,
            app_icon=self.app_icon,
            timeout=self.timeout,
        )

    def remove(self):
        if self.instance:
            self.instance.close()