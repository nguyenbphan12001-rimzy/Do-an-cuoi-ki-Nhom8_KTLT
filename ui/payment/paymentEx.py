# from PyQt6.QtWidgets import QMainWindow
#
# from ui.payment.payment import Ui_MainWindow
# import os
#
# class PaymentEx(Ui_MainWindow):
#
#     def setupUi(self, MainWindow):
#         super().setupUi(MainWindow)
#         self.MainWindow = MainWindow
#
#         current_dir = os.path.dirname(os.path.abspath(__file__))
#
#         img_path = os.path.abspath(os.path.join(current_dir, "..", "..", "images", "payments.png")).replace("\\", "/")
#
#         self.centralwidget.setStyleSheet(f"#centralwidget {{ border-image: url({img_path}); }}")
#     def showWindow(self):
#         self.MainWindow.show()
from PyQt6.QtWidgets import QMainWindow
from ui.payment.payment import Ui_MainWindow
import os


class PaymentEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow

        # Thiết lập background
        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.abspath(os.path.join(current_dir, "..", "..", "images", "payments.png")).replace("\\", "/")
        self.centralwidget.setStyleSheet(f"#centralwidget {{ border-image: url({img_path}); }}")

    def set_payment_info(self, ten_goi, gia):
        """Phương thức nhận dữ liệu và hiển thị lên giao diện"""
        # Hiển thị vào các QLineEdit dựa trên Object Name trong ảnh của bạn
        self.lineEditPackage.setText(ten_goi)
        self.lineEditTime.setText("Theo gói đã chọn")  # Hoặc tùy biến thêm
        self.lineEditTotalMoney.setText(f"{gia:,} VNĐ")

        # Bạn có thể mặc định chọn một phương thức thanh toán
        self.radioButtonFull.setChecked(True)

    def showWindow(self):
        self.MainWindow.showMaximized()