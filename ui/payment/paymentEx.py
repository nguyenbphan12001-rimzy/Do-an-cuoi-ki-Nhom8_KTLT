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
        """Xử lý: Lưu dữ liệu hội viên -> Hiện thông báo -> Mở màn hình Confirm"""
        ten = self.lineEditName.text().strip()

        # Kiểm tra xem UI của bạn dùng lineEditID hay lineEditSDT cho số điện thoại
        sdt = ""
        if hasattr(self, 'lineEditID'):
            sdt = self.lineEditID.text().strip()
        elif hasattr(self, 'lineEditSDT'):
            sdt = self.lineEditSDT.text().strip()

        # 1. Kiểm tra điều kiện (Validate)
        if not self.checkBoxBak.isChecked() and not self.checkBoxCard.isChecked():
            QMessageBox.warning(self.MainWindow, "Thông báo", "Vui lòng chọn phương thức thanh toán!")
            return

        if not ten:
            QMessageBox.warning(self.MainWindow, "Thông báo", "Thiếu thông tin khách hàng!")
            return

        # --- BƯỚC QUAN TRỌNG: Ghi dữ liệu vào member.json trước khi hiện thông báo ---
        ten_goi = self.lineEditPackage.text()
        self.save_to_member_database(ten, sdt, ten_goi)
        # --------------------------------------------------------------------------

        # 2. Hiển thị thông báo thành công
        phuong_thuc = "Ngân hàng" if self.checkBoxBak.isChecked() else "Thẻ tín dụng"
        msg = f"Khách hàng: {ten}\nSĐT: {sdt}\nGói: {ten_goi}\nThanh toán thành công qua {phuong_thuc}!"
        QMessageBox.information(self.MainWindow, "Thành công", msg)

        # 3. Mở màn hình Confirm bự (Code cũ của bạn)
        try:
            from ui.confirm.ConfirmEx import ConfirmEx
            self.confirm_window = QMainWindow()
            self.confirm_ui = ConfirmEx()
            self.confirm_ui.setupUi(self.confirm_window)
            self.confirm_ui.showWindow()
            self.MainWindow.close()
        except Exception as e:
            print(f"Lỗi chuyển màn hình: {e}")

    def save_to_member_database(self, username, phone, package):
        """Hàm thực hiện ghi file JSON - Đã sửa khớp với cấu trúc {'Datasets': [...]}"""
        import json
        from datetime import datetime, timedelta

        # 1. Xác định đường dẫn tuyệt đối đến file
        current_file_path = os.path.abspath(__file__)
        project_root = current_file_path.split("ui")[0]
        member_file = os.path.join(project_root, "Datasets", "member.json")

        # 2. Chuẩn bị dữ liệu mới
        ngay_het_han = (datetime.now() + timedelta(days=30)).strftime("%d/%m/%Y")
        new_member_obj = {
            "username": username,
            "phone_number": phone,
            "package": package,
            "gender": "M",
            "expire_date": ngay_het_han
        }

        try:
            # 3. Đọc dữ liệu cũ
            full_data = {"Datasets": []}  # Mặc định cấu trúc nếu file trống
            if os.path.exists(member_file):
                with open(member_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        temp = json.loads(content)
                        # Đảm bảo temp là dictionary và có khóa Datasets
                        if isinstance(temp, dict) and "Datasets" in temp:
                            full_data = temp

            # 4. Lấy danh sách hội viên ra để xử lý
            member_list = full_data.get("Datasets", [])

            # 5. Kiểm tra cập nhật hoặc thêm mới
            is_existing = False
            for m in member_list:
                # Kiểm tra m là dict để tránh lỗi 'str' object
                if isinstance(m, dict) and m.get('username') == username:
                    m['package'] = package
                    m['phone_number'] = phone
                    m['expire_date'] = ngay_het_han
                    is_existing = True
                    break

            if not is_existing:
                member_list.append(new_member_obj)

            # 6. Ghi ngược lại vào file với đúng cấu trúc gốc
            full_data["Datasets"] = member_list
            with open(member_file, 'w', encoding='utf-8') as f:
                json.dump(full_data, f, indent=4, ensure_ascii=False)

            print(f"✅ Đã cập nhật thành công hội viên {username} vào Datasets.")

        except Exception as e:
            print(f"❌ Lỗi ghi file member.json: {e}")

    def save_to_member_list(self, username, phone, package):
        """Hàm phụ trợ để ghi dữ liệu hội viên vào file hệ thống"""
        from datetime import datetime, timedelta

        # Lấy đường dẫn chuẩn đến file member.json
        current_file_path = os.path.abspath(__file__)
        project_root = current_file_path.split("ui")[0]
        member_file = os.path.join(project_root, "Datasets", "member.json")

        # Tính ngày hết hạn (mặc định 30 ngày kể từ hôm nay)
        expire_date = (datetime.now() + timedelta(days=30)).strftime("%d/%m/%Y")

        new_member_data = {
            "username": username,
            "phone_number": phone,
            "package": package,
            "gender": "M",  # Mặc định là Nam, user có thể sửa ở trang Member sau
            "expire_date": expire_date
        }

        try:
            data = []
            # Đọc dữ liệu cũ nếu file đã tồn tại
            if os.path.exists(member_file):
                with open(member_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        data = json.loads(content)

            # Kiểm tra nếu là Member cũ thì cập nhật gói, nếu mới thì append
            found = False
            for m in data:
                if m.get('username') == username:
                    m['package'] = package
                    m['phone_number'] = phone
                    m['expire_date'] = expire_date
                    found = True
                    break

            if not found:
                data.append(new_member_data)

            # Ghi lại vào file JSON
            with open(member_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"✅ Đã cập nhật Member: {username} vào file {member_file}")

        except Exception as e:
            print(f"❌ Lỗi khi lưu dữ liệu hội viên: {e}")

    def showWindow(self):
        """Hiển thị full màn hình"""
        self.MainWindow.showMaximized()