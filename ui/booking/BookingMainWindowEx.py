import os
import sys
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtCore import Qt
from models.trainers import Trainers
from ui.booking.booking import Ui_MainWindow
from models.rooms import Rooms
from PyQt6.QtCore import QDate
from ui.payment.paymentEx import PaymentEx
import json


class BookingMainWindowEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow

        # --- ĐOẠN KHỞI TẠO ĐƯỜNG DẪN CHUẨN ---
        if getattr(sys, 'frozen', False):
            # Nếu đang chạy bằng file .exe
            self.BASE_DIR = os.path.dirname(sys.executable)
        else:
            # Nếu đang chạy code bình thường
            self.BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

        self.DATASETS_DIR = os.path.join(self.BASE_DIR, "Datasets")
        # ---------------------------------------

        # Cài ảnh nền (Đã thêm dấu nháy '')
        img_path = os.path.join(self.BASE_DIR, "images", "Booking.png").replace("\\", "/")
        self.centralwidget.setStyleSheet(f"#centralwidget {{ border-image: url('{img_path}'); }}")

        # Cài đặt màu bôi đen cho ListWidget
        list_style = """
            QListWidget::item:selected {
                background-color: #1A483E; 
                color: white;
                border-radius: 4px;
            }
        """
        self.listWidgetHuanLuyenVien.setStyleSheet(list_style)

        # 1. Đọc file JSON HLV bằng đường dẫn chuẩn
        self.danh_sach_hlv = Trainers()
        json_path = os.path.join(self.DATASETS_DIR, "trainer.json")
        self.danh_sach_hlv.import_json(json_path)

        self.comboBoxHuanLuyenVien.currentTextChanged.connect(self.dong_bo_combobox_va_list)

        # Trạng thái mặc định
        self.xuly_an_hien_pt()

        # 2. Đọc file JSON Phòng bằng đường dẫn chuẩn
        self.danh_sach_phong = Rooms()
        json_phong_path = os.path.join(self.DATASETS_DIR, "room.json")
        self.danh_sach_phong.import_json(json_phong_path)

        self.SetupSignalAndSlots()

        ## Thiết lập ngày mặc định luôn là NGÀY HÔM NAY (Thời gian thực)
        default_date = QDate.currentDate()
        self.dateEdit.setDate(default_date)

    def SetupSignalAndSlots(self):
        self.radioButtonYes.toggled.connect(self.xuly_an_hien_pt)
        self.radioButtonNo.toggled.connect(self.xuly_an_hien_pt)

        # Bắt sự kiện click chọn Môn học
        self.radioButtonYoga.toggled.connect(self.xuly_loc_danh_sach_pt)
        self.radioButtonPilates.toggled.connect(self.xuly_loc_danh_sach_pt)
        self.radioButtonBoxing.toggled.connect(self.xuly_loc_danh_sach_pt)

        # 👉 BẮT SỰ KIỆN KHI THAY ĐỔI NGÀY VÀ GIỜ
        # Với DateEdit thì phải xài dateChanged
        self.dateEdit.dateChanged.connect(self.xuly_loc_danh_sach_pt)
        # Với ComboBox thì xài currentTextChanged
        self.comboBoxTime.currentTextChanged.connect(self.xuly_loc_danh_sach_pt)
        self.dateEdit.dateChanged.connect(self.cap_nhat_danh_sach_phong)
        self.comboBoxTime.currentTextChanged.connect(self.cap_nhat_danh_sach_phong)

        # Bắt sự kiện khi thay đổi lựa chọn trong ComboBox HLV
        self.comboBoxHuanLuyenVien.currentTextChanged.connect(self.dong_bo_combobox_va_list)
        if hasattr(self, 'radioButtonTudo'):
            self.radioButtonTudo.toggled.connect(self.cap_nhat_danh_sach_phong)
        self.radioButtonYoga.toggled.connect(self.cap_nhat_danh_sach_phong)
        self.radioButtonPilates.toggled.connect(self.cap_nhat_danh_sach_phong)
        self.radioButtonBoxing.toggled.connect(self.cap_nhat_danh_sach_phong)
        self.pushButtonDoneBooking.clicked.connect(self.mo_man_hinh_thanh_toan)
        self.pushButtonCancelBooking.clicked.connect(self.tro_ve_dashboard)
        self.comboBoxRoom.currentTextChanged.connect(self.cap_nhat_label_so_luong)

    def showWindow(self):
        self.MainWindow.show()

    # ==============================================================
    # 🔥 PHẦN 2: LOGIC LỌC DATA 3 LỚP (MÔN + NGÀY + GIỜ)
    # ==============================================================

    def xuly_an_hien_pt(self):
        if self.radioButtonNo.isChecked():
            self.comboBoxHuanLuyenVien.setEnabled(False)
            self.listWidgetHuanLuyenVien.setEnabled(False)
            self.comboBoxHuanLuyenVien.clear()
            self.listWidgetHuanLuyenVien.clear()
        else:
            self.comboBoxHuanLuyenVien.setEnabled(True)
            self.listWidgetHuanLuyenVien.setEnabled(True)
            self.xuly_loc_danh_sach_pt()

    def get_mon_tap_dang_chon(self):
        if hasattr(self, 'radioButtonTudo') and self.radioButtonTudo.isChecked(): return "Tự do"
        if self.radioButtonYoga.isChecked(): return "Yoga"
        if self.radioButtonPilates.isChecked(): return "Pilates"
        if self.radioButtonBoxing.isChecked(): return "Boxing"
        return ""

    def xuly_loc_danh_sach_pt(self):
        # 1. Bỏ qua nếu chọn "Không HLV"
        if self.radioButtonNo.isChecked():
            return

        # 2. Bỏ qua nếu chưa tick môn nào
        mon_tap = self.get_mon_tap_dang_chon()
        if mon_tap == "" or mon_tap == "Tự do":
            return

        # 3. LẤY NGÀY ĐANG CHỌN VÀ DỊCH SANG "THỨ"
        qdate_dang_chon = self.dateEdit.date()
        gio_dang_chon = self.comboBoxTime.currentText()

        # dayOfWeek() trả về số từ 1 (Thứ 2) đến 7 (Chủ nhật)
        weekday_num = qdate_dang_chon.dayOfWeek()
        thu_map = {
            1: "Thứ 2", 2: "Thứ 3", 3: "Thứ 4",
            4: "Thứ 5", 5: "Thứ 6", 6: "Thứ 7", 7: "Chủ nhật"
        }
        thu_dang_chon = thu_map.get(weekday_num)

        # Chặn tín hiệu để reset danh sách không bị lỗi
        self.comboBoxHuanLuyenVien.blockSignals(True)
        self.comboBoxHuanLuyenVien.clear()
        self.listWidgetHuanLuyenVien.clear()

        self.comboBoxHuanLuyenVien.addItem(f"-- Chọn PT môn {mon_tap} --")

        # 4. Quét JSON: Kiểm tra ĐÚNG MÔN + RẢNH 'THỨ' ĐÓ + RẢNH GIỜ NÀY
        for hlv in self.danh_sach_hlv.list:
            dieu_kien_mon = (hlv.status == mon_tap)
            # 👉 Đổi chỗ này: So sánh THỨ đang chọn với lịch rảnh trong JSON
            dieu_kien_ngay = (thu_dang_chon in hlv.available_dates)
            # Giữ nguyên kiểm tra giờ
            dieu_kien_gio = (gio_dang_chon in hlv.available_times)

            # Nếu thỏa mãn cả 3 thì mới cho hiện lên bảng
            if dieu_kien_mon and dieu_kien_ngay and dieu_kien_gio:
                hien_thi = f"{hlv.username} ({hlv.status})"
                self.comboBoxHuanLuyenVien.addItem(hien_thi)
                self.listWidgetHuanLuyenVien.addItem(hien_thi)

        self.comboBoxHuanLuyenVien.blockSignals(False)

    def dong_bo_combobox_va_list(self, text):
        if "-- Chọn PT" in text or text == "":
            self.listWidgetHuanLuyenVien.clearSelection()
            return

        items_tim_thay = self.listWidgetHuanLuyenVien.findItems(text, Qt.MatchFlag.MatchExactly)
        if items_tim_thay:
            item_can_chon = items_tim_thay[0]
            self.listWidgetHuanLuyenVien.setCurrentItem(item_can_chon)

    def cap_nhat_danh_sach_phong(self):
        mon_tap = self.get_mon_tap_dang_chon()
        if mon_tap == "":
            return

        # Chặn signal tạm thời để không bị lỗi khi clear()
        self.comboBoxRoom.blockSignals(True)
        self.comboBoxRoom.clear()

        # Quét các phòng phù hợp với môn tập
        for phong in self.danh_sach_phong.list:
            if phong.category == mon_tap:
                self.comboBoxRoom.addItem(phong.name)

        self.comboBoxRoom.blockSignals(False)

        # Sau khi nạp phòng xong, gọi luôn hàm cập nhật cái Label Số Lượng bên cạnh
        self.cap_nhat_label_so_luong()

    def mo_man_hinh_thanh_toan(self):
        # 1. Lấy thông tin từ giao diện Đặt lịch
        mon_tap = self.get_mon_tap_dang_chon()
        ngay_tap = self.dateEdit.date().toString("dd/MM/yyyy")
        gio_tap = self.comboBoxTime.currentText()

        phong_text = self.comboBoxRoom.currentText()
        phong = phong_text.split(" (")[0] if " (" in phong_text else phong_text

        # Validate xem người dùng đã chọn đủ chưa
        if mon_tap == "" or phong == "":
            QMessageBox.warning(self.MainWindow, "Thiếu thông tin", "Vui lòng chọn lĩnh vực và phòng tập!")
            return

        # 2. Xử lý chuỗi thông tin để hiển thị đẹp bên Payment
        thoi_gian_day_du = f"{gio_tap} ngày {ngay_tap}"
        goi_tap_hien_thi = f"Gói: {mon_tap}"

        # Nếu có thuê PT, nối thêm tên PT vào Gói tập
        if self.radioButtonYes.isChecked():
            ten_pt = self.comboBoxHuanLuyenVien.currentText()
            if ten_pt and "-- Chọn PT" not in ten_pt:
                goi_tap_hien_thi += f" (HLV: {ten_pt})"
            else:
                QMessageBox.warning(self.MainWindow, "Thiếu thông tin", "Vui lòng chọn Huấn luyện viên!")
                return

        # 3. Tính giá tiền (Bạn có thể custom lại logic giá ở đây)
        # Giả sử mặc định là 500k, thuê PT thì cộng thêm 200k
        gia_tien_tong = 500000
        if self.radioButtonYes.isChecked():
            gia_tien_tong += 200000

        # 4. Khởi tạo và nạp dữ liệu sang màn hình PaymentEx
        self.payment_window = QMainWindow()
        self.payment_ui = PaymentEx()
        self.payment_ui.setupUi(self.payment_window)

        # Gọi hàm set_booking_info (đã hướng dẫn bạn tạo ở tin nhắn trước bên file PaymentEx)
        self.payment_ui.set_booking_info(goi_tap_hien_thi, thoi_gian_day_du, phong, gia_tien_tong)

        # 5. Hiển thị màn hình Payment và ẩn/đóng màn hình Đặt lịch
        self.payment_window.showMaximized()
        self.MainWindow.hide()

    def tro_ve_dashboard(self):
        # 1. Hiện hộp thoại hỏi xác nhận trước
        reply = QMessageBox.question(
            self.MainWindow,
            "Xác nhận hủy",
            "Bạn có chắc chắn muốn hủy thao tác đặt lịch và quay về trang chủ không?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No  # Mặc định trỏ chuột vào nút No cho an toàn
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Nếu chọn Yes, thực hiện code quay về Dashboard như cũ
            from ui.dashboard.DashboardEx import DashboardEx

            self.dashboard_window = QMainWindow()
            self.dashboard_ui = DashboardEx()
            self.dashboard_ui.setupUi(self.dashboard_window)

            self.dashboard_window.showMaximized()
            self.dashboard_ui.showWindow()

            self.MainWindow.close()

    def cap_nhat_label_so_luong(self):
        ten_phong = self.comboBoxRoom.currentText()


        if ten_phong == "":
            self.labelSoLuong.setText("...")
            return

        so_nguoi_hien_tai = 0
        capacity = 20


        for phong in self.danh_sach_phong.list:
            if phong.name == ten_phong:

                so_nguoi_hien_tai = getattr(phong, 'current_user', 0)
                capacity = getattr(phong, 'capacity', 20)
                break


        hien_thi = f"{so_nguoi_hien_tai}/{capacity}"
        if so_nguoi_hien_tai >= capacity:
            hien_thi += " (ĐẦY)"

        self.labelSoLuong.setText(hien_thi)