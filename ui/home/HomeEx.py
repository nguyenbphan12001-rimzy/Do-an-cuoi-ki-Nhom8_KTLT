import sys

from PyQt6.QtWidgets import QMainWindow

from ui.home.Home import Ui_MainWindow
from ui.login.loginEx import LoginEx
from ui.signUp.signUpEx import SignUpEx
import os

class HomeEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()

        if getattr(sys, 'frozen', False):
            BASE_DIR = os.path.dirname(sys.executable)
        else:
            BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

        img_path = os.path.join(BASE_DIR, "images", "Home.png").replace("\\", "/")

        self.centralwidget.setStyleSheet(f"#centralwidget {{ border-image: url('{img_path}'); }}")
        # -------------------------------------
    def showWindow(self):
        self.MainWindow.show()

    def setupSignalAndSlot(self):
        self.pushButtonLogin.clicked.connect(self.process_login)
        self.pushButtonSignUp.clicked.connect(self.process_signup)
    def process_login(self):
        self.login_window=QMainWindow()
        self.login_ui=LoginEx()
        self.login_ui.setupUi(self.login_window)
        self.login_window.show()
        self.MainWindow.hide()

    def process_signup(self):
        self.signup_window = QMainWindow()
        self.signup_ui = SignUpEx(self.MainWindow)
        self.signup_ui.setupUi(self.signup_window)
        self.signup_window.show()
        self.MainWindow.close()  # (tuỳ bạn muốn ẩn Home hay không)