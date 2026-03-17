
from PyQt6.QtWidgets import QMainWindow

from ui.admin.adminEx import AdminEx
from ui.booking.BookingMainWindowEx import BookingMainWindowEx
from ui.dashboard.Dashboard import Ui_MainWindow

import os

from ui.member.MemberMainWindowEx import MemberMainWindowEx
from ui.registration.Registration_formMainWindowEx import Registration_formMainWindowEx


class DashboardEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()

        current_dir = os.path.dirname(os.path.abspath(__file__))

        img_path = os.path.abspath(os.path.join(current_dir, "..", "..", "images", "Dashboard.png")).replace("\\", "/")

        self.centralwidget.setStyleSheet(f"#centralwidget {{ border-image: url({img_path}); }}")
    def showWindow(self):
        self.MainWindow.show()
    def setupSignalAndSlot(self):
        self.pushButtonDatlich.clicked.connect(self.process_booking)
        self.pushButtonDkyHoivien.clicked.connect(self.process_dkyhoivien)
        self.pushButtonAdmin.clicked.connect(self.process_admin)
        self.pushButtonLogOut.clicked.connect(self.process_logout)
        self.pushButtonMember.clicked.connect(self.process_member)
    def process_booking(self):
        self.booking_window=QMainWindow()
        self.booking_ui=BookingMainWindowEx()
        self.booking_ui.setupUi(self.booking_window)
        self.booking_window.showMaximized()
        self.booking_ui.showWindow()
    def process_dkyhoivien(self):
        self.hoivien_window = QMainWindow()
        self.hoivien_ui = Registration_formMainWindowEx()
        self.hoivien_ui.setupUi(self.hoivien_window)
        self.hoivien_window.showMaximized()
        self.hoivien_ui.showWindow()
    def process_member(self):
        self.member_window = QMainWindow()
        self.member_ui = MemberMainWindowEx()
        self.member_ui.setupUi(self.member_window)
        self.member_window.showMaximized()
        self.member_ui.showWindow()
    def process_admin(self):
        self.admin_window=QMainWindow()
        self.admin_ui=AdminEx()
        self.admin_ui.setupUi(self.admin_window)
        self.admin_window.showMaximized()
        self.admin_ui.showWindow()
    def process_logout(self):
        from ui.home.HomeEx import HomeEx  # import trong function
        self.logout_window=QMainWindow()
        self.logout_ui=HomeEx()
        self.logout_ui.setupUi(self.logout_window)
        self.logout_window.showMaximized()
        self.logout_ui.showWindow()
