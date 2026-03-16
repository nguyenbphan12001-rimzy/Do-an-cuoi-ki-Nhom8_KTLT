from PyQt6.QtMultimedia import QWindowCapture
from PyQt6.QtWidgets import QMainWindow

from ui.admin.adminEx import AdminEx
from ui.booking.BookingMainWindowEx import BookingMainWindowEx
from ui.dashboard.Dashboard import Ui_MainWindow
from ui.home.HomeEx import HomeEx
from ui.member.MemberMainWindowEx import MemberMainWindowEx


class DashboardEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()
    def showWindow(self):
        self.MainWindow.show()
    def setupSignalAndSlot(self):
        self.pushButtonDatlich.clicked.connect(self.process_booking)
        self.pushButtonDkyHoivien.clicked.connect(self.process_hoivien)
        self.pushButtonAdmin.clicked.connect(self.process_admin)
        self.pushButtonLogOut.clicked.connect(self.process_logout)
    def process_booking(self):
        self.booking_window=QMainWindow()
        self.booking_ui=BookingMainWindowEx()
        self.booking_ui.setupUi(self.booking_window)
        self.booking_window.showMaximized()
        self.booking_ui.showWindow()
    def process_hoivien(self):
        self.hoivien_window = QMainWindow()
        self.hoivien_ui = MemberMainWindowEx()
        self.hoivien_ui.setupUi(self.hoivien_window)
        self.hoivien_window.showMaximized()
        self.hoivien_ui.showWindow()
    def process_admin(self):
        self.admin_window=QMainWindow()
        self.admin_ui=AdminEx()
        self.admin_ui.setupUi(self.admin_window)
        self.admin_window.showMaximized()
        self.admin_ui.showWindow()
    def process_logout(self):
        self.logout_window=QMainWindow()
        self.logout_ui=HomeEx()
        self.logout_ui.setupUi(self.logout_window)
        self.logout_window.showMaximized()
        self.logout_ui.showWindow()