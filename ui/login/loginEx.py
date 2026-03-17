from PyQt6.QtWidgets import QMainWindow

from ui.login.login import Ui_MainWindow
from ui.signUp.signUpEx import SignUpEx

import os
class LoginEx(Ui_MainWindow):
    def setupUi(self,MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.pushButtonSignUp.clicked.connect(self.open_signup)

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


