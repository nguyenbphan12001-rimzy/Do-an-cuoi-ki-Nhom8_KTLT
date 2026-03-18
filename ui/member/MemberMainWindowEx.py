from datetime import datetime
import os

from PyQt6.QtWidgets import QMessageBox, QMainWindow

from models.members import Members
from ui.member.MemberMainWindow import Ui_MainWindow



class MemberMainWindowEx(Ui_MainWindow):
    def __init__(self,member=None):
        self.member=member
        file_member="../../Datasets/member.json"
        self.mb=Members()
        self.mb.import_json(file_member)
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()
        self.load_member()

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

    def load_member(self):
        if not self.member:
            return
        self.lineEditName.setText(self.member.name)
        self.lineEditID.setText(self.member.id)
        self.lineEditPhone.setText(self.member.phone)
        self.lineEditGender.setText(self.member.gender)
        self.lineEditGoi.setText(self.member.goi)
        #xử lý trạng thái
        today=datetime.today().date()
        expire_date=self.member.expire_date
        if isinstance(expire_date,str):
            expire_date=datetime.strptime(expire_date,"%d/%m/%Y").date()
        if expire_date>=today:
            self.lineEditStatus.setText("CÒN HẠN")
            self.lineEditStatus.setStyleSheet("color:green;font-weight:bold;")
        else:
            self.lineEditStatus.setText("HẾT HẠN")
            self.lineEditStatus.setStyleSheet("color:red;font-weight:bold;")
