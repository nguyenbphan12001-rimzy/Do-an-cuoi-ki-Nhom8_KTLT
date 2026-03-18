# from ui.payment.payment import Ui_MainWindow
# import os
#
#
# class PaymentEx(Ui_MainWindow):
#     def setupUi(self, MainWindow):
#         super().setupUi(MainWindow)
#         self.MainWindow = MainWindow
#
#         # Thiết lập background
#         current_dir = os.path.dirname(os.path.abspath(__file__))
#         img_path = os.path.abspath(os.path.join(current_dir, "..", "..", "images", "payments.png")).replace("\\", "/")
#         self.centralwidget.setStyleSheet(f"#centralwidget {{ border-image: url({img_path}); }}")
#
#     def set_payment_info(self, ten_goi, gia):
#         """Phương thức nhận dữ liệu và hiển thị lên giao diện"""
#         # Hiển thị vào các QLineEdit dựa trên Object Name trong ảnh của bạn
#         self.lineEditPackage.setText(ten_goi)
#         self.lineEditTime.setText("Theo gói đã chọn")  # Hoặc tùy biến thêm
#         self.lineEditTotalMoney.setText(f"{gia:,} VNĐ")
#
#         # Bạn có thể mặc định chọn một phương thức thanh toán
#         self.radioButtonFull.setChecked(True)
#
#     def showWindow(self):
#         self.MainWindow.showMaximized()

from PyQt6.QtWidgets import QMainWindow, QMessageBox
from ui.payment.payment import Ui_MainWindow
import os


class PaymentEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.original_price = 0  # Lưu lại giá gốc để tính toán

        # Thiết lập background
        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.abspath(os.path.join(current_dir, "..", "..", "images", "payments.png")).replace("\\", "/")
        self.centralwidget.setStyleSheet(f"#centralwidget {{ border-image: url({img_path}); }}")

        self.setup_signals()

    def setup_signals(self):
        # Logic tính tiền cọc/đầy đủ
        self.radioButtonHalf.clicked.connect(self.update_price_display)
        self.radioButtonFull.clicked.connect(self.update_price_display)

        # Logic chọn duy nhất 1 phương thức thanh toán
        self.checkBoxBak.clicked.connect(lambda: self.handle_payment_selection("bank"))
        self.checkBoxCard.clicked.connect(lambda: self.handle_payment_selection("card"))

        # Logic nút Xác nhận
        self.pushButtonCofirm.clicked.connect(self.process_confirm)

    def set_payment_info(self, ten_goi, gia):
        """Nhận dữ liệu từ màn hình đăng ký"""
        self.original_price = gia
        self.lineEditPackage.setText(ten_goi)
        self.lineEditTime.setText("Theo gói đã chọn")

        self.radioButtonFull.setChecked(True)
        self.update_price_display()

    def update_price_display(self):
        """Cập nhật giá hiển thị"""
        if self.radioButtonHalf.isChecked():
            current_price = self.original_price / 2
        else:
            current_price = self.original_price

        self.lineEditTotalMoney.setText(f"{int(current_price):,} VNĐ")

    def handle_payment_selection(self, selected_type):
        """Xử lý chọn CheckBox"""
        if selected_type == "bank":
            if self.checkBoxBak.isChecked():
                self.checkBoxCard.setChecked(False)
        else:
            if self.checkBoxCard.isChecked():
                self.checkBoxBak.setChecked(False)

    def process_confirm(self):
        """Xử lý khi nhấn nút Xác nhận"""
        # 1. Kiểm tra thông tin khách hàng
        ten = self.lineEditName.text().strip()
        customer_id = self.lineEditID.text().strip()

        if not ten or not customer_id:
            QMessageBox.warning(self.MainWindow, "Thiếu thông tin", "Vui lòng nhập đầy đủ Tên và ID khách hàng!")
            return

        # 2. Kiểm tra phương thức thanh toán
        if not self.checkBoxBak.isChecked() and not self.checkBoxCard.isChecked():
            QMessageBox.warning(self.MainWindow, "Thiếu thông tin",
                                "Vui lòng chọn phương thức thanh toán (Ngân hàng hoặc Thẻ)!")
            return

        # 3. Thông báo thành công
        phuong_thuc = "Ngân hàng" if self.checkBoxBak.isChecked() else "Thẻ tín dụng"
        so_tien = self.lineEditTotalMoney.text()

        msg = f"Chúc mừng khách hàng {ten} (ID: {customer_id})!\n"
        msg += f"Bạn đã đăng ký thành công gói: {self.lineEditPackage.text()}\n"
        msg += f"Số tiền thanh toán: {so_tien}\n"
        msg += f"Hình thức: {phuong_thuc}"

        QMessageBox.information(self.MainWindow, "Thành công", msg)

        # Tùy chọn: Đóng ứng dụng hoặc quay lại màn hình chính
        # self.MainWindow.close()

    def showWindow(self):
        self.MainWindow.showMaximized()