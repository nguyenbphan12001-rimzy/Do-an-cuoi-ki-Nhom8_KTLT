from PyQt6.QtWidgets import QApplication, QMainWindow

from ui.home.HomeEx import HomeEx

app=QApplication([])
gui=HomeEx()
my_window = QMainWindow()
gui.setupUi(my_window)
my_window.showMaximized()
app.exec()