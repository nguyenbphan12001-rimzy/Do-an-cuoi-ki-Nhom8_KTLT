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


        if getattr(sys, 'frozen', False):

            self.BASE_DIR = os.path.dirname(sys.executable)
        else:

            self.BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

        self.DATASETS_DIR = os.path.join(self.BASE_DIR, "Datasets")



        img_path = os.path.join(self.BASE_DIR, "images", "Booking.png").replace("\\", "/")
        self.centralwidget.setStyleSheet(f"#centralwidget {{ border-image: url('{img_path}'); }}")


        list_style = """
            QListWidget::item:selected {
                background-color: #1A483E; 
                color: white;
                border-radius: 4px;
            }
        """
        self.listWidgetHuanLuyenVien.setStyleSheet(list_style)


        self.danh_sach_hlv = Trainers()
        json_path = os.path.join(self.DATASETS_DIR, "trainer.json")
        self.danh_sach_hlv.import_json(json_path)

        self.comboBoxHuanLuyenVien.currentTextChanged.connect(self.dong_bo_combobox_va_list)


        self.xuly_an_hien_pt()


        self.danh_sach_phong = Rooms()
        json_phong_path = os.path.join(self.DATASETS_DIR, "room.json")
        self.danh_sach_phong.import_json(json_phong_path)

        self.SetupSignalAndSlots()


        default_date = QDate.currentDate()
        self.dateEdit.setDate(default_date)

    def SetupSignalAndSlots(self):
        self.radioButtonYes.toggled.connect(self.xuly_an_hien_pt)
        self.radioButtonNo.toggled.connect(self.xuly_an_hien_pt)


        self.radioButtonYoga.toggled.connect(self.xuly_loc_danh_sach_pt)
        self.radioButtonPilates.toggled.connect(self.xuly_loc_danh_sach_pt)
        self.radioButtonBoxing.toggled.connect(self.xuly_loc_danh_sach_pt)



        self.dateEdit.dateChanged.connect(self.xuly_loc_danh_sach_pt)

        self.comboBoxTime.currentTextChanged.connect(self.xuly_loc_danh_sach_pt)
        self.dateEdit.dateChanged.connect(self.cap_nhat_danh_sach_phong)
        self.comboBoxTime.currentTextChanged.connect(self.cap_nhat_danh_sach_phong)


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

        if self.radioButtonNo.isChecked():
            return


        mon_tap = self.get_mon_tap_dang_chon()
        if mon_tap == "" or mon_tap == "Tự do":
            return


        qdate_dang_chon = self.dateEdit.date()
        gio_dang_chon = self.comboBoxTime.currentText()


        weekday_num = qdate_dang_chon.dayOfWeek()
        thu_map = {
            1: "Thứ 2", 2: "Thứ 3", 3: "Thứ 4",
            4: "Thứ 5", 5: "Thứ 6", 6: "Thứ 7", 7: "Chủ nhật"
        }
        thu_dang_chon = thu_map.get(weekday_num)


        self.comboBoxHuanLuyenVien.blockSignals(True)
        self.comboBoxHuanLuyenVien.clear()
        self.listWidgetHuanLuyenVien.clear()

        self.comboBoxHuanLuyenVien.addItem(f"-- Chọn PT môn {mon_tap} --")


        for hlv in self.danh_sach_hlv.list:
            dieu_kien_mon = (hlv.status == mon_tap)

            dieu_kien_ngay = (thu_dang_chon in hlv.available_dates)

            dieu_kien_gio = (gio_dang_chon in hlv.available_times)


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


        self.comboBoxRoom.blockSignals(True)
        self.comboBoxRoom.clear()


        for phong in self.danh_sach_phong.list:
            if phong.category == mon_tap:
                self.comboBoxRoom.addItem(phong.name)

        self.comboBoxRoom.blockSignals(False)

        #
        self.cap_nhat_label_so_luong()

    def mo_man_hinh_thanh_toan(self):
        # 1. Lấy thông tin từ giao diện Đặt lịch
        mon_tap = self.get_mon_tap_dang_chon()
        ngay_tap = self.dateEdit.date().toString("dd/MM/yyyy")
        gio_tap = self.comboBoxTime.currentText()

        phong_text = self.comboBoxRoom.currentText()
        phong = phong_text.split(" (")[0] if " (" in phong_text else phong_text


        if mon_tap == "" or phong == "":
            QMessageBox.warning(self.MainWindow, "Thiếu thông tin", "Vui lòng chọn lĩnh vực và phòng tập!")
            return

        thoi_gian_day_du = f"{gio_tap} ngày {ngay_tap}"
        goi_tap_hien_thi = f"Gói: {mon_tap}"

        if self.radioButtonYes.isChecked():
            ten_pt = self.comboBoxHuanLuyenVien.currentText()
            if ten_pt and "-- Chọn PT" not in ten_pt:
                goi_tap_hien_thi += f" (HLV: {ten_pt})"
            else:
                QMessageBox.warning(self.MainWindow, "Thiếu thông tin", "Vui lòng chọn Huấn luyện viên!")
                return


        gia_tien_tong = 500000
        if self.radioButtonYes.isChecked():
            gia_tien_tong += 200000


        self.payment_window = QMainWindow()
        self.payment_ui = PaymentEx()
        self.payment_ui.setupUi(self.payment_window)


        self.payment_ui.set_booking_info(goi_tap_hien_thi, thoi_gian_day_du, phong, gia_tien_tong)


        self.payment_window.showMaximized()
        self.MainWindow.hide()

    def tro_ve_dashboard(self):

        reply = QMessageBox.question(
            self.MainWindow,
            "Xác nhận hủy",
            "Bạn có chắc chắn muốn hủy thao tác đặt lịch và quay về trang chủ không?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No  # Mặc định trỏ chuột vào nút No cho an toàn
        )

        if reply == QMessageBox.StandardButton.Yes:

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