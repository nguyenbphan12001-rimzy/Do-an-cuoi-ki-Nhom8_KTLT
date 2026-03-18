import os
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtCore import Qt
from models.trainers import Trainers
from ui.booking.booking import Ui_MainWindow
from models.rooms import Rooms
from PyQt6.QtCore import QDate  # Đảm bảo có QDate ở đây
from ui.payment.paymentEx import PaymentEx

class BookingMainWindowEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow

        # Cài ảnh nền
        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.abspath(os.path.join(current_dir, "..", "..", "images", "Booking.png")).replace("\\", "/")
        self.centralwidget.setStyleSheet(f"#centralwidget {{ border-image: url({img_path}); }}")

        # Cài đặt màu bôi đen cho ListWidget
        list_style = """
            QListWidget::item:selected {
                background-color: #1A483E; 
                color: white;
                border-radius: 4px;
            }
        """
        self.listWidgetHuanLuyenVien.setStyleSheet(list_style)

        # 1. Đọc file JSON HLV
        self.danh_sach_hlv = Trainers()
        json_path = os.path.abspath(os.path.join(current_dir, "..", "..", "Datasets", "trainer.json")).replace("\\",
                                                                                                               "/")
        self.danh_sach_hlv.import_json(json_path)


        self.comboBoxHuanLuyenVien.currentTextChanged.connect(self.dong_bo_combobox_va_list)

        # Trạng thái mặc định
        self.xuly_an_hien_pt()
        # 2. Đọc file JSON Phòng (MỚI THÊM)
        self.danh_sach_phong = Rooms()
        json_phong_path = os.path.abspath(os.path.join(current_dir, "..", "..", "Datasets", "room.json")).replace("\\",
                                                                                                                  "/")
        self.danh_sach_phong.import_json(json_phong_path)
        self.SetupSignalAndSlots()


        # ... (các dòng kết nối nút Lĩnh vực) ...
        # Thiết lập ngày mặc định là 18/03/2026
        default_date = QDate(2026, 3, 18)
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

        # Bắt sự kiện khi thay đổi lựa chọn trong ComboBox HLV
        self.comboBoxHuanLuyenVien.currentTextChanged.connect(self.dong_bo_combobox_va_list)
        if hasattr(self, 'radioButtonTudo'):
            self.radioButtonTudo.toggled.connect(self.cap_nhat_danh_sach_phong)
        self.radioButtonYoga.toggled.connect(self.cap_nhat_danh_sach_phong)
        self.radioButtonPilates.toggled.connect(self.cap_nhat_danh_sach_phong)
        self.radioButtonBoxing.toggled.connect(self.cap_nhat_danh_sach_phong)
        self.pushButtonDoneBooking.clicked.connect(self.mo_man_hinh_thanh_toan)

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
        if mon_tap == "":
            return

            # 3. Lấy giá trị Ngày và Giờ đang hiển thị
        ngay_dang_chon = self.dateEdit.date().toString("dd/MM/yyyy")
        gio_dang_chon = self.comboBoxTime.currentText()

        # Chặn tín hiệu để reset danh sách không bị lỗi
        self.comboBoxHuanLuyenVien.blockSignals(True)
        self.comboBoxHuanLuyenVien.clear()
        self.listWidgetHuanLuyenVien.clear()

        self.comboBoxHuanLuyenVien.addItem(f"-- Chọn PT môn {mon_tap} --")

        # 4. Quét JSON: Kiểm tra ĐÚNG MÔN + RẢNH NGÀY NÀY + RẢNH GIỜ NÀY
        for hlv in self.danh_sach_hlv.list:
            dieu_kien_mon = (hlv.status == mon_tap)
            # Kiểm tra xem ngay_dang_chon có nằm trong mảng available_dates không
            dieu_kien_ngay = (ngay_dang_chon in hlv.available_dates)
            # Kiểm tra xem gio_dang_chon có nằm trong mảng available_times không
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

    def get_mon_tap_dang_chon(self):
        if hasattr(self, 'radioButtonTudo') and self.radioButtonTudo.isChecked(): return "Tự do"
        if self.radioButtonYoga.isChecked(): return "Yoga"
        if self.radioButtonPilates.isChecked(): return "Pilates"
        if self.radioButtonBoxing.isChecked(): return "Boxing"
        return ""

    def cap_nhat_danh_sach_phong(self):
        mon_tap = self.get_mon_tap_dang_chon()
        if mon_tap == "":
            return

        # Đổi tên self.comboBoxRoom thành tên chuẩn trong Qt Designer của mày nếu khác nhé
        self.comboBoxRoom.clear()

        # Quét data trong room.json, trùng môn nào thì ném tên phòng đó vào ComboBox
        for phong in self.danh_sach_phong.list:
            if phong.category == mon_tap:
                self.comboBoxRoom.addItem(phong.name)

    def mo_man_hinh_thanh_toan(self):
        # 1. Lấy thông tin từ giao diện Đặt lịch
        mon_tap = self.get_mon_tap_dang_chon()
        ngay_tap = self.dateEdit.date().toString("dd/MM/yyyy")
        gio_tap = self.comboBoxTime.currentText()
        phong = self.comboBoxRoom.currentText()

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
        self.payment_ui.showWindow()
        self.MainWindow.hide()  # Dùng close() nếu không muốn quay lại màn này nữa


