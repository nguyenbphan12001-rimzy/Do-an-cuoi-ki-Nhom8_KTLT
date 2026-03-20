
from PyQt6.QtWidgets import QMainWindow
import json
import os
from ui.admin.AdminHistoryEx import AdminHistoryEx
from ui.dashboard.Dashboard import Ui_MainWindow
from ui.member.MemberMainWindowEx import MemberMainWindowEx
from ui.registration.Registration_formMainWindowEx import Registration_formMainWindowEx
from ui.home.HomeEx import HomeEx
from ui.booking.BookingMainWindowEx import BookingMainWindowEx


class DashboardEx(Ui_MainWindow):
    def __init__(self, username=None):
        super().__init__()
        self.username = username

        # Nếu không truyền username, tự load từ session
        if username is None:
            current_user_file = os.path.join(os.path.dirname(__file__), "../../datasets/current_user.json")
            try:
                with open(current_user_file, encoding="utf-8") as f:
                    data = json.load(f)
                    self.username = data.get("username")
            except Exception:
                self.username = None

        # Load session data
        self.load_session_data()

    def setupUi(self, MainWindow):
        """Thiết lập UI chính và các signal"""
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow

        # Thiết lập background
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = current_dir.split("ui")[0]
        img_path = os.path.join(project_root, "images", "Dashboard.png").replace("\\", "/")
        self.centralwidget.setStyleSheet(f"#centralwidget {{ border-image: url({img_path}); }}")

        # Setup các signal cho button
        self.setupSignalAndSlot()

    def load_session_data(self):
        """Đảm bảo Dashboard luôn có dữ liệu user mới nhất từ file session"""
        try:
            project_root = os.path.abspath(__file__).split("ui")[0]
            session_file = os.path.join(project_root, "datasets", "current_user.json")

            if os.path.exists(session_file):
                with open(session_file, 'r', encoding='utf-8') as f:
                    self.current_user = json.load(f)
                    print(f"✅ Dashboard nạp thành công user: {self.current_user.get('username')}")
            else:
                self.current_user = None
        except Exception as e:
            print(f"❌ Lỗi nạp session tại Dashboard: {e}")
            self.current_user = None

    def showWindow(self):
        """Hiển thị Dashboard"""
        self.MainWindow.show()

    def setupSignalAndSlot(self):
        """Kết nối các button với function"""
        self.pushButtonDatlich.clicked.connect(self.process_booking)
        self.pushButtonDkyHoivien.clicked.connect(self.process_dkyhoivien)
        self.pushButtonProfile.clicked.connect(self.process_profile)
        self.pushButtonLogOut.clicked.connect(self.process_logout)
        # self.pushButtonMember.clicked.connect(self.process_member)
        self.pushButtonMyBooking.clicked.connect(self.mo_man_hinh_lich_su)

    # ----------------- Xử lý button -----------------
    def process_booking(self):
        self.booking_window = QMainWindow()
        self.booking_ui = BookingMainWindowEx()
        self.booking_ui.setupUi(self.booking_window)
        self.booking_ui.current_user = getattr(self, "current_user", None)
        self.booking_window.showMaximized()
        self.booking_ui.showWindow()
        # Dashboard vẫn là window gốc, không hide

    def process_dkyhoivien(self):
        self.hoivien_window = QMainWindow()
        self.hoivien_ui = Registration_formMainWindowEx()
        self.hoivien_ui.setupUi(self.hoivien_window)
        self.hoivien_ui.current_user = getattr(self, "current_user", None)
        self.hoivien_window.showMaximized()
        self.hoivien_ui.showWindow()
        # Dashboard vẫn là window gốc

    def process_member(self):
        self.member_window = QMainWindow()
        self.member_ui = MemberMainWindowEx()
        self.member_ui.setupUi(self.member_window)
        self.member_ui.current_user = getattr(self, "current_user", None)
        self.member_ui.load_member()
        self.member_window.showMaximized()
        # self.MainWindow.hide()

    def process_profile(self):
        """Mở AdminEx (Profile)"""
        self.admin_window = QMainWindow()
        self.admin_ui = MemberMainWindowEx(self.username)
        self.admin_ui.setupUi(self.admin_window)
        self.admin_ui.current_user = getattr(self, "current_user", None)
        # 2. Gọi hàm load_member để nạp thông tin ra các ô nhập liệu
        self.admin_ui.load_member()
        self.admin_window.showMaximized()

        self.MainWindow.hide()

    def process_logout(self):
        """Đăng xuất về HomeEx"""
        self.logout_window = QMainWindow()
        self.logout_ui = HomeEx()
        self.logout_ui.setupUi(self.logout_window)
        self.logout_window.showMaximized()
        self.logout_ui.showWindow()
        # Đóng Dashboard
        self.MainWindow.close()

    def mo_man_hinh_lich_su(self):
        """Mở màn hình lịch sử Admin"""
        self.history_win = AdminHistoryEx(self.MainWindow)
        self.history_win.show()
        self.MainWindow.hide()