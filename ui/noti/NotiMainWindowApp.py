from PyQt6.QtWidgets import QApplication, QMainWindow

from ui.noti.NotiMainWindowEx import NotiMainWindowEx


app=QApplication([])
gui=NotiMainWindowEx()
my_window = QMainWindow()
gui.setupUi(my_window)
my_window.showMaximized()

app.exec()
