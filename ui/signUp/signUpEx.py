# from ui.signUp.signUp import Ui_MainWindow
from PyQt6.QtWidgets import QMessageBox
import json
import os
from PyQt6.QtGui import QIntValidator

from ui.signUp.signUp import Ui_MainWindow


class SignUpEx(Ui_MainWindow):
    def __init__(self, login_window):
        super().__init__()   # 👈 QUAN TRỌNG
        self.login_window = login_window

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow

        # connect nút
        self.pushButtonCreate.clicked.connect(self.create_account)
        self.lineEditContactNo.setValidator(QIntValidator())

    def showWindow(self):
        self.MainWindow.show()

    def create_account(self):

        name = self.lineEditName.text()
        email = self.lineEditEmail.text()
        phone = self.lineEditContactNo.text()
        password = self.lineEditPassword.text()
        confirm = self.lineEditConfirm.text()

        # kiểm tra rỗng
        if name == "" or email == "" or phone == "" or password == "" or confirm == "":
            QMessageBox.warning(self.MainWindow, "Error", "Please fill all fields")
            return
        if not (phone.isdigit() and len(phone) == 10):
            QMessageBox.warning(self.MainWindow, "Error", "Contact No must be 10-digit number")
            return

        # kiểm tra password trùng
        if password != confirm:
            QMessageBox.warning(self.MainWindow, "Error", "Passwords do not match")
            return
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        FILE = os.path.join(BASE_DIR, "../../datasets/user.json")
        with open(FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        users = data["Datasets"]

        for u in users:
            if u["email"] == email:
                QMessageBox.warning(self.MainWindow, "Error", "Account already exists")
                return

        new_user = {
            "username": name,
            "email": email,
            "phone_number": phone,
            "password": password,
            "role": "user",
            "gender": "M",
            "status": "Không"
        }

        users.append(new_user)

        with open(FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        QMessageBox.information(self.MainWindow, "Success", "Account created successfully")

        # đóng signup quay về login
        self.MainWindow.hide()
        self.login_window.show()