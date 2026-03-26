# from ui.signUp.signUp import Ui_MainWindow
from PyQt6.QtWidgets import QMessageBox, QMainWindow
import json
import os
import sys
from PyQt6.QtGui import QIntValidator

from ui.signUp.signUp import Ui_MainWindow


class SignUpEx(Ui_MainWindow):
    def __init__(self, login_window=None):
        super().__init__()  # 👈 QUAN TRỌNG
        self.login_window = login_window

        if getattr(sys, 'frozen', False):
            self.BASE_DIR = os.path.dirname(sys.executable)
        else:
            self.BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

        self.DATASETS_DIR = os.path.join(self.BASE_DIR, "Datasets")

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.SetupSignalAndSlot()

    def SetupSignalAndSlot(self):
        img_path = os.path.join(self.BASE_DIR, "images", "signup.png").replace("\\", "/")
        self.centralwidget.setStyleSheet(f"#centralwidget {{ border-image: url('{img_path}'); }}")
        self.pushButtonCreate.clicked.connect(self.create_account)
        self.lineEditContactNo.setValidator(QIntValidator())
        self.pushButtonBack.clicked.connect(self.go_back)

    def go_back(self):
        from ui.home.HomeEx import HomeEx  # 👈 import tại đây (tránh circular)

        self.home_window = QMainWindow()
        self.home_ui = HomeEx()
        self.home_ui.setupUi(self.home_window)

        self.home_window.show()
        self.MainWindow.close()  # hoặc hide()

    def showWindow(self):
        self.MainWindow.show()

    def create_account(self):
        name = self.lineEditName.text()
        email = self.lineEditEmail.text()
        phone = self.lineEditContactNo.text()
        password = self.lineEditPassword.text()
        confirm = self.lineEditConfirm.text()

        if name == "" or email == "" or phone == "" or password == "" or confirm == "":
            QMessageBox.warning(self.MainWindow, "Error", "Please fill all fields")
            return

        phone = self.lineEditContactNo.text()

        if not phone.isdigit():
            QMessageBox.warning(self.MainWindow, "Error", "SDT phải bao gồm 10 số")
            return

        if len(phone) != 10:
            QMessageBox.warning(self.MainWindow, "Error", "SDT phải bao gồm 10 số")
            return

        if self.radioButtonMale.isChecked():
            gender = "M"
        elif self.radioButtonFemale.isChecked():
            gender = "F"
        else:
            gender = ""

        if not self.radioButtonMale.isChecked() and not self.radioButtonFemale.isChecked():
            QMessageBox.warning(self.MainWindow, "Error", "Please select gender")
            return

        if password != confirm:
            QMessageBox.warning(self.MainWindow, "Error", "Passwords do not match")
            return

        FILE = os.path.join(self.DATASETS_DIR, "user.json")

        if not os.path.exists(FILE):
            data = {"Datasets": []}
        else:
            with open(FILE, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {"Datasets": []}

        users = data.get("Datasets", [])

        for u in users:
            if u.get("email") == email:
                QMessageBox.warning(self.MainWindow, "Error", "Account already exists")
                return

        new_user = {
            "username": name,
            "email": email,
            "phone_number": phone,
            "password": password,
            "role": "user",
            "gender": gender,
            "status": "Không"
        }

        users.append(new_user)
        data["Datasets"] = users

        with open(FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        QMessageBox.information(self.MainWindow, "Success", "Account created successfully")
        self.go_back()