from PyQt6.QtWidgets import QApplication, QMainWindow

from ui.payment.paymentEx import PaymentEx

app=QApplication([])
gui=PaymentEx()
my_window = QMainWindow()
gui.setupUi(my_window)
my_window.showMaximized()

app.exec()