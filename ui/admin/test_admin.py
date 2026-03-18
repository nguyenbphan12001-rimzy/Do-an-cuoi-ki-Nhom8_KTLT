from PyQt6.QtWidgets import QApplication, QMainWindow

from ui.admin.adminEx import AdminEx

app=QApplication([])
gui=AdminEx()
my_window = QMainWindow()
gui.setupUi(my_window)
my_window.show()
# my_window.showMaximized()
app.exec()