from plyer import notification

def notification_show(judul, pesan, nama, icon, toast):
    notification.notify(title=judul, message=pesan, app_name=nama, app_icon=icon, toast=toast)

notification_show('Task Reminder', 'awokawok', "asede",'image/icon.ico', False)