import json
import sys
from datetime import datetime
import os
import traceback
from PyQt6.QtWidgets import QMessageBox, QMainWindow
from models.members import Members
from ui.member.MemberMainWindow import Ui_MainWindow


class MemberMainWindowEx(Ui_MainWindow):
    def __init__(self, member=None):
        super().__init__()

        if getattr(sys, 'frozen', False):
            self.BASE_DIR = os.path.dirname(sys.executable)
        else:
            self.BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

        self.DATASETS_DIR = os.path.join(self.BASE_DIR, "Datasets")


        self.mb = Members()
        self.file_member = os.path.join(self.DATASETS_DIR, "member.json")
        self.mb.import_json(self.file_member)
        self.current_user = None

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()

        img_path = os.path.join(self.BASE_DIR, "images", "hoivien_anh(update).jpg").replace("\\", "/")
        self.centralwidget.setStyleSheet(f"#centralwidget {{ border-image: url('{img_path}'); }}")

        self.load_member_data()

        self.lineEditGoi.setReadOnly(True)

    def showWindow(self):
        self.MainWindow.show()

    def setupSignalAndSlot(self):
        self.pushButtonKhonggiahan.clicked.connect(self.process_khonggiahan)
        self.pushButtonGiahan.clicked.connect(self.process_giahan)
        self.pushButtonChinh.clicked.connect(self.process_chinhsua)
        self.pushButtonBack.clicked.connect(self.showDashboard)

    def process_khonggiahan(self):
        QMessageBox.information(self.MainWindow, "Thông báo", "Bạn đã chọn không gia hạn")
        self.showDashboard()

    def showDashboard(self):
        from ui.dashboard.DashboardEx import DashboardEx
        self.dashboard_window = QMainWindow()
        self.dashboard_ui = DashboardEx()
        self.dashboard_ui.setupUi(self.dashboard_window)
        self.dashboard_ui.current_user = self.current_user
        self.dashboard_window.showMaximized()
        self.dashboard_ui.showWindow()
        self.MainWindow.close()

    def process_giahan(self):
        from ui.registration.Registration_formMainWindowEx import Registration_formMainWindowEx
        self.registration_window = QMainWindow()
        self.registration_ui = Registration_formMainWindowEx()
        self.registration_ui.setupUi(self.registration_window)
        self.registration_window.show()
        self.MainWindow.close()

    def load_member_data(self):
        try:
            current_user_file = os.path.join(self.DATASETS_DIR, "current_user.json")
            member_file = os.path.join(self.DATASETS_DIR, "member.json")

            if not os.path.exists(current_user_file):
                return
            with open(current_user_file, 'r', encoding='utf-8') as f:
                self.current_user = json.load(f)

            user_phone = str(self.current_user.get("phone_number", ""))
            user_name = self.current_user.get("username", "")

            self.lineEditName.setText(user_name)
            self.lineEditPhone.setText(user_phone)
            self.lineEditGoi.setText("Chưa đăng ký gói nào")

            if not os.path.exists(member_file):
                return
            with open(member_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            ds_hoi_vien = data.get("Datasets", [])

            my_info = None
            for m in reversed(ds_hoi_vien):
                if str(m.get("phone_number")) == user_phone or m.get("username") == user_name:
                    my_info = m
                    break

            if my_info:
                goi_tap = my_info.get("serve") or my_info.get("package") or "Chưa rõ gói"
                self.lineEditGoi.setText(str(goi_tap))

                ngay_dk = my_info.get("register_date", "--/--/----")
                ngay_hh = my_info.get("expire_date", "--/--/----")
                self.labelNgayDKy.setText(ngay_dk)
                self.labelNgayGiahan.setText(ngay_hh)

                gender = str(my_info.get("gender", "")).upper()
                if gender in ["M", "NAM", "MALE"]:
                    self.radioButtonMale.setChecked(True)
                else:
                    self.radioButtonFemale.setChecked(True)

                try:
                    today = datetime.now()
                    expire_dt = datetime.strptime(ngay_hh, "%d/%m/%Y")
                    if today <= expire_dt:
                        self.pushButtonConhan.setStyleSheet(
                            "background-color: #5cb85c; color: white; border-radius:10px; font-weight: bold;")
                        self.pushButtonHethan.setStyleSheet(
                            "background-color: #e0e0e0; color: gray; border-radius:10px;")
                    else:
                        self.pushButtonConhan.setStyleSheet(
                            "background-color: #e0e0e0; color: gray; border-radius:10px;")
                        self.pushButtonHethan.setStyleSheet(
                            "background-color: #d9534f; color: white; border-radius:10px; font-weight: bold;")
                except:
                    pass
            else:
                self.pushButtonGiahan.hide()
                self.pushButtonKhonggiahan.hide()

        except Exception as e:
            print(f"Lỗi load_member_data: {e}")

    def process_chinhsua(self):
        self.lineEditName.setReadOnly(False)
        self.lineEditPhone.setReadOnly(False)
        self.radioButtonMale.setEnabled(True)
        self.radioButtonFemale.setEnabled(True)
        self.pushButtonChinh.setText("LƯU HỒ SƠ (SAVE)")

        try:
            self.pushButtonChinh.clicked.disconnect()
        except:
            pass
        self.pushButtonChinh.clicked.connect(self.save_changes)

    def save_changes(self):
        try:
            new_name = self.lineEditName.text().strip()
            new_phone = self.lineEditPhone.text().strip()
            new_gender = "M" if self.radioButtonMale.isChecked() else "F"

            if not new_name or not new_phone:
                QMessageBox.warning(self.MainWindow, "Lỗi", "Không được để trống tên hoặc SĐT!")
                return

            with open(self.file_member, 'r', encoding='utf-8') as f:
                data = json.load(f)

            updated = False
            for m in data.get("Datasets", []):
                if m.get("username") == self.current_user.get("username"):
                    m["username"] = new_name
                    m["phone_number"] = new_phone
                    m["gender"] = new_gender
                    updated = True

            if updated:
                with open(self.file_member, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)

                self.current_user["username"] = new_name
                self.current_user["phone_number"] = new_phone
                session_path = os.path.join(self.DATASETS_DIR, "current_user.json")
                with open(session_path, 'w', encoding='utf-8') as f:
                    json.dump(self.current_user, f, indent=4, ensure_ascii=False)

                QMessageBox.information(self.MainWindow, "Thành công", "Đã cập nhật hồ sơ!")

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

        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Lỗi", f"Lỗi lưu file: {str(e)}")