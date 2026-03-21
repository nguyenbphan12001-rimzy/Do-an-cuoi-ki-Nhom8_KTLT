import json
import pandas as pd
import seaborn as sns
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import os

from models.trainers import Trainers
from ui.dashboard.DashboardEx import DashboardEx
from ui.statistic.StatisticMainWindow import Ui_MainWindow


class StatisticMainWindowEx(Ui_MainWindow):
    def __init__(self):
        self.tr = Trainers()
        self.tr.import_json("../../Datasets/trainer.json")


    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupPlot()
        self.pushButtonTKgoitap.clicked.connect(self.show_goitap)
        self.pushButtonTKdoanhthu.clicked.connect(self.show_doanhthu)
        self.pushButtonTKluongkhach.clicked.connect(self.show_luongkhach)

        self.pushButtonTudo.clicked.connect(lambda :self.filter_users("Tự do"))
        self.pushButtonBoxing.clicked.connect(lambda :self.filter_users("Boxing"))
        self.pushButtonPilates.clicked.connect(lambda : self.filter_users("Pilates"))
        self.pushButtonYoga.clicked.connect(lambda :self.filter_users("Yoga"))
        self.setupSignalAndSLot()
        self.display_trainers()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.abspath(os.path.join(current_dir, "../../images/Thongke.png")).replace("\\", "/")

        self.MainWindow.setStyleSheet(f"""
            QMainWindow {{
                border-image: url({img_path}) 0 0 0 0 stretch stretch;
            }}
            #centralwidget, #widget, #widget_2, #widget_3, #groupBox, #verticalLayoutChart {{
                background-color: transparent !important;
                border: none;
            }}
            /* Giữ màu cho các nút bấm */
            QPushButton {{
                background-color: rgb(203, 221, 209);
                border-radius: 15px;
                border: 3px solid #58827d;
            }}
            QPushButton#pushButtonBack {{
                background-color: rgb(24, 78, 73);
                color: white;
            }}
        """)


    def setupSignalAndSLot(self):
        self.pushButtonTKgoitap.clicked.connect(self.show_goitap)
        self.pushButtonTKdoanhthu.clicked.connect(self.show_doanhthu)
        self.pushButtonTKluongkhach.clicked.connect(self.show_luongkhach)

        self.pushButtonAdd.clicked.connect(self.process_add)
        self.pushButtonDelete.clicked.connect(self.process_delete)
        self.pushButtonSave.clicked.connect(self.process_save)
        self.tableWidgetPt.cellClicked.connect(self.process_selection)

    def show(self):
        self.MainWindow.show()

    def setupPlot(self):
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self.MainWindow)
        self.verticalLayoutChart.addWidget(self.toolbar)
        self.verticalLayoutChart.addWidget(self.canvas)

    def show_goitap(self):
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, '../../Datasets/pie_data.csv')
        df = pd.read_csv(file_path)
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.pie(df["Số người"], labels=df["Gói tập"], autopct='%1.2f%%')
        ax.legend(df["Gói tập"], loc='center right', bbox_to_anchor=(-0.1, 0.5))
        self.figure.subplots_adjust(left=0.3)
        self.figure.set_facecolor('#cbddd1')
        ax.set_title("Thống kê các gói tập", fontsize=12, fontweight='bold')
        self.canvas.draw()

    def show_luongkhach(self):
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, '../../Datasets/line_data.csv')
        df = pd.read_csv(file_path)
        self.figure.clear()
        self.figure.set_facecolor('#cbddd1')
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#eaf4ef')
        ax.ticklabel_format(useOffset=False, style="plain")
        ax.grid()
        sns.lineplot(
            ax=ax,
            data=df,
            x="Ngày",
            y="Số lượng đặt",
            marker="o",
            color='orange',
            label="Số lượng đặt"
        )
        ax.set_title("Số lượng khách đặt lịch trong một tuần", fontsize=12, fontweight='bold')

        ax.legend(loc='lower right')
        self.figure.tight_layout()
        self.canvas.draw()

    def show_doanhthu(self):
        # Đọc dữ liệu
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, '../../Datasets/bar_data.csv')
        df = pd.read_csv(file_path)
        self.figure.clear()
        self.figure.set_facecolor('#cbddd1')
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#eaf4ef')
        ax.bar(df["Tháng"], df["triệu đồng"], color='tab:blue')
        ax.set_xticks(range(1, 13))
        ax.set_title("Doanh thu năm 2025", fontsize=12, fontweight='bold')
        ax.set_xlabel("Tháng", fontsize=10)
        ax.set_ylabel("Triệu đồng", fontsize=10)
        ax.ticklabel_format(useOffset=False, style="plain", axis='y')
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        self.figure.tight_layout()
        self.canvas.draw()

    def process_back(self):
        self.MainWindow.close()
        self.dashboard_window = QMainWindow()
        self.dashboard_ui = DashboardEx()
        self.dashboard_ui.setupUi(self.dashboard_window)
        self.dashboard_ui.showWindow()

    #Danh sách khách hàng
    def filter_users(self, goitap):
        try:
            # 1. Khai báo đường dẫn
            base_dir = os.path.dirname(__file__)
            file_path = os.path.join(base_dir, "../../Datasets/booking_history.json")

            # 2. Đọc file JSON
            with open(file_path, "r", encoding="utf-8") as f:
                raw = json.load(f)

            data = raw.get("Datasets", [])
            users = []

            # 3. Lọc dữ liệu theo gói tập
            for item in data:
                package = item.get("package_details", "")
                if f"Gói: {goitap}" in package:
                    users.append(item)

            # 4. Xóa trùng theo SĐT (Phải thụt lề vào trong try)
            unique_users = {}
            for u in users:
                unique_users[u["phone"]] = u
            users = list(unique_users.values())

            # 5. Hiển thị lên bảng (Phải thụt lề vào trong try)
            self.tableWidget.setRowCount(len(users))
            self.tableWidget.setColumnCount(3)
            self.tableWidget.setHorizontalHeaderLabels(["Họ và tên", "SĐT", "Môn đăng ký"])

            for row, user in enumerate(users):
                self.tableWidget.setItem(row, 0, QTableWidgetItem(user.get("customer_name", "")))
                self.tableWidget.setItem(row, 1, QTableWidgetItem(user.get("phone", "")))
                self.tableWidget.setItem(row, 2, QTableWidgetItem(goitap))

        except Exception as e:
            # Except phải thẳng hàng với Try
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self.MainWindow, "Lỗi dữ liệu", f"Không thể đọc file JSON!\nChi tiết: {e}")

    def display_trainers(self):
        self.tableWidgetPt.setRowCount(0)

        for item in self.tr.list:
            row = self.tableWidgetPt.rowCount()
            self.tableWidgetPt.insertRow(row)

            self.tableWidgetPt.setItem(row, 0, QTableWidgetItem(str(item.username)))
            self.tableWidgetPt.setItem(row, 1, QTableWidgetItem(str(item.phone_number)))
            self.tableWidgetPt.setItem(row, 2, QTableWidgetItem(str(item.email)))

            gender_str = item.gender if isinstance(item.gender, str) else "".join(item.gender)
            self.tableWidgetPt.setItem(row, 3, QTableWidgetItem(gender_str))

            self.tableWidgetPt.setItem(row, 4, QTableWidgetItem(str(item.status)))

            dates = ", ".join(item.available_dates) if isinstance(item.available_dates, list) else str(
                item.available_dates)
            times = ", ".join(item.available_times) if isinstance(item.available_times, list) else str(
                item.available_times)

            self.tableWidgetPt.setItem(row, 5, QTableWidgetItem(dates))
            self.tableWidgetPt.setItem(row, 6, QTableWidgetItem(times))

    def process_selection(self, row, column):
        try:
            if row < 0 or row >= len(self.tr.list):
                return

            item = self.tr.list[row]

            self.lineEditNamePt.setText(item.username)
            self.lineEditPhonePt.setText(item.phone_number)
            self.lineEditEmailPt.setText(item.email)

            if item.gender == "M":
                self.radioButtonMale.setChecked(True)
            else:
                self.radioButtonFemale.setChecked(True)

            self.lineEditRolePt.setText(item.status)
            self.lineEditDatePt.setText(", ".join(item.available_dates))
            self.lineEditTimePt.setText(", ".join(item.available_times))

        except Exception as e:
            print("LỖI:", e)

    def process_add(self):
        self.lineEditNamePt.clear()
        self.lineEditPhonePt.clear()
        self.lineEditEmailPt.clear()
        self.radioButtonMale.setChecked(False)
        self.radioButtonFemale.setChecked(False)
        self.lineEditRolePt.clear()
        self.lineEditDatePt.clear()
        self.lineEditTimePt.clear()

    def process_save(self):
        from models.trainer import Trainer

        name = self.lineEditNamePt.text().strip()
        if not name:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng nhập tên trước khi lưu mới!")
            return

        # Tạo object mới hoàn toàn
        new_trainer = Trainer(
            username=name,
            phone_number=self.lineEditPhonePt.text(),
            email=self.lineEditEmailPt.text(),
            gender="M" if self.radioButtonMale.isChecked() else "F",
            status=self.lineEditRolePt.text(),
            available_dates=[d.strip() for d in self.lineEditDatePt.text().split(",") if d.strip()],
            available_times=[t.strip() for t in self.lineEditTimePt.text().split(",") if t.strip()],
            password="123",
            role="trainer"
        )

        # Thêm vào cuối danh sách
        self.tr.save_item(new_trainer)

        # LƯU XUỐNG JSON
        self.tr.export_json("../../Datasets/trainer.json")

        self.display_trainers()
        self.process_add()  # Tự động xóa trắng các ô sau khi lưu xong

        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(self.MainWindow, "Thông báo", "Đã lưu thông tin nhân viên thành công!")

    def process_delete(self):
        row = self.tableWidgetPt.currentRow()
        if row < 0:
            return

        trainer = self.tr.list[row]
        self.tr.remove_item(trainer.username)
        self.display_trainers()



