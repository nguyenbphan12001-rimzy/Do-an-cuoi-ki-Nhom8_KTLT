from PyQt6.QtWidgets import QApplication, QMainWindow

from ui.confirm.ConfirmEx import ConfirmEx

app=QApplication([])
gui=ConfirmEx()
my_window = QMainWindow()
gui.setupUi(my_window)
my_window.showMaximized()
app.exec()