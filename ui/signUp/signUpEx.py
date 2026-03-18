# from ui.signUp.signUp import Ui_MainWindow
from PyQt6.QtWidgets import QMessageBox
import json
import os
from PyQt6.QtGui import QIntValidator

from ui.signUp.signUp import Ui_MainWindow


class SignUpEx(Ui_MainWindow):
    def __init__(self, login_window=None):
        super().__init__()   # 👈 QUAN TRỌNG
        self.login_window = login_window

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.SetupSignalAndSlot()



    def SetupSignalAndSlot(self):

        current_dir = os.path.dirname(os.path.abspath(__file__))

        img_path = os.path.abspath(os.path.join(current_dir, "..", "..", "images", "signup.png")).replace("\\", "/")

        self.centralwidget.setStyleSheet(f"#centralwidget {{ border-image: url({img_path}); }}")

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
        # if not (phone.isdigit() and len(phone) == 10):
        #     QMessageBox.warning(self.MainWindow, "Error", "Contact No must be 10-digit number")
        #     return

        phone = self.lineEditContactNo.text()

        # kiểm tra số điện thoại
        if not phone.isdigit():
            QMessageBox.warning(self.MainWindow, "Error", "Phone number must contain only digits")
            return

        if len(phone) != 10:
            QMessageBox.warning(self.MainWindow, "Error", "Phone number must be exactly 10 digits")
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
            "gender": gender,
            "status": "Không"
        }

        users.append(new_user)

        with open(FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        QMessageBox.information(self.MainWindow, "Success", "Account created successfully")

        # đóng signup quay về login
        self.MainWindow.hide()
        self.login_window.show()