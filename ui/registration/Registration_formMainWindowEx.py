# from PyQt6.QtWidgets import QMessageBox, QMainWindow
#
# from ui.payment.paymentEx import PaymentEx
# from ui.registration.Registration_formMainWindow import Ui_MainWindow
#
#
#
# class Registration_formMainWindowEx(Ui_MainWindow):
#     def setupUi(self, MainWindow):
#         super().setupUi(MainWindow)
#         self.MainWindow = MainWindow
#         self.setupSignalAndSlot()
#
#     def setupSignalAndSlot(self):
#         # Kết nối các nút bấm đúng với tên trong Object Inspector của bạn
#         self.pushButtonHaituan.clicked.connect(lambda: self.process_goitap("2 tuần", 299000))
#         self.pushButtonMotthang.clicked.connect(lambda: self.process_goitap("1 tháng", 499000))
#         self.pushButtonBathang.clicked.connect(lambda: self.process_goitap("3 tháng", 1399000))
#         self.pushButtonSauthang.clicked.connect(lambda: self.process_goitap("6 tháng", 2499000))
#         self.pushButtonMotnam.clicked.connect(lambda: self.process_goitap("1 năm", 4799000))
#
#     def process_goitap(self, ten_goi=None, gia=None):
#         # Hiển thị thông báo xác nhận
#         reply = QMessageBox.question(
#             self.MainWindow,
#             "Xác nhận",
#             f"Bạn có chắc chắn muốn đăng ký gói {ten_goi} không?\nGiá: {gia:,} VNĐ",
#             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
#         )
#
#         if reply == QMessageBox.StandardButton.Yes:
#             self.showPayment(ten_goi, gia)
#
#     def showPayment(self, ten_goi, gia):
#         # Khởi tạo cửa sổ QMainWindow mới
#         self.payment_window = QMainWindow()
#         # Khởi tạo lớp logic PaymentEx
#         self.payment_ui = PaymentEx()
#         self.payment_ui.setupUi(self.payment_window)
#
#         # Đổ dữ liệu từ Đăng ký sang Thanh toán
#         self.payment_ui.set_payment_info(ten_goi, gia)
#
#         # Hiển thị màn hình mới và ẩn màn hình cũ
#         self.payment_ui.showWindow()
#         self.MainWindow.hide()
#
#     def showWindow(self):
#         self.MainWindow.show()

from PyQt6.QtWidgets import QMessageBox, QMainWindow

# Đảm bảo đường dẫn import này chính xác với cấu trúc thư mục của bạn
from ui.payment.paymentEx import PaymentEx
from ui.registration.Registration_formMainWindow import Ui_MainWindow


class Registration_formMainWindowEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()

    def setupSignalAndSlot(self):
        """Kết nối các nút bấm gói tập với hàm xử lý"""
        # Các nút bấm dựa trên Object Name bạn đã đặt trong Qt Designer
        self.pushButtonHaituan.clicked.connect(lambda: self.process_goitap("2 tuần", 299000))
        self.pushButtonMotthang.clicked.connect(lambda: self.process_goitap("1 tháng", 499000))
        self.pushButtonBathang.clicked.connect(lambda: self.process_goitap("3 tháng", 1399000))
        self.pushButtonSauthang.clicked.connect(lambda: self.process_goitap("6 tháng", 2499000))
        self.pushButtonMotnam.clicked.connect(lambda: self.process_goitap("1 năm", 4799000))

    def process_goitap(self, ten_goi=None, gia=None):
        """Hiển thị hộp thoại xác nhận trước khi chuyển sang thanh toán"""
        reply = QMessageBox.question(
            self.MainWindow,
            "Xác nhận đăng ký",
            f"Bạn có chắc chắn muốn đăng ký gói {ten_goi} không?\nGiá: {gia:,} VNĐ",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.showPayment(ten_goi, gia)

    def showPayment(self, ten_goi, gia):
        """Khởi tạo và hiển thị màn hình thanh toán theo mô hình OOP"""
        # 1. Tạo instance của QMainWindow để làm cửa sổ cha cho Payment
        self.payment_window = QMainWindow()

        # 2. Khởi tạo lớp xử lý logic PaymentEx
        self.payment_ui = PaymentEx()
        self.payment_ui.setupUi(self.payment_window)

        # 3. Truyền dữ liệu (Gói tập, Giá).
        # Bên trong hàm này của PaymentEx sẽ tự động gọi load_user_data() từ user.json
        self.payment_ui.set_payment_info(ten_goi, gia)

        # 4. Hiển thị màn hình Payment (Full screen) và ẩn màn hình Registration
        self.payment_ui.showWindow()
        self.MainWindow.hide()

    def showWindow(self):
        """Hiển thị màn hình đăng ký"""
        self.MainWindow.show()