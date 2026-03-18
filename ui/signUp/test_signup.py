from PyQt6.QtWidgets import QApplication, QMainWindow

from ui.signUp.signUpEx import SignUpEx

app=QApplication([])
gui=SignUpEx()
my_window = QMainWindow()
gui.setupUi(my_window)
my_window.showMaximized()
app.exec()