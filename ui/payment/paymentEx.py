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
        self.loai_thanh_toan = "membership"
        """Nhận dữ liệu từ màn hình Đăng ký truyền sang"""
        self.original_price = gia
        self.lineEditPackage.setText(ten_goi)
        self.lineEditTime.setText("Theo gói đã chọn")

        # Mặc định ban đầu
        self.radioButtonFull.setChecked(True)
        self.update_price_display()

        # GỌI HÀM NẠP DỮ LIỆU TỪ SESSION
        self.load_user_data()
    def set_booking_info(self, goi_tap, thoi_gian, phong, gia):
        self.loai_thanh_toan = "booking"
        """Nhận dữ liệu chi tiết từ màn hình Đặt lịch truyền sang"""
        self.original_price = gia
        self.room_name = phong

        # Vì form Payment không có ô chứa Phòng riêng, ta gộp nó vào tên Gói tập hiển thị cho đẹp
        goi_tap_kem_phong = f"{goi_tap} - {phong}"

        self.lineEditPackage.setText(goi_tap_kem_phong)
        self.lineEditTime.setText(thoi_gian)

        # Mặc định ban đầu chọn Trả 100%
        self.radioButtonFull.setChecked(True)
        self.update_price_display()

        # Tự động nạp dữ liệu user
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
        """Xử lý khi nhấn nút Xác nhận thanh toán và Lưu JSON"""
        from datetime import datetime

        ten = self.lineEditName.text().strip()
        sdt = ""
        if hasattr(self, 'lineEditID'):
            sdt = self.lineEditID.text().strip()

        if not self.checkBoxBak.isChecked() and not self.checkBoxCard.isChecked():
            QMessageBox.warning(self.MainWindow, "Thông báo", "Vui lòng chọn phương thức thanh toán!")
            return

        if not ten:
            QMessageBox.warning(self.MainWindow, "Thông báo", "Thiếu thông tin khách hàng!")
            return

        phuong_thuc = "Ngân hàng" if self.checkBoxBak.isChecked() else "Thẻ tín dụng"

        # Dữ liệu chung cho cả 2 hóa đơn
        bill_data = {
            "customer_name": ten,
            "phone": sdt,
            "package_details": self.lineEditPackage.text(),
            "time": self.lineEditTime.text(),
            "total_paid": self.lineEditTotalMoney.text(),
            "payment_method": phuong_thuc,
            "payment_time": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }

        # Đường dẫn thư mục
        current_file_path = os.path.abspath(__file__)
        project_root = current_file_path.split("ui")[0]
        datasets_dir = os.path.join(project_root, "datasets")

        # 👉 XỬ LÝ RẼ NHÁNH TẠI ĐÂY
        if getattr(self, 'loai_thanh_toan', 'booking') == "booking":
            # 1. LƯU VÀO BOOKING_HISTORY
            history_file = os.path.join(datasets_dir, "booking_history.json")
            history_list = []
            if os.path.exists(history_file):
                try:
                    with open(history_file, 'r', encoding='utf-8') as f:
                        history_list = json.load(f)
                except Exception:
                    pass

            history_list.append(bill_data)
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(history_list, f, indent=4, ensure_ascii=False)

            # 2. CẬP NHẬT PHÒNG
            if hasattr(self, 'room_name') and self.room_name:
                room_file = os.path.join(datasets_dir, "room.json")
                if os.path.exists(room_file):
                    try:
                        with open(room_file, 'r', encoding='utf-8') as f:
                            rooms = json.load(f)
                        for r in rooms:
                            if r.get("name") == self.room_name:
                                r["current_user"] = r.get("current_user", 0) + 1
                                break
                        with open(room_file, 'w', encoding='utf-8') as f:
                            json.dump(rooms, f, indent=4, ensure_ascii=False)
                    except Exception:
                        pass

        elif self.loai_thanh_toan == "membership":
            # 👉 NẾU LÀ MUA GÓI HỘI VIÊN THÌ LƯU VÀO FILE KHÁC (VD: membership_history.json)
            member_file = os.path.join(datasets_dir, "membership_history.json")
            member_list = []
            if os.path.exists(member_file):
                try:
                    with open(member_file, 'r', encoding='utf-8') as f:
                        member_list = json.load(f)
                except Exception:
                    pass

            member_list.append(bill_data)
            with open(member_file, 'w', encoding='utf-8') as f:
                json.dump(member_list, f, indent=4, ensure_ascii=False)

            # (Tùy chọn: Sau này mày có thể viết thêm code update cột 'status' của user trong users.json ở đây)

        # Chuyển trang
        QMessageBox.information(self.MainWindow, "Thành công", "Thanh toán thành công!")
        self.mo_man_hinh_confirm()

    def mo_man_hinh_confirm(self):
        from ui.confirm.ConfirmEx import ConfirmEx
        self.confirm_window = QMainWindow()
        self.confirm_ui = ConfirmEx()
        self.confirm_ui.setupUi(self.confirm_window)
        self.confirm_ui.showWindow()
        self.MainWindow.hide()



    def showWindow(self):
        """Hiển thị full màn hình"""
        self.MainWindow.showMaximized()