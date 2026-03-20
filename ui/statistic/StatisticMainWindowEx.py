import pandas as pd
import seaborn as sns
from PyQt6.QtWidgets import QMainWindow
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import os

from ui.dashboard.DashboardEx import DashboardEx
from ui.statistic.StatisticMainWindow import Ui_MainWindow


class StatisticMainWindowEx(Ui_MainWindow):
    def __init__(self):
        pass

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupPlot()
        self.pushButtonTKgoitap.clicked.connect(self.show_goitap)
        self.pushButtonTKdoanhthu.clicked.connect(self.show_doanhthu)
        self.pushButtonTKluongkhach.clicked.connect(self.show_luongkhach)
        self.pushButtonBack.clicked.connect(self.process_back)

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
