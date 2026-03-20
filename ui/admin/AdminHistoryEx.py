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
        """Phân quyền: Admin xem tất cả, User chỉ xem của mình"""
        current_file_path = os.path.abspath(__file__)
        project_root = current_file_path.split("ui")[0]
        datasets_dir = os.path.join(project_root, "datasets")

        history_file = os.path.join(datasets_dir, "booking_history.json")
        user_session_file = os.path.join(datasets_dir, "current_user.json")

        # 1. Đọc thông tin User đang đăng nhập từ session
        curr_user_data = {}
        if os.path.exists(user_session_file):
            try:
                with open(user_session_file, 'r', encoding='utf-8') as f:
                    curr_user_data = json.load(f)
            except:
                pass

        role = curr_user_data.get("role", "user")  # Lấy quyền (admin/user)
        my_phone = str(curr_user_data.get("phone_number", ""))  # Lấy SĐT để lọc

        # 2. Đọc toàn bộ lịch sử
        all_history = []
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    all_history = json.load(f)
            except:
                pass

        # 3. THỰC HIỆN LỌC DỮ LIỆU THEO QUYỀN
        display_list = []

        if role == "admin":
            # Nếu là Admin (như Lâm Tâm Như), hốt hết không chừa dòng nào
            display_list = all_history
            self.lbl_summary.setText(f"Chế độ Admin: Đang hiển thị toàn bộ {len(display_list)} bản ghi.")
        else:
            # Nếu là User thường, chỉ lọc những dòng có SĐT trùng với mình
            for item in all_history:
                if str(item.get("phone")) == my_phone:
                    display_list.append(item)
            self.lbl_summary.setText(f"Xin chào {curr_user_data.get('username')}, bạn có {len(display_list)} lịch tập.")

        # 4. Hiển thị lên TableWidget
        display_list.reverse()  # Cái mới nhất hiện lên đầu
        self.table_history.setRowCount(0)

        for row, bill in enumerate(display_list):
            self.table_history.insertRow(row)
            self.table_history.setItem(row, 0, QTableWidgetItem(str(bill.get("customer_name", ""))))
            self.table_history.setItem(row, 1, QTableWidgetItem(str(bill.get("phone", ""))))
            self.table_history.setItem(row, 2, QTableWidgetItem(str(bill.get("package_details", ""))))
            self.table_history.setItem(row, 3, QTableWidgetItem(str(bill.get("time", ""))))
            self.table_history.setItem(row, 4, QTableWidgetItem("N/A"))
            self.table_history.setItem(row, 5, QTableWidgetItem(str(bill.get("payment_time", ""))))