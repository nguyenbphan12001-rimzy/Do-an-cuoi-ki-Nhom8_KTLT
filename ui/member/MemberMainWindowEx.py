import json
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
        self.load_member_data()
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

    def load_member_data(self):
        """Hàm tự động nạp thông tin hội viên lên giao diện"""
        try:
            # 1. Tìm đường dẫn tới thư mục datasets
            current_file_path = os.path.abspath(__file__)
            # Cắt chuỗi để lùi về thư mục gốc, chỗ này tuỳ cấu trúc thư mục của mày
            # Nếu chạy lỗi đường dẫn thì báo tao chỉnh lại
            project_root = current_file_path.split("ui")[0]
            datasets_dir = os.path.join(project_root, "datasets")

            current_user_file = os.path.join(datasets_dir, "current_user.json")
            member_file = os.path.join(datasets_dir, "member.json")

            # 2. Lấy user đang đăng nhập
            if not os.path.exists(current_user_file):
                print("Không tìm thấy current_user.json")
                return

            with open(current_user_file, 'r', encoding='utf-8') as f:
                user = json.load(f)

            sdt_hien_tai = user.get("phone_number", "")
            ten_hien_tai = user.get("username", "")

            # Hiển thị mặc định trước (lỡ nó chưa mua gói nào)
            self.lineEditName.setText(ten_hien_tai)  # Nhớ check lại tên ô lineEdit Name của mày
            self.lineEditPhone.setText(sdt_hien_tai)  # Nhớ check lại tên ô lineEdit SĐT

            # 3. Quét trong member.json để tìm gói tập
            if not os.path.exists(member_file):
                self.lineEditGoi.setText("Chưa đăng ký gói nào")
                return

            with open(member_file, 'r', encoding='utf-8') as f:
                member_data = json.load(f)

            ds_hoi_vien = member_data.get("Datasets", [])

            # Quét ngược từ dưới lên (reversed) để lấy cái gói tập MỚI MUA NHẤT
            my_membership = None
            for m in reversed(ds_hoi_vien):
                if m.get("phone_number") == sdt_hien_tai or m.get("username") == ten_hien_tai:
                    my_membership = m
                    break

            if my_membership:
                # Có mua gói -> Đổ data ra
                self.lineEditGoi.setText(my_membership.get("serve", ""))

                # Xử lý giới tính
                gender = my_membership.get("gender", "Unknown")
                if gender.lower() == "male" or gender == "Nam":
                    self.radioButtonMale.setChecked(True)
                elif gender.lower() == "female" or gender == "Nữ":
                    self.radioButtonFemale.setChecked(True)

                # Cập nhật ngày tháng (Nhớ thay bằng đúng tên Label chứa ngày của mày)
                ngay_dk = my_membership.get("register_date", "")
                ngay_hh = my_membership.get("expire_date", "")

                # Ví dụ mày đặt tên label là label_NgayDangKy và label_NgayGiaHan
                self.labelNgayDKy.setText(ngay_dk)
                self.labelNgayGiahan.setText(ngay_hh)

                # --- TÍNH TOÁN TRẠNG THÁI CÒN HẠN HAY HẾT HẠN ---
                try:
                    het_han_dt = datetime.strptime(ngay_hh, "%d/%m/%Y")
                    if datetime.now() <= het_han_dt:
                        # Còn hạn -> Mày tuỳ chỉnh giao diện chỗ này
                        self.pushButtonConhan.setStyleSheet("background-color: #5cb85c; color: white;")  # Sáng xanh
                        self.pushButtonHethan.setStyleSheet("background-color: #f5c6cb; color: gray;")  # Mờ đỏ
                    else:
                        # Hết hạn
                        self.pushButtonConhan.setStyleSheet("background-color: #d4edda; color: gray;")  # Mờ xanh
                        self.pushButtonHethan.setStyleSheet("background-color: #d9534f; color: white;")  # Sáng đỏ
                except Exception as e:
                    print("Lỗi tính ngày:", e)

            else:
                self.lineEditGoi.setText("Chưa đăng ký gói nào")
                self.labelNgayDKy.setText("--/--/----")
                self.labelNgayGiahan.setText("--/--/----")

        except Exception as e:
            import traceback
            print("Lỗi load hồ sơ:", e)
            print(traceback.format_exc())
