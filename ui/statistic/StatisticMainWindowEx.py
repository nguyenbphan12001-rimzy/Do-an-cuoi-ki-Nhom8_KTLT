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
<<<<<<< HEAD
        self.pushButtonTKgoitap.clicked.connect(self.show_goitap)
        self.pushButtonTKdoanhthu.clicked.connect(self.show_doanhthu)
        self.pushButtonTKluongkhach.clicked.connect(self.show_luongkhach)
        self.pushButtonBack.clicked.connect(self.process_back)
        self.pushButtonTudo.clicked.connect(lambda :self.filter_users("Tự do"))
        self.pushButtonBoxing.clicked.connect(lambda :self.filter_users("Boxing"))
        self.pushButtonPilates.clicked.connect(lambda : self.filter_users("Pilates"))
        self.pushButtonYoga.clicked.connect(lambda :self.filter_users("Yoga"))
=======
        self.setupSignalAndSLot()
        self.display_trainers()
>>>>>>> 1286e67864d3f991fe55d890f01cf37ed3c765cf

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
        self.pushButtonBack.clicked.connect(self.process_back)
        self.pushButtonAdd.clicked.connect(self.process_add)
        self.pushButtonChange.clicked.connect(self.process_update)
        self.pushButtonDelete.clicked.connect(self.process_delete)
        self.pushButtonSave.clicked.connect(self.process_save)
        self.tableWidgetPt.itemSelectionChanged.connect(self.process_selection)

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

<<<<<<< HEAD

    #Danh sách khách hàng
    def filter_users(self, goitap):
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, "../../Datasets/booking_history.json")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)  # data là LIST

        users = []

        # Lọc theo gói tập trong chuỗi
        for item in data:
            package = item.get("package_details", "")

            if f"Gói: {goitap}" in package:
                users.append(item)

        # Xóa trùng theo SĐT
        unique_users = {}
        for u in users:
            unique_users[u["phone"]] = u

        users = list(unique_users.values())

        # Hiển thị lên bảng
        self.tableWidget.setRowCount(len(users))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Họ và tên", "SĐT", "Môn đăng ký"]
        )

        for row, user in enumerate(users):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(user.get("customer_name", "")))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(user.get("phone", "")))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(goitap))
=======
    def display_trainers(self):
        self.tableWidgetPt.setRowCount(0)

        for item in self.tr.list:
            row = self.tableWidgetPt.rowCount()
            self.tableWidgetPt.insertRow(row)

            self.tableWidgetPt.setItem(row, 0, QTableWidgetItem(item.username))
            self.tableWidgetPt.setItem(row, 1, QTableWidgetItem(""))  # không có tuổi
            self.tableWidgetPt.setItem(row, 2, QTableWidgetItem(item.phone_number))
            self.tableWidgetPt.setItem(row, 3, QTableWidgetItem(item.email))
            self.tableWidgetPt.setItem(row, 4, QTableWidgetItem(item.gender))
            self.tableWidgetPt.setItem(row, 5, QTableWidgetItem(item.status))

            dates = ", ".join(item.available_dates)
            times = ", ".join(item.available_times)

            self.tableWidgetPt.setItem(row, 6, QTableWidgetItem(dates))
            self.tableWidgetPt.setItem(row, 7, QTableWidgetItem(times))

    def process_selection(self):
        row = self.tableWidgetPt.currentRow()
        if row < 0:
            return

        item = self.tr.list[row]

        self.lineEditNamePt.setText(item.username)
        self.lineEditAgePt.setText("")
        self.lineEditPhonePt.setText(item.phone_number)
        self.lineEditEmailPt.setText(item.email)
        self.lineEditGenderPt.setText(item.gender)
        self.lineEditRolePt.setText(item.status)
        self.lineEditDatePt.setText(", ".join(item.available_dates))
        self.lineEditTimePt.setText(", ".join(item.available_times))

    def process_add(self):
        self.lineEditNamePt.clear()
        self.lineEditAgePt.clear()
        self.lineEditPhonePt.clear()
        self.lineEditEmailPt.clear()
        self.lineEditGenderPt.clear()
        self.lineEditRolePt.clear()
        self.lineEditDatePt.clear()
        self.lineEditTimePt.clear()

    def process_save(self):
        from models.trainer import Trainer

        username = self.lineEditNamePt.text()
        phone = self.lineEditPhonePt.text()
        email = self.lineEditEmailPt.text()
        gender = self.lineEditGenderPt.text()
        status = self.lineEditRolePt.text()

        # tách chuỗi thành list
        dates = self.lineEditDatePt.text().split(",")
        times = self.lineEditTimePt.text().split(",")

        # strip cho sạch
        dates = [d.strip() for d in dates]
        times = [t.strip() for t in times]

        trainer = Trainer(
            username,
            phone,
            email,
            gender,
            status,
            dates,
            times
        )

        self.tr.save_item(trainer)
        self.display_trainers()

    def process_delete(self):
        row = self.tableWidgetPt.currentRow()
        if row < 0:
            return

        trainer = self.tr.list[row]
        self.tr.remove_item(trainer.username)
        self.display_trainers()

    def process_update(self):
        row = self.tableWidgetPt.currentRow()
        if row < 0:
            return

        from models.trainer import Trainer

        username = self.lineEditNamePt.text()
        phone = self.lineEditPhonePt.text()
        email = self.lineEditEmailPt.text()
        gender = self.lineEditGenderPt.text()
        status = self.lineEditRolePt.text()

        dates = [d.strip() for d in self.lineEditDatePt.text().split(",")]
        times = [t.strip() for t in self.lineEditTimePt.text().split(",")]

        trainer = Trainer(
            username,
            phone,
            email,
            gender,
            status,
            dates,
            times
        )

        self.tr.update_item(row, trainer)
        self.display_trainers()



>>>>>>> 1286e67864d3f991fe55d890f01cf37ed3c765cf
