from PyQt6.QtWidgets import QMainWindow

from ui.login.login import Ui_MainWindow
from ui.signUp.signUpEx import SignUpEx


class LoginEx(Ui_MainWindow):
    def setupUi(self,MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.pushButtonSignUp.clicked.connect(self.open_signup)
    def showWindow(self):
        self.MainWindow.show()

    def open_signup(self):
        self.signup_window = QMainWindow()  # tạo cửa sổ
        self.signup = SignUpEx()  # tạo UI
        self.signup.setupUi(self.signup_window)
        self.signup_window.show()  # hiển thị
        self.MainWindow.close()  # đóng cửa sổ login


