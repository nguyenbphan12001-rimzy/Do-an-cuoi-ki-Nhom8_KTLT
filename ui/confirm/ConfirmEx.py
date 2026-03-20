from PyQt6.QtWidgets import QMainWindow

from ui.confirm.Confirm import Ui_MainWindow
from ui.dashboard.DashboardEx import DashboardEx
import os

class ConfirmEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()

        current_dir = os.path.dirname(os.path.abspath(__file__))

        img_path = os.path.abspath(os.path.join(current_dir, "..", "..", "images", "Confirm.png")).replace("\\", "/")

        self.centralwidget.setStyleSheet(f"#centralwidget {{ border-image: url({img_path}); }}")
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
        self.MainWindow.close()
