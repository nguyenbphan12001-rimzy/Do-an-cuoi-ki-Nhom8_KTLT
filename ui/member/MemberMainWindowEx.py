import json
import os

from PyQt6.QtWidgets import QMessageBox, QMainWindow


from ui.member.MemberMainWindow import Ui_MainWindow



class MemberMainWindowEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()

        current_dir = os.path.dirname(os.path.abspath(__file__))

        img_path = os.path.abspath(os.path.join(current_dir, "..", "..", "images", "hoivien_anh(update).jpg")).replace("\\", "/")

        self.centralwidget.setStyleSheet(f"#centralwidget {{ border-image: url({img_path}); }}")
        #Không cho chỉnh sửa gói tập
        self.lineEditGoi.setReadOnly(True)
    def showWindow(self):
        self.MainWindow.show()
    def setupSignalAndSlot(self):
        self.pushButtonKhonggiahan.clicked.connect(self.process_khonggiahan)
        self.pushButtonGiahan.clicked.connect(self.process_giahan)
        # self.pushButtonChinh.clicked.connect(self.process_chinhsua)

    def process_khonggiahan(self):
        reply=QMessageBox.information(self.MainWindow,"Thông báo","Bạn đã chọn không gia hạn",QMessageBox.StandardButton.Ok)
        if reply==QMessageBox.StandardButton.Ok:
            self.showDashboard()
    def showDashboard(self):
        from ui.dashboard.DashboardEx import DashboardEx
        self.dashboard_window=QMainWindow()
        self.dashboard_ui=DashboardEx()
        self.dashboard_ui.setupUi(self.dashboard_window)
        self.dashboard_window.show()
        self.MainWindow.close()
    def process_giahan(self):
        from ui.registration.Registration_formMainWindowEx import Registration_formMainWindowEx
        self.registration_window=QMainWindow()
        self.registration_ui=Registration_formMainWindowEx()
        self.registration_ui.setupUi(self.registration_window)
        self.registration_window.show()
        self.MainWindow.close()
