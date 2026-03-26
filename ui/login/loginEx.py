import json
import os
import sys
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from ui.login.login import Ui_MainWindow
from ui.signUp.signUpEx import SignUpEx


class LoginEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.SetupSignalAndSlot()


        if getattr(sys, 'frozen', False):
            self.BASE_DIR = os.path.dirname(sys.executable)
        else:

            self.BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

        self.DATASETS_DIR = os.path.join(self.BASE_DIR, "Datasets")
        self.file_path = os.path.join(self.DATASETS_DIR, "user.json")

        if not os.path.exists(self.DATASETS_DIR):
            os.makedirs(self.DATASETS_DIR)


        img_path = os.path.join(self.BASE_DIR, "images", "login.png").replace("\\", "/")
        self.centralwidget.setStyleSheet(f"#centralwidget {{ border-image: url('{img_path}'); }}")

    def SetupSignalAndSlot(self):
        self.pushButtonSignUp.clicked.connect(self.open_signup)
        self.pushButtonLogin.clicked.connect(self.handle_login)
        self.pushButtonForgetPassword.clicked.connect(self.forget_password)

    def save_current_session(self, user_data):
        try:
            session_path = os.path.join(self.DATASETS_DIR, "current_user.json")
            with open(session_path, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Lỗi lưu session: {e}")

    def handle_login(self):
        username = self.lineEditUsername.text().strip()
        password = self.lineEditPassword.text().strip()

        if not username or not password:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Nhập username và password!")
            return

        role = "admin" if self.radioButtonAdmin.isChecked() else "user" if self.radioButtonUser.isChecked() else None
        if role is None:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng chọn Role!")
            return

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            # Code này sẽ hiện ra chính xác là lỗi gì và nó đang tìm ở đường dẫn nào
            QMessageBox.critical(self.MainWindow, "Lỗi", f"Gặp sự cố đọc file!\nLỗi: {e}\nĐường dẫn: {self.file_path}")
            return

        user_found = next((u for u in data.get("Datasets", []) if
                           u.get("username") == username and u.get("password") == password and u.get("role") == role),
                          None)

        if user_found:
            self.save_current_session(user_found)

            if role == "admin":
                # Khởi tạo cửa sổ Thống kê (Statistic)
                from ui.statistic.StatisticMainWindowEx import StatisticMainWindowEx
                self.main_statistic_window = QMainWindow()
                self.statistic_ui = StatisticMainWindowEx()
                self.statistic_ui.setupUi(self.main_statistic_window)

                self.main_statistic_window.show()
                print(f"✅ Admin {username} đã đăng nhập vào hệ thống Thống kê.")
            else:
                from ui.dashboard.DashboardEx import DashboardEx
                self.main_dashboard_window = QMainWindow()
                self.dashboard_ui = DashboardEx(username)
                self.dashboard_ui.setupUi(self.main_dashboard_window)
                self.main_dashboard_window.showMaximized()
                print(f"✅ User {username} đã đăng nhập vào Dashboard.")

            self.MainWindow.hide()
        else:
            QMessageBox.warning(self.MainWindow, "Thất bại", "Sai tài khoản, mật khẩu hoặc role!")

    def open_signup(self):
        self.signup_window = QMainWindow()
        self.signup = SignUpEx(self.MainWindow)
        self.signup.setupUi(self.signup_window)
        self.signup_window.show()
        self.MainWindow.hide()

    def forget_password(self):
        username = self.lineEditUsername.text().strip()
        if not username:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Nhập username trước!")
            return
        try:
            with open(self.file_path, encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Lỗi", f"Không đọc được file!\n{e}")
            return

        for user in data.get("Datasets", []):
            if user.get("username") == username:
                QMessageBox.information(self.MainWindow, "Password", f"Mật khẩu là: {user.get('password')}")
                return

        QMessageBox.warning(self.MainWindow, "Lỗi", "Không tìm thấy username!")