import os

from PyQt6.QtWidgets import QMainWindow

from ui.booking.booking import Ui_MainWindow


class BookingMainWindowEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        # self.pushButtonDoneBooking.clicked.connect(self.process_booking)


    def showWindow(self):
        self.MainWindow.show()

    # def process_booking(self):
    #     self.MainWindow.close()
    #     self.mainwindow = QMainWindow()
    #     self.ui = PaymentEx()
    #     self.ui.setupUi(self.mainwindow)
    #     self.ui.showWindow()

