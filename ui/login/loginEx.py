import json
import os
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from ui.login.login import Ui_MainWindow
from ui.signUp.signUpEx import SignUpEx
# from ui.dashboard.DashboardEx import DashboardEx


class LoginEx(Ui_MainWindow):

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow

        current_dir = os.path.dirname(os.path.abspath(__file__))

        img_path = os.path.abspath(os.path.join(current_dir, "..", "..", "images", "login.png")).replace("\\", "/")

        self.centralwidget.setStyleSheet(f"#centralwidget {{ border-image: url({img_path}); }}")

        self.pushButtonSignUp.clicked.connect(self.open_signup)
        self.pushButtonLogin.clicked.connect(self.handle_login)
        self.pushButtonForgetPassword.clicked.connect(self.forget_password)

        # 📂 PATH JSON
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(BASE_DIR, "../../datasets/user.json")
    def showWindow(self):
        self.MainWindow.show()

    # 🔹 SIGNUP
    def open_signup(self):
        self.signup_window = QMainWindow()
        self.signup = SignUpEx()
        self.signup.setupUi(self.signup_window)

        self.signup_window.show()
        self.MainWindow.close()

    def open_dashboard(self, role, username):
        print("👉 Đang mở dashboard...")

        from ui.dashboard.DashboardEx import DashboardEx  # 👈 chuyển vào đây
        self.dashboard_window = QMainWindow()
        self.dashboard = DashboardEx()
        self.dashboard.setupUi(self.dashboard_window)

        # 👉 truyền dữ liệu nếu muốn
        self.dashboard_window.setWindowTitle(f"Dashboard - {username} ({role})")

        self.dashboard_window.showMaximized()
        print("👉 Đang mở dashboard...")

        self.MainWindow.hide()
    def handle_login(self):
        username = self.lineEditUsername.text().strip()
        password = self.lineEditPassword.text().strip()

        if username == "" or password == "":
            QMessageBox.warning(self.MainWindow, "Lỗi", "Nhập username và password!")
            return

        # 👉 ROLE
        if self.radioButtonAdmin.isChecked():
            role = "admin"
        elif self.radioButtonUser.isChecked():
            role = "user"
        else:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Chọn role!")
            return

        # 👉 ĐỌC FILE
        try:
            with open(self.file_path, encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Lỗi", f"Không đọc được file!\n{e}")
            return

        # 👉 FLAG kiểm tra
        found = False

        for user in data.get("Datasets", []):
            if (
                    user.get("username") == username and
                    user.get("password") == password and
                    user.get("role") == role
            ):
                found = True
                break

        if found:
            QMessageBox.information(self.MainWindow, "Thành công", f"Xin chào {username}!")
            self.open_dashboard(role, username)
        else:
            QMessageBox.warning(self.MainWindow, "Sai", "Sai tài khoản / mật khẩu / role!")
    # 🔑 FORGET PASSWORD
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
