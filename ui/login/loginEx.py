import json
import os
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from ui.login.login import Ui_MainWindow
from ui.signUp.signUpEx import SignUpEx

class LoginEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.SetupSignalAndSlot()

        # Thiết lập đường dẫn thư mục gốc (DO AN KTLT)
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        # Trỏ thẳng vào thư mục datasets ở gốc project
        self.DATASETS_DIR = os.path.abspath(os.path.join(self.BASE_DIR, "../../datasets"))
        self.file_path = os.path.join(self.DATASETS_DIR, "user.json")

        # Đảm bảo thư mục datasets tồn tại để không bị lỗi ghi file
        if not os.path.exists(self.DATASETS_DIR):
            os.makedirs(self.DATASETS_DIR)

        # Thiết lập background
        img_path = os.path.abspath(os.path.join(self.BASE_DIR, "..", "..", "images", "login.png")).replace("\\", "/")
        self.centralwidget.setStyleSheet(f"#centralwidget {{ border-image: url({img_path}); }}")

    def SetupSignalAndSlot(self):
        self.pushButtonSignUp.clicked.connect(self.open_signup)
        self.pushButtonLogin.clicked.connect(self.handle_login)
        self.pushButtonForgetPassword.clicked.connect(self.forget_password)

    def save_current_session(self, user_data):
        """Lưu thông tin người dùng đang đăng nhập vào file session"""
        try:
            session_path = os.path.join(self.DATASETS_DIR, "current_user.json")
            with open(session_path, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, indent=4, ensure_ascii=False)
            print(f"✅ Đã tạo session tại: {session_path}")
        except Exception as e:
            print(f"❌ Lỗi lưu session: {e}")

    def handle_login(self):
        username = self.lineEditUsername.text().strip()
        password = self.lineEditPassword.text().strip()

        if not username or not password:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Nhập username và password!")
            return

        if self.radioButtonAdmin.isChecked():
            role = "admin"
        elif self.radioButtonUser.isChecked():
            role = "user"
        else:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng chọn Role!")
            return

        try:
            with open(self.file_path, 'r', encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Lỗi", f"Không tìm thấy file dữ liệu tại {self.file_path}")
            return

        user_found = None
        for user in data.get("Datasets", []):
            if (user.get("username") == username and
                user.get("password") == password and
                user.get("role") == role):
                user_found = user
                break

        if user_found:
            # Lưu session trước khi chuyển màn hình
            self.save_current_session(user_found)
            QMessageBox.information(self.MainWindow, "Thành công", f"Xin chào {username}!")
            self.open_dashboard(role, username)
            self.dashboard.current_user = user_found
        else:
            QMessageBox.warning(self.MainWindow, "Thất bại", "Sai tài khoản, mật khẩu hoặc role!")

    # --- Các hàm chuyển màn hình giữ nguyên ---
    def open_signup(self):
        self.signup_window = QMainWindow()
        self.signup = SignUpEx(self.MainWindow)
        self.signup.setupUi(self.signup_window)
        self.signup_window.show()
        self.MainWindow.hide()

    def open_dashboard(self, role, username):
        from ui.dashboard.DashboardEx import DashboardEx
        self.dashboard_window = QMainWindow()
        self.dashboard = DashboardEx()
        self.dashboard.setupUi(self.dashboard_window)
        self.dashboard_window.showMaximized()
        self.MainWindow.hide()

    def forget_password(self):
        username = self.lineEditUsername.text().strip()

        if username == "":
            QMessageBox.warning(self.MainWindow, "Lỗi", "Nhập username trước!")
            return

        try:
            with open(self.file_path, encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Lỗi", f"Không đọc được file!\n{e}")
            return

        for user in data.get("Datasets", []):
            if user.get("username") == username:
                QMessageBox.information(
                    self.MainWindow,
                    "Password",
                    f"Mật khẩu là: {user.get('password')}"
                )
                return

        QMessageBox.warning(self.MainWindow, "Lỗi", "Không tìm thấy username!")
