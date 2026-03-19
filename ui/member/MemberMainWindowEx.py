from datetime import datetime
import os

from PyQt6.QtWidgets import QMessageBox, QMainWindow

from models.members import Members
from ui.member.MemberMainWindow import Ui_MainWindow



class MemberMainWindowEx(Ui_MainWindow):
    def __init__(self, member=None):
        super().__init__()
        # 1. Xác định đường dẫn tuyệt đối để tránh lỗi file không tìm thấy
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = current_dir.split("ui")[0]
        file_member = os.path.join(project_root, "Datasets", "member.json")

        self.mb = Members()
        # Nạp dữ liệu từ file
        self.mb.import_json(file_member)

        self.current_user = None  # Nhận dữ liệu từ dashboard
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
        self.dashboard_window = QMainWindow()
        self.dashboard_ui = DashboardEx()
        self.dashboard_ui.setupUi(self.dashboard_window)

        # Trả lại user cho Dashboard để Dashboard có thể mở lại Member lần nữa
        self.dashboard_ui.current_user = self.current_user

        self.dashboard_window.showMaximized()
        self.MainWindow.close()  # Đóng Member khi về Dashboard

    def process_giahan(self):
        from ui.registration.Registration_formMainWindowEx import Registration_formMainWindowEx
        self.registration_window=QMainWindow()
        self.registration_ui=Registration_formMainWindowEx()
        self.registration_ui.setupUi(self.registration_window)
        self.registration_window.show()
        self.MainWindow.close()

    def load_member(self):
        if not self.current_user:
            print("Lỗi: Không tìm thấy session người dùng (current_user is None)")
            return

        username = self.current_user.get("username")
        member = None

        # 1. Tìm hội viên trong danh sách (mb.list)
        for m in self.mb.list:
            if m.username == username:
                member = m
                break

        # 2. Nếu không tìm thấy, báo lỗi và dừng hàm
        if not member:
            QMessageBox.warning(self.MainWindow, "Thông báo", "Bạn chưa đăng ký hội viên!")
            return

        # 3. Đổ dữ liệu lên các ô nhập liệu
        self.member = member
        self.lineEditName.setText(member.username)
        self.lineEditPhone.setText(member.phone_number)
        self.lineEditGoi.setText(member.package)

        # Hiển thị Giới tính
        if member.gender == "M":
            self.radioButtonMale.setChecked(True)
        else:
            self.radioButtonFemale.setChecked(True)

        # Khóa lại không cho sửa (chỉ cho sửa khi nhấn nút CHỈNH SỬA)
        self.radioButtonMale.setEnabled(False)
        self.radioButtonFemale.setEnabled(False)

        # 4. Xử lý logic Ngày hết hạn và màu sắc Nút trạng thái
        try:
            today = datetime.today().date()
            expire_date = member.expire_date

            # Chuyển đổi chuỗi ngày thành object date để so sánh
            if isinstance(expire_date, str):
                expire_date = datetime.strptime(expire_date, "%d/%m/%Y").date()

            # Kiểm tra Còn hạn hay Hết hạn
            if expire_date >= today:
                # Còn hạn: Nút Xanh sáng lên, nút Đỏ mờ đi
                self.pushButtonConhan.setEnabled(True)
                self.pushButtonHethan.setEnabled(False)
                self.pushButtonConhan.setStyleSheet(
                    "background-color: rgb(78,170,28); color: white; font-weight: bold; border-radius:10px;")
                self.pushButtonHethan.setStyleSheet("background-color: lightgray; color: gray; border-radius:10px;")
            else:
                # Hết hạn: Nút Đỏ sáng lên, nút Xanh mờ đi
                self.pushButtonConhan.setEnabled(False)
                self.pushButtonHethan.setEnabled(True)
                self.pushButtonConhan.setStyleSheet("background-color: lightgray; color: gray; border-radius:10px;")
                self.pushButtonHethan.setStyleSheet(
                    "background-color: rgb(255,138,138); color: white; font-weight: bold; border-radius:10px;")

        except Exception as e:
            print(f"Lỗi xử lý ngày tháng: {e}")

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
        name = self.lineEditName.text().strip()
        phone = self.lineEditPhone.text().strip()

        if not name or not phone:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng không để trống!")
            return

        gender = "M" if self.radioButtonMale.isChecked() else "F"
        old_username = self.current_user.get("username")

        member_to_update = None
        for m in self.mb.list:
            if m.username == old_username:
                member_to_update = m
                break

        if not member_to_update:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Không tìm thấy dữ liệu!")
            return

        # 1. Cập nhật object trong bộ nhớ
        member_to_update.username = name
        member_to_update.phone_number = phone
        member_to_update.gender = gender

        # 2. Lưu lại file member.json
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = current_dir.split("ui")[0]
        member_file = os.path.join(project_root, "Datasets", "member.json")
        self.mb.export_json(member_file)

        # 3. Cập nhật Session file (Để đổi tên đồng bộ các màn hình)
        self.current_user["username"] = name
        self.current_user["phone_number"] = phone
        session_file = os.path.join(project_root, "datasets", "current_user.json")
        try:
            import json
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(self.current_user, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Lỗi cập nhật session: {e}")

        QMessageBox.information(self.MainWindow, "Thành công", "Đã lưu thay đổi!")

        # 4. Khóa giao diện và đổi nút về CHỈNH SỬA
        self.lineEditName.setReadOnly(True)
        self.lineEditPhone.setReadOnly(True)
        self.radioButtonMale.setEnabled(False)
        self.radioButtonFemale.setEnabled(False)
        self.pushButtonChinh.setText("CHỈNH SỬA HỒ SƠ")
        try:
            self.pushButtonChinh.clicked.disconnect()
        except:
            pass
        self.pushButtonChinh.clicked.connect(self.process_chinhsua)
