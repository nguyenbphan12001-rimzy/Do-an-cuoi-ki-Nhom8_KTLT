import os
from PyQt6.QtWidgets import QMessageBox, QMainWindow


from ui.payment.paymentEx import PaymentEx
from ui.registration.Registration_formMainWindow import Ui_MainWindow


class Registration_formMainWindowEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()
        current_dir = os.path.dirname(os.path.abspath(__file__))

        img_path = os.path.abspath(os.path.join(current_dir, "..", "..", "images", "Registration.png")).replace(
            "\\", "/")

        self.centralwidget.setStyleSheet(f"#centralwidget {{ border-image: url({img_path}); }}")

    def setupSignalAndSlot(self):
        """Kết nối các nút bấm gói tập với hàm xử lý"""
        self.pushButtonHaituan.clicked.connect(lambda: self.process_goitap("2 tuần", 299000))
        self.pushButtonMotthang.clicked.connect(lambda: self.process_goitap("1 tháng", 499000))
        self.pushButtonBathang.clicked.connect(lambda: self.process_goitap("3 tháng", 1399000))
        self.pushButtonSauthang.clicked.connect(lambda: self.process_goitap("6 tháng", 2499000))
        self.pushButtonMotnam.clicked.connect(lambda: self.process_goitap("1 năm", 4799000))

        # ĐÃ SỬA: process_go_back thành go_back cho đúng với tên hàm ở dưới
        self.pushButtonback.clicked.connect(self.go_back)

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
        self.payment_window = QMainWindow()
        self.payment_ui = PaymentEx()
        self.payment_ui.setupUi(self.payment_window)
        self.payment_ui.set_payment_info(ten_goi, gia)
        self.payment_ui.showWindow()
        self.MainWindow.hide()

    def go_back(self):
        # ĐÃ DỜI DÒNG IMPORT VÀO ĐÂY (Local Import) ĐỂ TRÁNH LỖI VÒNG LẶP
        from ui.dashboard.DashboardEx import DashboardEx

        self.dashboard_window = QMainWindow()
        self.dashboard_ui = DashboardEx()
        self.dashboard_ui.setupUi(self.dashboard_window)

        self.dashboard_window.showMaximized()
        self.dashboard_ui.showWindow()

        self.MainWindow.close()

    def showWindow(self):
        """Hiển thị màn hình đăng ký"""
        self.MainWindow.show()