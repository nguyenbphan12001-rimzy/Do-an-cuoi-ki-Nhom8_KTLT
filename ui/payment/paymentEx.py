import json
import os
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from ui.payment.payment import Ui_MainWindow


class PaymentEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.original_price = 0  # Lưu lại giá gốc để tính toán phần trăm

        # 1. Thiết lập background hình ảnh
        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.abspath(os.path.join(current_dir, "..", "..", "images", "payments.png")).replace("\\", "/")
        self.centralwidget.setStyleSheet(f"#centralwidget {{ border-image: url({img_path}); }}")

        # 2. Kết nối các sự kiện (Signals & Slots)
        self.setup_signals()

    def setup_signals(self):
        # Sự kiện chọn Cọc 50% hoặc Trả 100%
        self.radioButtonHalf.clicked.connect(self.update_price_display)
        self.radioButtonFull.clicked.connect(self.update_price_display)

        # Sự kiện chọn phương thức thanh toán (chỉ cho chọn 1 trong 2)
        self.checkBoxBak.clicked.connect(lambda: self.handle_payment_selection("bank"))
        self.checkBoxCard.clicked.connect(lambda: self.handle_payment_selection("card"))

        # Sự kiện nút Xác nhận
        self.pushButtonCofirm.clicked.connect(self.process_confirm)

    def load_user_data(self):
        """Đọc file session bằng cách tìm thư mục gốc của Project"""
        try:
            # 1. Lấy đường dẫn của file paymentEx.py đang chạy
            current_file_path = os.path.abspath(__file__)

            # 2. Tìm thư mục "DO AN KTLT" trong đường dẫn đó
            # Code này sẽ cắt chuỗi để lấy phần đường dẫn đến hết "DO AN KTLT"
            project_root = current_file_path.split("ui")[0]

            # 3. Kết hợp với thư mục datasets
            file_path = os.path.join(project_root, "datasets", "current_user.json")

            print(f"--- Payment đang đọc session tại: {file_path}")

            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    user = json.load(f)

                    # Điền Tên và SĐT
                    self.lineEditName.setText(str(user.get("username", "")))

                    if hasattr(self, 'lineEditID'):
                        self.lineEditID.setText(str(user.get("phone_number", "")))
                    elif hasattr(self, 'lineEditSDT'):
                        self.lineEditSDT.setText(str(user.get("phone_number", "")))

                    print(f"✅ Nạp thành công User: {user.get('username')}")
            else:
                print(f"⚠️ KHÔNG tìm thấy file tại: {file_path}")
        except Exception as e:
            print(f"❌ Lỗi: {e}")

    def set_payment_info(self, ten_goi, gia):
        """Nhận dữ liệu từ màn hình Đăng ký truyền sang"""
        self.original_price = gia
        self.lineEditPackage.setText(ten_goi)
        self.lineEditTime.setText("Theo gói đã chọn")

        # Mặc định ban đầu
        self.radioButtonFull.setChecked(True)
        self.update_price_display()

        # GỌI HÀM NẠP DỮ LIỆU TỪ SESSION
        self.load_user_data()

    def update_price_display(self):
        """Xử lý chia đôi tiền khi nhấn Cọc 50%"""
        if self.radioButtonHalf.isChecked():
            current_price = self.original_price / 2
        else:
            current_price = self.original_price

        self.lineEditTotalMoney.setText(f"{int(current_price):,} VNĐ")

    def handle_payment_selection(self, selected_type):
        """Đảm bảo chỉ chọn được Ngân hàng HOẶC Thẻ tín dụng"""
        if selected_type == "bank":
            if self.checkBoxBak.isChecked():
                self.checkBoxCard.setChecked(False)
        else:
            if self.checkBoxCard.isChecked():
                self.checkBoxBak.setChecked(False)

    def process_confirm(self):
        """Xử lý: Hiện thông báo nhỏ trước -> Nhấn OK -> Hiện màn hình Confirm bự"""
        ten = self.lineEditName.text().strip()
        sdt = ""
        if hasattr(self, 'lineEditID'):
            sdt = self.lineEditID.text().strip()

        # 1. Kiểm tra điều kiện (Validate)
        if not self.checkBoxBak.isChecked() and not self.checkBoxCard.isChecked():
            QMessageBox.warning(self.MainWindow, "Thông báo", "Vui lòng chọn phương thức thanh toán!")
            return

        if not ten:
            QMessageBox.warning(self.MainWindow, "Thông báo", "Thiếu thông tin khách hàng!")
            return

        # 2. Hiển thị thông báo nhỏ (Hộp thoại xác nhận)
        phuong_thuc = "Ngân hàng" if self.checkBoxBak.isChecked() else "Thẻ tín dụng"
        msg = f"Khách hàng: {ten}\nSĐT: {sdt}\nGói: {self.lineEditPackage.text()}\nThanh toán thành công qua {phuong_thuc}!"

        # Dòng này sẽ làm app dừng lại đợi bạn nhấn OK
        QMessageBox.information(self.MainWindow, "Thành công", msg)

        # 3. Sau khi nhấn OK, đoạn code dưới đây mới chạy để mở màn hình Confirm bự
        try:
            from ui.confirm.ConfirmEx import ConfirmEx  # Import tại đây để tránh vòng lặp import

            self.confirm_window = QMainWindow()
            self.confirm_ui = ConfirmEx()
            self.confirm_ui.setupUi(self.confirm_window)

            # Hiển thị màn hình confirm bự
            self.confirm_ui.showWindow()

            # Xóa màn hình thanh toán
            self.MainWindow.close()

            print("--- Đã chuyển sang màn hình Confirm sau khi nhấn OK")
        except Exception as e:
            print(f"Lỗi chuyển màn hình: {e}")

    def showWindow(self):
        """Hiển thị full màn hình"""
        self.MainWindow.showMaximized()