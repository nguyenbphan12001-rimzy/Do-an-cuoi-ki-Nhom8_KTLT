import json
import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QFrame,
                             QPushButton)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QBrush, QColor, QPixmap


class AdminHistoryEx(QMainWindow):
    def __init__(self, parent_window=None):
        super().__init__()
        self.parent_window = parent_window  # Lưu cửa sổ Admin chính để quay về
        self.setWindowTitle("FIT LIFESTYLE - Quản lý lịch sử đặt lịch")
        self.resize(1100, 700)  # Tăng nhẹ kích thước để bảng đẹp hơn
        self.setWindowIcon(QIcon("images/icon_app.png"))


        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(15)


        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5EC;
            }
            /* --- Style cho nút Quay lại --- */
            QPushButton#btnBack {
                background-color: #D4E7DD;
                color: #264E3D;
                border-radius: 15px;
                padding: 8px 20px;
                font-weight: bold;
                font-size: 20px;
                border: 1px solid #C1D8CD;
            }
            QPushButton#btnBack:hover {
                background-color: #C1D8CD; /* Đậm hơn chút khi rê chuột vào */
            }
            QPushButton#btnBack:pressed {
                background-color: #A3C5B5; /* Đậm hơn nữa khi click */
            }
            /* ------------------------------ */
            QFrame#headerPill {
                background-color: #264E3D;
                border-radius: 20px;
                margin-bottom: 10px;
            }
            QLabel#headerTitle {
                color: #F5F5EC;
                font-weight: bold;
                margin-left: 20px;
            }
            QLabel#SummaryLabel {
                color: #264E3D;
                font-weight: bold;
                font-size: 14px;
                font-style: italic;
            }
            /* Style cho vùng chứa Bảng để tạo bo góc khối mượt */
            QFrame#TableContainer {
                background-color: #D4E7DD; /* Mint nhạt bao quanh */
                border-radius: 20px;
                padding: 10px;
                border: 1px solid #C1D8CD;
            }
            /* Style cho Bảng */
            QTableWidget {
                background-color: white; /* Giữ bảng trắng để thanh lịch */
                border: none;
                color: #1A3028;
                gridline-color: transparent; /* Tắt lưới mặc định */
                font-size: 13px;
                alternate-background-color: #f9f9f9; /* Màu nền dòng xen kẽ */
                selection-background-color: #C1D8CD;
                selection-color: #1A3028;
                border-radius: 10px;
            }
            QTableWidget::item {
                padding: 5px 10px;
            }
            /* Style cho Header Bảng */
            QHeaderView::section {
                background-color: #264E3D;
                color: #F5F5EC;
                font-weight: bold;
                font-size: 14px;
                padding: 10px;
                border: none;
                border-right: 1px solid #3A6658;
            }
            /* Ẩn cục ô vuông ở góc trên cùng bên trái của Table */
            QTableCornerButton::section {
                background-color: #264E3D;
                border: none;
            }
        """)


        top_bar_layout = QHBoxLayout()
        self.btn_back = QPushButton("← Back")
        self.btn_back.setObjectName("btnBack")
        self.btn_back.setCursor(Qt.CursorShape.PointingHandCursor)  # Thêm hiệu ứng bàn tay khi trỏ chuột vào
        self.btn_back.clicked.connect(self.go_back)

        top_bar_layout.addWidget(self.btn_back, alignment=Qt.AlignmentFlag.AlignLeft)
        top_bar_layout.addStretch()  # Dùng stretch để đẩy nút về sát bên trái
        main_layout.addLayout(top_bar_layout)


        header_pill = QFrame()
        header_pill.setObjectName("headerPill")  # Áp dụng style QSS
        header_layout = QHBoxLayout(header_pill)
        header_layout.setContentsMargins(15, 10, 15, 10)

        # Logo )
        lbl_logo = QLabel()
        if os.path.exists("images/logo_icon.png"):  # Thử load logo icon nhỏ
            pixmap = QPixmap("images/logo_icon.png").scaled(35, 35, Qt.AspectRatioMode.KeepAspectRatio)
            lbl_logo.setPixmap(pixmap)
        header_layout.addWidget(lbl_logo, 0, Qt.AlignmentFlag.AlignVCenter)


        lbl_title = QLabel("LỊCH SỬ ĐĂNG KÝ LỊCH TẬP")
        lbl_title.setObjectName("headerTitle")
        title_font = QFont("Arial", 20, QFont.Weight.Bold)
        lbl_title.setFont(title_font)
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        header_layout.addWidget(lbl_title, 1)  # Cho phép text dãn
        header_layout.addStretch()  # Thêm spacer để logo and title dính nhau

        main_layout.addWidget(header_pill, 0, Qt.AlignmentFlag.AlignCenter)  # Failsafe align center


        self.lbl_summary = QLabel("Đang tải dữ liệu...")
        self.lbl_summary.setObjectName("SummaryLabel")
        self.lbl_summary.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.lbl_summary)


        table_container = QFrame()
        table_container.setObjectName("TableContainer")
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(1, 1, 1, 1)  # Sát viền


        self.table_history = QTableWidget()
        columns = ["Tên khách", "SĐT", "Gói tập & Phòng", "Thời gian tập", "Thời gian mua"]
        self.table_history.setColumnCount(len(columns))
        self.table_history.setHorizontalHeaderLabels(columns)

        header = self.table_history.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)


        self.table_history.verticalHeader().setVisible(False)
        self.table_history.setAlternatingRowColors(True)
        self.table_history.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_history.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_history.setShowGrid(False)

        table_layout.addWidget(self.table_history)
        main_layout.addWidget(table_container)


        self.load_history_data()

    def go_back(self):

        if self.parent_window:
            self.parent_window.show()  # Hiện lại Dashboard
        self.close()

    def closeEvent(self, event):

        if self.parent_window:
            self.parent_window.show()
        event.accept()

    def load_history_data(self):
        import sys

        if getattr(sys, 'frozen', False):
            # Nếu chạy từ file .exe
            base_dir = os.path.dirname(sys.executable)
        else:

            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


        datasets_dir = os.path.join(base_dir, "Datasets")

        history_file = os.path.join(datasets_dir, "booking_history.json")
        user_session_file = os.path.join(datasets_dir, "current_user.json")

        print(f"DEBUG: Dang tim file tai: {history_file}")


        curr_user_data = {}
        if os.path.exists(user_session_file):
            try:
                with open(user_session_file, 'r', encoding='utf-8') as f:
                    curr_user_data = json.load(f)
            except Exception as e:
                print(f"Loi doc session: {e}")

        role = curr_user_data.get("role", "user")
        my_phone = str(curr_user_data.get("phone_number", ""))

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
                print(f"Loi doc history: {e}")
        else:
            print("LOI: Khong tim thay file booking_history.json!")


        display_list = []
        seen_records = set()

        for item in all_history:
            if not isinstance(item, dict): continue

            # Tạo signature để lọc trùng
            record_signature = (
                str(item.get("phone", "")),
                str(item.get("package_details", "")),
                str(item.get("time", "")),
                str(item.get("payment_time", ""))
            )

            # Check quyền: Admin thấy hết, User chỉ thấy của mình
            is_valid_user = (role == "admin") or (str(item.get("phone", "")) == my_phone)

            if is_valid_user and record_signature not in seen_records:
                seen_records.add(record_signature)
                display_list.append(item)


        if role == "admin":
            self.lbl_summary.setText(f"Chế độ Admin: Đang hiển thị {len(display_list)} bản ghi.")
        else:
            name = curr_user_data.get('username', 'Khách')
            self.lbl_summary.setText(f"Xin chào {name}, bạn có {len(display_list)} lịch tập.")


        display_list.reverse()
        self.table_history.setRowCount(len(display_list))

        for row, bill in enumerate(display_list):
            self.table_history.setItem(row, 0, QTableWidgetItem(str(bill.get("customer_name", ""))))
            self.table_history.setItem(row, 1, QTableWidgetItem(str(bill.get("phone", ""))))
            self.table_history.setItem(row, 2, QTableWidgetItem(str(bill.get("package_details", ""))))
            self.table_history.setItem(row, 3, QTableWidgetItem(str(bill.get("time", ""))))
            self.table_history.setItem(row, 4, QTableWidgetItem(str(bill.get("payment_time", ""))))

            # Căn giữa cho đẹp
            for col in range(5):
                it = self.table_history.item(row, col)
                if it: it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)