from PyQt6.QtWidgets import QApplication,QMainWindow

from ui.booking.BookingMainWindowEx import BookingMainWindowEx

app=QApplication([])
gui=BookingMainWindowEx()
my_window = QMainWindow()
gui.setupUi(my_window)
my_window.showMaximized()

# gui.showWindow()

app.exec()
