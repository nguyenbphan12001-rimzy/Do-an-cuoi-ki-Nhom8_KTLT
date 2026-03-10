from PyQt6.QtWidgets import QApplication,QMainWindow

from project.ui.loginEx import LoginEx

app=QApplication([])
gui=LoginEx()
gui.setupUi(QMainWindow())
gui.showWindow()
app.exec()
