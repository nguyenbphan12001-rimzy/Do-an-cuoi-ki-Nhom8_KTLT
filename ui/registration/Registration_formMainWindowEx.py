import os
import sys
from PyQt6.QtWidgets import QMessageBox, QMainWindow

from ui.payment.paymentEx import PaymentEx
from ui.registration.Registration_formMainWindow import Ui_MainWindow


class Registration_formMainWindowEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()
        if getattr(sys, 'frozen', False):
            BASE_DIR = os.path.dirname(sys.executable)
        else:
            BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

        img_path = os.path.join(BASE_DIR, "images", "Registration.png").replace("\\", "/")

        self.centralwidget.setStyleSheet(f"#centralwidget {{ border-image: url('{img_path}'); }}")

    def setupSignalAndSlot(self):
        self.pushButtonHaituan.clicked.connect(lambda: self.process_goitap("2 tuần", 299000))
        self.pushButtonMotthang.clicked.connect(lambda: self.process_goitap("1 tháng", 499000))
        self.pushButtonBathang.clicked.connect(lambda: self.process_goitap("3 tháng", 1399000))
        self.pushButtonSauthang.clicked.connect(lambda: self.process_goitap("6 tháng", 2499000))
        self.pushButtonMotnam.clicked.connect(lambda: self.process_goitap("1 năm", 4799000))

        self.pushButtonback.clicked.connect(self.go_back)

    def process_goitap(self, ten_goi=None, gia=None):
        reply = QMessageBox.question(
            self.MainWindow,
            "Xác nhận đăng ký",
            f"Bạn có chắc chắn muốn đăng ký gói {ten_goi} không?\nGiá: {gia:,} VNĐ",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.showPayment(ten_goi, gia)

    def showPayment(self, ten_goi, gia):
        self.payment_window = QMainWindow()
        self.payment_ui = PaymentEx()
        self.payment_ui.setupUi(self.payment_window)
        self.payment_ui.set_payment_info(ten_goi, gia)
        self.payment_window.showMaximized()  # Hiện full màn hình cho thanh toán
        self.MainWindow.hide()

    def go_back(self):
        from ui.dashboard.DashboardEx import DashboardEx

        self.dashboard_window = QMainWindow()
        self.dashboard_ui = DashboardEx()
        self.dashboard_ui.setupUi(self.dashboard_window)

        self.dashboard_window.showMaximized()
        self.dashboard_ui.showWindow()

        self.MainWindow.close()

    def showWindow(self):
        self.MainWindow.show()