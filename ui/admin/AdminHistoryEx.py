import json
import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel,
                             QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon


class AdminHistoryEx(QMainWindow):
    def __init__(self, parent_window=None):
        super().__init__()
        self.parent_window = parent_window  # Lưu cửa sổ Admin chính để quay về
        self.setWindowTitle("FIT LIFESTYLE - Quản lý lịch sử đặt lịch")
        self.resize(1000, 600)
        self.setWindowIcon(QIcon("images/icon_app.png"))

        # 1. Widget trung tâm và Layout chính
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # 2. Tiêu đề
        lbl_title = QLabel("LỊCH SỬ ĐĂNG KÝ LỊCH TẬP")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Arial", 20, QFont.Weight.Bold)
        lbl_title.setFont(title_font)
        lbl_title.setStyleSheet("color: #1A483E; margin-bottom: 10px;")
        main_layout.addWidget(lbl_title)

        # 3. Label hiển thị công suất
        self.lbl_summary = QLabel("Đang tải dữ liệu...")
        self.lbl_summary.setFont(QFont("Arial", 11))
        self.lbl_summary.setStyleSheet("color: #666; font-style: italic;")
        main_layout.addWidget(self.lbl_summary)

        # 4. Bảng hiển thị dữ liệu
        self.table_history = QTableWidget()
        columns = ["Tên khách", "SĐT", "Gói tập & Phòng", "Thời gian tập", "PT / Ghi chú", "Thời gian mua"]
        self.table_history.setColumnCount(len(columns))
        self.table_history.setHorizontalHeaderLabels(columns)

        header = self.table_history.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setStyleSheet(
            "QHeaderView::section { background-color: #f0f0f0; padding: 4px; font-weight: bold; border: 1px solid #dcdcdc; }")

        self.table_history.setAlternatingRowColors(True)
        self.table_history.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_history.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        main_layout.addWidget(self.table_history)

        # 5. Nạp dữ liệu
        self.load_history_data()



    def closeEvent(self, event):
        """Khi bấm dấu X tắt cửa sổ này, nó sẽ tự hiện lại màn hình Admin chính"""
        if self.parent_window:
            self.parent_window.show()
        event.accept()

    def load_history_data(self):
        """Phân quyền: Admin xem tất cả, User chỉ xem của mình + LỌC TRÙNG LẶP"""
        current_file_path = os.path.abspath(__file__)
        project_root = current_file_path.split("ui")[0]
        datasets_dir = os.path.join(project_root, "datasets")

        history_file = os.path.join(datasets_dir, "booking_history.json")
        user_session_file = os.path.join(datasets_dir, "current_user.json")

        # 1. Đọc thông tin User
        curr_user_data = {}
        if os.path.exists(user_session_file):
            try:
                with open(user_session_file, 'r', encoding='utf-8') as f:
                    curr_user_data = json.load(f)
            except Exception as e:
                pass

        role = curr_user_data.get("role", "user")
        my_phone = str(curr_user_data.get("phone_number", ""))

        # 2. Đọc toàn bộ lịch sử
        all_history = []
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    raw_data = json.load(f)
                    if isinstance(raw_data, dict):
                        all_history = raw_data.get("Datasets", [])
                    else:
                        all_history = raw_data
            except Exception as e:
                pass

        # 3. Lọc dữ liệu VÀ LOẠI BỎ TRÙNG LẶP
        display_list = []
        seen_records = set()  # Bộ nhớ tạm để đánh dấu các dòng đã nạp

        for item in all_history:
            if not isinstance(item, dict):
                continue

            # Tạo một cái "chữ ký" cho mỗi bản ghi (dựa vào SĐT, gói tập, giờ tập và giờ mua)
            # Nếu 4 cái này y chang nhau thì chắc chắn là dữ liệu bị nhân đôi
            record_signature = (
                item.get("phone", ""),
                item.get("package_details", ""),
                item.get("time", ""),
                item.get("payment_time", "")
            )

            # Phân quyền: Nếu là admin thì lấy hết, là user thì phải trùng SĐT
            is_valid_user = (role == "admin") or (str(item.get("phone", "")) == my_phone)

            # Nếu user hợp lệ VÀ bản ghi này chưa từng xuất hiện (chưa bị trùng)
            if is_valid_user and record_signature not in seen_records:
                seen_records.add(record_signature)  # Đánh dấu là đã thấy
                display_list.append(item)  # Thêm vào danh sách hiển thị

        # Cập nhật Label
        if role == "admin":
            self.lbl_summary.setText(f"Chế độ Admin: Đang hiển thị {len(display_list)} bản ghi (đã ẩn trùng lặp).")
        else:
            self.lbl_summary.setText(
                f"Xin chào {curr_user_data.get('username', 'Khách')}, bạn có {len(display_list)} lịch tập.")

        # 4. Hiển thị lên Table
        display_list.reverse()  # Mới nhất lên đầu
        self.table_history.setRowCount(0)

        for row, bill in enumerate(display_list):
            self.table_history.insertRow(row)
            self.table_history.setItem(row, 0, QTableWidgetItem(str(bill.get("customer_name", ""))))
            self.table_history.setItem(row, 1, QTableWidgetItem(str(bill.get("phone", ""))))
            self.table_history.setItem(row, 2, QTableWidgetItem(str(bill.get("package_details", ""))))
            self.table_history.setItem(row, 3, QTableWidgetItem(str(bill.get("time", ""))))
            self.table_history.setItem(row, 4, QTableWidgetItem("N/A"))
            self.table_history.setItem(row, 5, QTableWidgetItem(str(bill.get("payment_time", ""))))