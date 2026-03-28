import json
import os
import sys
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from ui.payment.payment import Ui_MainWindow


class PaymentEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.original_price = 0

        if getattr(sys, 'frozen', False):

            self.BASE_DIR = os.path.dirname(sys.executable)
        else:
            self.BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

        self.DATASETS_DIR = os.path.join(self.BASE_DIR, "Datasets")


        img_path = os.path.join(self.BASE_DIR, "images", "payments.png").replace("\\", "/")
        self.centralwidget.setStyleSheet(f"#centralwidget {{ border-image: url('{img_path}'); }}")

        self.setup_signals()
        self.lineEditTotalMoney.setReadOnly(True)

    def setup_signals(self):
        self.radioButtonHalf.clicked.connect(self.update_price_display)
        self.radioButtonFull.clicked.connect(self.update_price_display)

        self.checkBoxBak.clicked.connect(lambda: self.handle_payment_selection("bank"))
        self.checkBoxCard.clicked.connect(lambda: self.handle_payment_selection("card"))

        self.pushButtonCofirm.clicked.connect(self.process_confirm)

    def load_user_data(self):
        try:
            file_path = os.path.join(self.DATASETS_DIR, "current_user.json")
            print(f"--- Payment đang đọc session tại: {file_path}")

            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    user = json.load(f)

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
        self.original_price = gia
        if hasattr(self, 'radioButtonHalf'):
            self.radioButtonHalf.setEnabled(False)

        clean_ten_goi = ten_goi.replace("Gói ", "").strip()
        self.lineEditPackage.setText(clean_ten_goi)

        if hasattr(self, 'lineEditRoom'):
            self.lineEditRoom.setText("N/A")
        elif hasattr(self, 'lineEditPhong'):
            self.lineEditPhong.setText("N/A")

        self.lineEditTime.setText("Theo gói đã chọn")
        self.radioButtonFull.setChecked(True)
        self.update_price_display()
        self.load_user_data()

    def set_booking_info(self, goi_tap, thoi_gian, phong, gia):
        self.loai_thanh_toan = "booking"
        self.original_price = gia
        self.room_name = phong

        if hasattr(self, 'radioButtonHalf'):
            self.radioButtonHalf.setEnabled(True)
        clean_goi_tap = goi_tap.replace("Gói ", "").strip()
        self.lineEditPackage.setText(clean_goi_tap)

        if hasattr(self, 'lineEditRoom'):
            self.lineEditRoom.setText(phong)
        elif hasattr(self, 'lineEditPhong'):
            self.lineEditPhong.setText(phong)

        self.lineEditTime.setText(thoi_gian)
        self.radioButtonFull.setChecked(True)
        self.update_price_display()
        self.load_user_data()

    def update_price_display(self):
        if self.radioButtonHalf.isChecked():
            current_price = self.original_price / 2
        else:
            current_price = self.original_price
        self.lineEditTotalMoney.setText(f"{int(current_price):,} VNĐ")

    def handle_payment_selection(self, selected_type):
        if selected_type == "bank":
            if self.checkBoxBak.isChecked():
                self.checkBoxCard.setChecked(False)
        else:
            if self.checkBoxCard.isChecked():
                self.checkBoxBak.setChecked(False)

    def process_confirm(self):
        try:
            from datetime import datetime, timedelta

            ten = self.lineEditName.text().strip()
            sdt = ""
            if hasattr(self, 'lineEditSDT'):
                sdt = self.lineEditSDT.text().strip()

            if not self.checkBoxBak.isChecked() and not self.checkBoxCard.isChecked():
                QMessageBox.warning(self.MainWindow, "Thông báo", "Vui lòng chọn phương thức thanh toán!")
                return

            # Đã fix thêm lỗi thiếu số điện thoại để báo cáo cho xịn
            if not ten or not sdt:
                QMessageBox.warning(self.MainWindow, "Thông báo", "Thiếu thông tin tên hoặc số điện thoại khách hàng!")
                return

            phuong_thuc = "Ngân hàng" if self.checkBoxBak.isChecked() else "Thẻ tín dụng"
            loai = getattr(self, 'loai_thanh_toan', 'booking')

            if loai == "booking":

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

                history_file = os.path.join(self.DATASETS_DIR, "booking_history.json")
                history_data = {"Datasets": []}

                if os.path.exists(history_file):
                    try:
                        with open(history_file, 'r', encoding='utf-8') as f:
                            loaded_data = json.load(f)
                            if isinstance(loaded_data, dict) and "Datasets" in loaded_data:
                                history_data = loaded_data
                            elif isinstance(loaded_data, list):
                                history_data["Datasets"] = loaded_data
                    except Exception:
                        pass

                history_data["Datasets"].append(bill_data)

                with open(history_file, 'w', encoding='utf-8') as f:
                    json.dump(history_data, f, indent=4, ensure_ascii=False)

                if hasattr(self, 'room_name') and self.room_name:
                    room_file = os.path.join(self.DATASETS_DIR, "room.json")
                    if os.path.exists(room_file):
                        try:
                            with open(room_file, 'r', encoding='utf-8') as f:
                                room_json = json.load(f)

                            ds_phong = room_json.get("Datasets", room_json) if isinstance(room_json,
                                                                                          dict) else room_json

                            for r in ds_phong:
                                if r.get("name") == self.room_name:
                                    r["current_user"] = r.get("current_user", 0) + 1
                                    break

                            with open(room_file, 'w', encoding='utf-8') as f:
                                json.dump(room_json, f, indent=4, ensure_ascii=False)
                        except Exception as e:
                            print(f"Lỗi cập nhật phòng: {e}")

            elif loai == "membership":

                member_file = os.path.join(self.DATASETS_DIR, "member.json")
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
                    "package": ten_goi_tap,
                    "register_date": ngay_dang_ky.strftime("%d/%m/%Y"),
                    "expire_date": ngay_het_han.strftime("%d/%m/%Y")
                }

                ds_hoi_vien.append(new_member)
                member_data["Datasets"] = ds_hoi_vien

                with open(member_file, 'w', encoding='utf-8') as f:
                    json.dump(member_data, f, indent=4, ensure_ascii=False)

            #Xử lý 50%deposit, lưu lại để có cơ sở tính nợ với khách
            if hasattr(self, 'radioButtonHalf') and self.radioButtonHalf.isChecked():
                tien_da_tra = self.original_price / 2
                tien_con_no = self.original_price - tien_da_tra


                chi_tiet = self.lineEditPackage.text()
                if getattr(self, 'room_name', ''):
                    chi_tiet += f" - {self.room_name}"

                debt_data = {
                    "customer_name": ten,
                    "phone": sdt,
                    "package_details": chi_tiet,
                    "total_price": self.original_price,
                    "paid_amount": tien_da_tra,
                    "remaining_debt": tien_con_no,
                    "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "status": "Pending"
                }

                deposit_file = os.path.join(self.DATASETS_DIR, "50%deposit.json")
                deposit_json = {"Datasets": []}

                if os.path.exists(deposit_file):
                    try:
                        with open(deposit_file, 'r', encoding='utf-8') as f:
                            loaded_deposit = json.load(f)
                            if isinstance(loaded_deposit, dict) and "Datasets" in loaded_deposit:
                                deposit_json = loaded_deposit
                            elif isinstance(loaded_deposit, list):
                                deposit_json["Datasets"] = loaded_deposit
                    except Exception:
                        pass

                deposit_json["Datasets"].append(debt_data)

                with open(deposit_file, 'w', encoding='utf-8') as f:
                    json.dump(deposit_json, f, indent=4, ensure_ascii=False)


            thong_tin_chi_tiet = (
                f"✅ THANH TOÁN THÀNH CÔNG!\n\n"
                f"👤 Khách hàng: {ten}\n"
                f"📞 Số điện thoại: {sdt}\n"
                f"📦 Gói dịch vụ: {self.lineEditPackage.text()}\n"
                f"⏰ Thời gian: {self.lineEditTime.text()}\n"
                f"💰 Tổng tiền đã trả: {self.lineEditTotalMoney.text()}\n"
                f"💳 Hình thức: {phuong_thuc}\n\n"
                f"Hệ thống đã cập nhật dữ liệu thành công."
            )

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
        self.MainWindow.showMaximized()