from PyQt6.QtWidgets import QApplication, QMainWindow

from ui.member.MemberMainWindowEx import MemberMainWindowEx

app=QApplication([])
gui=MemberMainWindowEx()
my_window = QMainWindow()
gui.setupUi(my_window)
my_window.show()

app.exec()