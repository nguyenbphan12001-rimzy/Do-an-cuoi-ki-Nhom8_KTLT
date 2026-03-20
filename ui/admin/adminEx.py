from PyQt6.QtWidgets import QMainWindow, QMessageBox
from ui.admin.admin import Ui_MainWindow
import json
import os

class AdminEx(Ui_MainWindow):
    def __init__(self, username=None):
        super().__init__()
        self.username = username

        # Path file JSON user
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(current_dir, "../../datasets/user.json").replace("\\", "/")

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.MainWindow.resize(900, 600)

        # Background
        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(current_dir, "../../images/fit lifestyle.jpg").replace("\\", "/")
        self.centralwidget.setStyleSheet(f"""
        #centralwidget {{
            background-image: url({img_path});
            background-repeat: no-repeat;
            background-position: center;
            background-size: contain;
        }}
        """)

        # Load dữ liệu user lên UI
        self.load_user_info()

        # Khóa ô input ban đầu
        self.set_read_only(True)

        # Kết nối nút Update / Save
        self.pushButtonUpdate.clicked.connect(self.enable_edit)
        self.pushButtonSave.clicked.connect(self.save_user_info)

    def enable_edit(self):
        """Cho phép chỉnh sửa các ô input"""
        self.set_read_only(False)
        self.lineEditUsername.setFocus()

    def save_user_info(self):
        """Lưu thông tin vào file JSON và khóa lại input"""
        try:
            with open(self.file_path, encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Không thể đọc file user.json")
            return

        updated = False
        for user in data.get("Datasets", []):
            if user.get("username") == self.username:
                # Cập nhật dữ liệu
                user["username"] = self.lineEditUsername.text()
                user["phone_number"] = self.lineEditPhoneNo.text()
                user["email"] = self.lineEditEmail.text()
                user["status"] = self.lineEditStatus.text()
                user["gender"] = "M" if self.radioButtonMale.isChecked() else "F"
                self.username = user["username"]
                updated = True
                break

        if updated:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            # Khóa lại ô input
            self.set_read_only(True)
            self.load_user_info()
            QMessageBox.information(self.MainWindow, "Thành công", "Đã lưu thông tin!")
        else:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Không tìm thấy user để lưu!")

    def set_read_only(self, status: bool):
        """Khóa hoặc mở khóa các ô input"""
        self.lineEditUsername.setReadOnly(status)
        self.lineEditPhoneNo.setReadOnly(status)
        self.lineEditEmail.setReadOnly(status)
        self.lineEditStatus.setReadOnly(status)
        self.radioButtonMale.setEnabled(not status)
        self.radioButtonFemale.setEnabled(not status)

    def load_user_info(self):
        """Nạp dữ liệu từ file JSON lên UI"""
        try:
            with open(self.file_path, encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            return

        for user in data.get("Datasets", []):
            if user.get("username") == self.username:
                self.lineEditUsername.setText(user.get("username", ""))
                self.lineEditPhoneNo.setText(user.get("phone_number", ""))
                self.lineEditEmail.setText(user.get("email", ""))
                self.lineEditStatus.setText(user.get("status", ""))
                if user.get("gender") == "M":
                    self.radioButtonMale.setChecked(True)
                else:
                    self.radioButtonFemale.setChecked(True)
                break

        print("USERNAME NHẬN ĐƯỢC:", self.username)