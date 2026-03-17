from ui.payment.payment import Ui_MainWindow


class PaymentEx(Ui_MainWindow):

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
    def showWindow(self):
        self.MainWindow.show()