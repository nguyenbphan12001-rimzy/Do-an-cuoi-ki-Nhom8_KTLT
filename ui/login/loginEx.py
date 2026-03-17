import os

from PyQt6.QtWidgets import QMainWindow, QMessageBox
from ui.login.login import Ui_MainWindow


from ui.signUp.signUpEx import SignUpEx
class LoginEx(Ui_MainWindow):
    def setupUi(self,MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.pushButtonSignUp.clicked.connect(self.open_signup)
        self.pushButtonSignUp.clicked.connect(self.open_signup)
        self.pushButtonLogin.clicked.connect(self.handle_login)
        self.pushButtonForgetPassword.clicked.connect(self.forget_password)
        current_dir = os.path.dirname(os.path.abspath(__file__))

        img_path = os.path.abspath(os.path.join(current_dir, "..", "..", "images", "login.png")).replace("\\", "/")

        self.centralwidget.setStyleSheet(f"#centralwidget {{ border-image: url({img_path}); }}")
    def showWindow(self):
        self.MainWindow.show()

    def open_signup(self):
        self.signup_window = QMainWindow()  # tạo cửa sổ
        self.signup = SignUpEx()  # tạo UI
        self.signup.setupUi(self.signup_window)
        self.signup_window.show()  # hiển thị
        self.MainWindow.close()  # đóng cửa sổ login

    def handle_login(self):
        username = self.lineEditUsername.text()
        password = self.lineEditPassword.text()
        if username == "" or password == "":
            QMessageBox.warning(self.MainWindow, "Error", "Please enter username and password")
            return
        # kiểm tra login as
        role = ""
        if self.radioButtonAdmin.isChecked():
            role = "admin"
        elif self.radioButtonUser.isChecked():
            role = "user"
        else:
            QMessageBox.warning(self.MainWindow, "Error", "Please choose login role")
            return
        if username == "admin" and password == "123" and role == "admin":
            QMessageBox.information(self.MainWindow, "Success", "Login as Admin success")

        elif username == "user" and password == "123" and role == "user":
            QMessageBox.information(self.MainWindow, "Success", "Login as User success")

        else:
            QMessageBox.warning(self.MainWindow, "Login Failed", "Wrong username or password")

    def forget_password(self):
        username = self.lineEditUsername.text()

        if username == "":
            QMessageBox.warning(self.MainWindow, "Warning", "Please enter username first")
            return

        # ví dụ dữ liệu demo
        if username == "admin":
            password = "123"
        elif username == "user":
            password = "123"
        else:
            QMessageBox.warning(self.MainWindow, "Error", "Username not found")
            return

        QMessageBox.information(
            self.MainWindow,
            "Your Password",
            f"Your password is: {password}"
        )

