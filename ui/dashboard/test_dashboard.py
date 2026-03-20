from PyQt6.QtWidgets import QApplication, QMainWindow

from ui.dashboard.DashboardEx import DashboardEx

app=QApplication([])
gui = DashboardEx()
my_window = QMainWindow()
gui.setupUi(my_window)
my_window.showMaximized()
app.exec()