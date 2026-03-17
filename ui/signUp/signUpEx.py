# from ui.signUp.signUp import Ui_MainWindow
from PyQt6.QtWidgets import QMessageBox

from ui.signUp.signUp import Ui_MainWindow


class SignUpEx(Ui_MainWindow):
    def setupUi(self,MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
    def showWindow(self):
        self.MainWindow.show()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow

        # kết nối nút Create account
        self.pushButtonCreate.clicked.connect(self.create_account)
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

        # kiểm tra password trùng
        if password != confirm:
            QMessageBox.warning(self.MainWindow, "Error", "Passwords do not match")
            return
        QMessageBox.information(self.MainWindow, "Success", "Account created successfully")
        # đóng signup quay về login
        self.MainWindow.hide()

