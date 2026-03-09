from PyQt6.QtWidgets import QApplication, QMainWindow



from ui.registration.Registration_formMainWindowEx import Registration_formMainWindowEx

app=QApplication([])
gui=Registration_formMainWindowEx()
my_window = QMainWindow()
gui.setupUi(my_window)
my_window.showMaximized()

app.exec()

