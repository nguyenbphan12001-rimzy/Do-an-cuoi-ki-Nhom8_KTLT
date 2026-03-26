from PyQt6.QtWidgets import QMainWindow
from ui.confirm.Confirm import Ui_MainWindow
import os
import sys


class ConfirmEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow

        if getattr(sys, 'frozen', False):
            self.BASE_DIR = os.path.dirname(sys.executable)
        else:
            self.BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


        self.setupSignalAndSlot()

        img_path = os.path.join(self.BASE_DIR, "images", "Confirm.png").replace("\\", "/")
        self.centralwidget.setStyleSheet(f"#centralwidget {{ border-image: url('{img_path}'); }}")

    def showWindow(self):
        self.MainWindow.show()

    def setupSignalAndSlot(self):
        self.pushButtonQuayVe.clicked.connect(self.process_opendashboard)

    def process_opendashboard(self):
        from ui.dashboard.DashboardEx import DashboardEx

        self.dashboard_window = QMainWindow()
        self.dashboard_ui = DashboardEx()
        self.dashboard_ui.setupUi(self.dashboard_window)
        self.dashboard_window.showMaximized()
        self.dashboard_ui.showWindow()
        self.MainWindow.close()