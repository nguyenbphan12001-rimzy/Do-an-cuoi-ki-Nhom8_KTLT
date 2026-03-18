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
        """Đọc file user.json từ thư mục Datasets bằng đường dẫn tuyệt đối"""
        try:
            # Lấy đường dẫn đến thư mục chứa file paymentEx.py hiện tại
            # D:\DO AN KTLT\ui\payment
            current_dir = os.path.dirname(os.path.abspath(__file__))

            # Đi ngược lên 2 cấp để vào thư mục gốc DO AN KTLT
            root_dir = os.path.dirname(os.path.dirname(current_dir))

            # Kết hợp với thư mục Datasets và file user.json
            file_path = os.path.join(root_dir, "Datasets", "user.json")

            print(f"--- Đang tìm file tại: {file_path}")  # Kiểm tra trong Terminal

            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    users = data.get("Datasets", [])

                    if users:
                        user = users[-1]  # Lấy user cuối cùng

                        # Đổ dữ liệu
                        self.lineEditName.setText(str(user.get("username", "")))

                        # Thử cả 2 tên object phổ biến cho SĐT
                        if hasattr(self, 'lineEditID'):
                            self.lineEditID.setText(str(user.get("phone_number", "")))
                        if hasattr(self, 'lineEditSDT'):
                            self.lineEditSDT.setText(str(user.get("phone_number", "")))

                        print("--- Nạp dữ liệu thành công!")
                    else:
                        print("--- File JSON trống (không có Datasets)")
            else:
                print(f"--- KHÔNG tìm thấy file tại: {file_path}")

        except Exception as e:
            print(f"--- Lỗi nạp dữ liệu user: {e}")

        except Exception as e:
            print(f"Lỗi nạp dữ liệu user: {e}")

    def set_payment_info(self, ten_goi, gia):
        """Nhận dữ liệu từ màn hình Đăng ký truyền sang"""
        self.original_price = gia
        self.lineEditPackage.setText(ten_goi)
        self.lineEditTime.setText("Theo gói đã chọn")

        # Mặc định ban đầu
        self.radioButtonFull.setChecked(True)
        self.update_price_display()

        # Tự động điền tên và SĐT từ file JSON
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
        """Xử lý khi nhấn nút Xác nhận thanh toán"""
        ten = self.lineEditName.text().strip()

        # Kiểm tra xem đã chọn phương thức thanh toán chưa
        if not self.checkBoxBak.isChecked() and not self.checkBoxCard.isChecked():
            QMessageBox.warning(self.MainWindow, "Thông báo", "Vui lòng chọn phương thức thanh toán!")
            return

        if not ten:
            QMessageBox.warning(self.MainWindow, "Thông báo", "Vui lòng kiểm tra lại thông tin khách hàng!")
            return

        # Thông báo thành công
        QMessageBox.information(self.MainWindow, "Thành công", f"Giao dịch của khách hàng {ten} đã được ghi nhận!")
        # self.MainWindow.close() # Mở dòng này nếu muốn đóng cửa sổ sau khi xong

    def set_booking_info(self, goi_tap, thoi_gian, phong, gia):
        """Nhận dữ liệu chi tiết từ màn hình Đặt lịch truyền sang"""
        self.original_price = gia

        # Vì form Payment không có ô chứa Phòng riêng, ta gộp nó vào tên Gói tập hiển thị cho đẹp
        goi_tap_kem_phong = f"{goi_tap} - {phong}"

        self.lineEditPackage.setText(goi_tap_kem_phong)
        self.lineEditTime.setText(thoi_gian)

        # Mặc định ban đầu chọn Trả 100%
        self.radioButtonFull.setChecked(True)
        self.update_price_display()

        # Tự động nạp dữ liệu user
        self.load_user_data()

    def showWindow(self):
        """Hiển thị full màn hình"""
        self.MainWindow.showMaximized()