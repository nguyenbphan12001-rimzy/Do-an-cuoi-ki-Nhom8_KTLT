from datetime import datetime
import os

from PyQt6.QtWidgets import QMessageBox, QMainWindow

from models.members import Members
from ui.member.MemberMainWindow import Ui_MainWindow



class MemberMainWindowEx(Ui_MainWindow):
    def __init__(self,member=None):
        super().__init__()
        file_member="../../Datasets/member.json"
        self.mb=Members()
        self.mb.import_json(file_member)
        self.current_user=None #Nhận dữ liệu từ dashboard
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
        self.pushButtonChinh.clicked.connect(self.process_chinhsua)
        self.pushButtonBack.clicked.connect(self.showDashboard)

    def process_khonggiahan(self):
        reply=QMessageBox.information(self.MainWindow,"Thông báo","Bạn đã chọn không gia hạn",QMessageBox.StandardButton.Ok)
        if reply==QMessageBox.StandardButton.Ok:
            self.showDashboard()
    def showDashboard(self):
        from ui.dashboard.DashboardEx import DashboardEx
        self.dashboard_window=QMainWindow()
        self.dashboard_ui=DashboardEx()
        self.dashboard_ui.setupUi(self.dashboard_window)
        self.dashboard_ui.current_user=self.current_user
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
        if not self.current_user:
            return
        username = self.current_user.get("username")
        member = None
        for m in self.mb.list:
            if m.username == username:
                member = m
                break
        if not member:
            QMessageBox.warning(self.MainWindow, "Thông báo", "Bạn chưa đăng ký hội viên!")
            return
        self.member=member
        self.lineEditName.setText(member.username)
        self.lineEditPhone.setText(member.phone_number)
        self.lineEditGoi.setText(member.package)
        if member.gender=="M":
            self.radioButtonMale.setChecked(True)
        else:
            self.radioButtonFemale.setChecked(True)
        #Khóa lại
        self.radioButtonMale.setEnabled(False)
        self.radioButtonFemale.setEnabled(False)
        #Trạng thái gói tập
        today = datetime.today().date()
        expire_date = member.expire_date
        if isinstance(expire_date, str):
            expire_date = datetime.strptime(expire_date, "%d/%m/%Y").date()
        if expire_date >= today:
            self.pushButtonConhan.setEnabled(True)
            self.pushButtonHethan.setEnabled(False)
            self.pushButtonConhan.setStyleSheet("""
            background-color: rgb(78,170,28);
            color: white;
            font-weight: bold;
            border-radius:10px;
        """)
            self.pushButtonHethan.setStyleSheet("""
                background-color: lightgray;
                color: gray;
                border-radius:10px;
            """)
        else:
            self.pushButtonConhan.setEnabled(False)
            self.pushButtonHethan.setEnabled(True)
            self.pushButtonConhan.setStyleSheet("""
                       background-color: lightgray;
                       color: gray;
                       border-radius:10px;
                   """)
            self.pushButtonHethan.setStyleSheet("""
                       background-color: rgb(255,138,138);
                       color: white;
                       font-weight: bold;
                       border-radius:10px;
                   """)
    def process_chinhsua(self):
        #Cho phép chỉnh sửa
        self.lineEditName.setReadOnly(False)
        self.lineEditPhone.setReadOnly(False)
        self.radioButtonMale.setEnabled(True)
        self.radioButtonFemale.setEnabled(True)
        #Đổi thành nút lưu
        self.pushButtonChinh.setText("SAVE")
        try:
            self.pushButtonChinh.clicked.disconnect()
        except:
            pass
        self.pushButtonChinh.clicked.connect(self.save_changes)
    #Thêm chuc năng lưu
    def save_changes(self):
        name=self.lineEditName.text()
        phone=self.lineEditPhone.text()
        if self.radioButtonMale.isChecked():
            gender="M"
        else:
            gender="F"
        old_username=self.current_user.get("username")
        member=None
        for m in self.mb.list:
            if m.username==old_username:
                member=m
                break
        if not member:
            QMessageBox.warning(self.MainWindow,"Lỗi","Không tìm thấy hội viên!")
            return
        #Cập nhật dữ liệu
        member.username=name
        member.phone_number=phone
        member.gender=gender
        #lưu lại json
        self.mb.export_json("../../Datasets/member.json")

        QMessageBox.information(self.MainWindow,"Thành công","Cập nhật thông tin thành công!")
        self.lineEditName.setReadOnly(True)
        self.lineEditPhone.setReadOnly(True)
        self.radioButtonMale.setEnabled(False)
        self.radioButtonFemale.setEnabled(False)
        #reset lại tên nút
        self.pushButtonChinh.setText("CHỈNH SỬA HỒ SƠ")
        try:
            self.pushButtonChinh.clicked.disconnect()
        except:
            pass
        self.pushButtonChinh.clicked.connect(self.process_chinhsua)
