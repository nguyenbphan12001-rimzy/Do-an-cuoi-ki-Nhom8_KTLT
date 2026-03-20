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
            current_file_path = os.path.abspath(__file__)
            project_root = current_file_path.split("ui")[0]
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
        self.loai_thanh_toan = "membership"
        self.original_price = gia
        # Vô hiệu hóa nút Cọc 50% vì Đăng ký hội viên phải trả 100%
        if hasattr(self, 'radioButtonHalf'):
            self.radioButtonHalf.setEnabled(False)

        # Gọt bỏ chữ "Gói " dư thừa
        clean_ten_goi = ten_goi.replace("Gói ", "").strip()
        self.lineEditPackage.setText(clean_ten_goi)

        # Thanh toán hội viên thì không có phòng
        if hasattr(self, 'lineEditRoom'):
            self.lineEditRoom.setText("N/A")
        elif hasattr(self, 'lineEditPhong'):
            self.lineEditPhong.setText("N/A")

        self.lineEditTime.setText("Theo gói đã chọn")
        self.radioButtonFull.setChecked(True)
        self.update_price_display()
        self.load_user_data()

    def set_booking_info(self, goi_tap, thoi_gian, phong, gia):
        """Nhận dữ liệu chi tiết từ màn hình Đặt lịch (Booking) truyền sang"""
        self.loai_thanh_toan = "booking"
        self.original_price = gia
        self.room_name = phong

        # Kích hoạt lại nút Cọc 50%
        if hasattr(self, 'radioButtonHalf'):
            self.radioButtonHalf.setEnabled(True)
        # Gọt bỏ chữ "Gói " dư thừa
        clean_goi_tap = goi_tap.replace("Gói ", "").strip()
        self.lineEditPackage.setText(clean_goi_tap)

        # Đẩy phòng xuống LineEdit bên dưới
        if hasattr(self, 'lineEditRoom'):
            self.lineEditRoom.setText(phong)
        elif hasattr(self, 'lineEditPhong'):
            self.lineEditPhong.setText(phong)

        self.lineEditTime.setText(thoi_gian)
        self.radioButtonFull.setChecked(True)
        self.update_price_display()
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
        """Xử lý khi nhấn nút Xác nhận thanh toán (Đã tách rạch ròi 2 bên)"""
        try:
            from datetime import datetime, timedelta

            ten = self.lineEditName.text().strip()
            sdt = ""
            if hasattr(self, 'lineEditSDT'):
                sdt = self.lineEditSDT.text().strip()
            elif hasattr(self, 'lineEditSDT'):
                sdt = self.lineEditSDT.text().strip()

            if not self.checkBoxBak.isChecked() and not self.checkBoxCard.isChecked():
                QMessageBox.warning(self.MainWindow, "Thông báo", "Vui lòng chọn phương thức thanh toán!")
                return

            if not ten:
                QMessageBox.warning(self.MainWindow, "Thông báo", "Thiếu thông tin khách hàng!")
                return

            phuong_thuc = "Ngân hàng" if self.checkBoxBak.isChecked() else "Thẻ tín dụng"
            loai = getattr(self, 'loai_thanh_toan', 'booking')

            current_file_path = os.path.abspath(__file__)
            datasets_dir = os.path.join(current_file_path.split("ui")[0], "datasets")

            # 👉 CHIA LÀM 2 NGÃ RẼ RÕ RÀNG:

            if loai == "booking":
                # ---------------------------------------------------------
                # HƯỚNG 1: ĐẶT LỊCH TẬP (Chỉ lưu vào booking_history.json và cập nhật room)
                # ---------------------------------------------------------
                chi_tiet_goi = self.lineEditPackage.text()
                if getattr(self, 'room_name', ''):
                    chi_tiet_goi = f"{chi_tiet_goi} - {self.room_name}"

                bill_data = {
                    "customer_name": ten,
                    "phone": sdt,
                    "package_details": chi_tiet_goi,
                    "time": self.lineEditTime.text(),
                    "total_paid": self.lineEditTotalMoney.text(),
                    "payment_method": phuong_thuc,
                    "payment_time": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                }

                # Lưu vào booking_history
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

                # Cập nhật số người trong phòng
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

            elif loai == "membership":
                # ---------------------------------------------------------
                # HƯỚNG 2: ĐĂNG KÝ HỘI VIÊN (Chỉ lưu vào member.json)
                # ---------------------------------------------------------
                member_file = os.path.join(datasets_dir, "member.json")
                member_data = {"Datasets": []}
                if os.path.exists(member_file):
                    try:
                        with open(member_file, 'r', encoding='utf-8') as f:
                            member_data = json.load(f)
                    except Exception:
                        pass

                ds_hoi_vien = member_data.get("Datasets", [])
                new_id_num = 1
                if len(ds_hoi_vien) > 0:
                    try:
                        new_id_num = int(ds_hoi_vien[-1].get("id", "000")) + 1
                    except ValueError:
                        pass

                ngay_dang_ky = datetime.now()
                ten_goi_tap = self.lineEditPackage.text()

                if "2 tuần" in ten_goi_tap:
                    ngay_het_han = ngay_dang_ky + timedelta(days=14)
                elif "1 tháng" in ten_goi_tap:
                    ngay_het_han = ngay_dang_ky + timedelta(days=30)
                elif "3 tháng" in ten_goi_tap:
                    ngay_het_han = ngay_dang_ky + timedelta(days=90)
                elif "6 tháng" in ten_goi_tap:
                    ngay_het_han = ngay_dang_ky + timedelta(days=180)
                elif "1 năm" in ten_goi_tap:
                    ngay_het_han = ngay_dang_ky + timedelta(days=365)
                else:
                    ngay_het_han = ngay_dang_ky

                new_member = {
                    "username": ten,
                    "id": f"{new_id_num:03d}",
                    "phone_number": sdt,
                    "gender": "Unknown",
                    "serve": ten_goi_tap,
                    "register_date": ngay_dang_ky.strftime("%d/%m/%Y"),
                    "expire_date": ngay_het_han.strftime("%d/%m/%Y")
                }

                ds_hoi_vien.append(new_member)
                member_data["Datasets"] = ds_hoi_vien
                with open(member_file, 'w', encoding='utf-8') as f:
                    json.dump(member_data, f, indent=4, ensure_ascii=False)

            # 3. KẾT THÚC THÀNH CÔNG VÀ CHUYỂN MÀN HÌNH
                    # Gom tất cả thông tin đã lấy được ở trên vào một chuỗi
                    thong_tin_chi_tiet = (
                        f"✅ THANH TOÁN THÀNH CÔNG!\n\n"
                        f"👤 Khách hàng: {ten}\n"
                        f"📞 Số điện thoại: {sdt}\n"
                        f"📦 Gói dịch vụ: {self.lineEditPackage.text()}\n"
                        f"⏰ Thời gian: {self.lineEditTime.text()}\n"
                        f"💰 Tổng tiền: {self.lineEditTotalMoney.text()}\n"
                        f"💳 Hình thức: {phuong_thuc}\n\n"
                        f"Hệ thống đã cập nhật dữ liệu thành công."
                    )

                    # Hiển thị thông báo với đầy đủ chi tiết
                    QMessageBox.information(self.MainWindow, "Xác nhận giao dịch", thong_tin_chi_tiet)

                    self.mo_man_hinh_confirm()
        except Exception as e:
            import traceback
            QMessageBox.critical(self.MainWindow, "Lỗi Hệ Thống", f"Bị lỗi rồi bro ơi:\n{e}")
            print(traceback.format_exc())

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