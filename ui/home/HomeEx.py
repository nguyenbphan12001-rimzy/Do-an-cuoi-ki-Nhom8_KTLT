from PyQt6.QtWidgets import QMainWindow

from ui.home.Home import Ui_MainWindow
from ui.login.loginEx import LoginEx
from ui.signUp.signUpEx import SignUpEx


class HomeEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()
    def showWindow(self):
        self.MainWindow.show()

    def setupSignalAndSlot(self):
        self.pushButtonLogin.clicked.connect(self.process_login)
        self.pushButtonSignUp.clicked.connect(self.process_signup)
    def process_login(self):
        self.login_window=QMainWindow()
        self.login_ui=LoginEx()
        self.login_ui.setupUi(self.login_window)
        self.login_ui.showWindow()
    def process_signup(self):
        self.signup_window=QMainWindow()
        self.signup_ui=SignUpEx()
        self.signup_ui.setupUi(self.signup_window)
        self.signup_ui.showWindow()