from PyQt6.QtWidgets import QMainWindow

from ui.confirm.Confirm import Ui_MainWindow
from ui.dashboard.DashboardEx import DashboardEx


class ConfirmEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()
    def showWindow(self):
        self.MainWindow.show()
    def setupSignalAndSlot(self):
        self.pushButtonQuayVe.clicked.connect(self.process_opendashboard)
    def process_opendashboard(self):
        self.dashboard_window=QMainWindow()
        self.dashboard_ui=DashboardEx()
        self.dashboard_ui.setupUi(self.dashboard_window)
        self.dashboard_window.showMaximized()
        self.dashboard_ui.showWindow()
