from PyQt6.QtWidgets import QMainWindow
import os
import json

from ui.admin.adminEx import AdminEx
from ui.booking.BookingMainWindowEx import BookingMainWindowEx
from ui.dashboard.Dashboard import Ui_MainWindow
from ui.member.MemberMainWindowEx import MemberMainWindowEx
from ui.registration.Registration_formMainWindowEx import Registration_formMainWindowEx


class DashboardEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow

        # 1. Tự động nạp lại user từ session khi Dashboard hiện lên
        self.load_session_data()

        # 2. Thiết lập giao diện
        self.setupSignalAndSlot()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = current_dir.split("ui")[0]
        img_path = os.path.join(project_root, "images", "Dashboard.png").replace("\\", "/")
        self.centralwidget.setStyleSheet(f"#centralwidget {{ border-image: url({img_path}); }}")

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
        self.MainWindow.show()

    def setupSignalAndSlot(self):
        self.pushButtonDatlich.clicked.connect(self.process_booking)
        self.pushButtonDkyHoivien.clicked.connect(self.process_dkyhoivien)
        self.pushButtonAdmin.clicked.connect(self.process_admin)
        self.pushButtonLogOut.clicked.connect(self.process_logout)
        self.pushButtonMember.clicked.connect(self.process_member)

    def process_booking(self):
        self.booking_window = QMainWindow()
        self.booking_ui = BookingMainWindowEx()
        self.booking_ui.setupUi(self.booking_window)
        # Truyền user sang Booking nếu cần
        self.booking_ui.current_user = getattr(self, "current_user", None)
        self.booking_window.showMaximized()
        self.booking_ui.showWindow()
        self.MainWindow.close()

    def process_dkyhoivien(self):
        self.hoivien_window = QMainWindow()
        self.hoivien_ui = Registration_formMainWindowEx()
        self.hoivien_ui.setupUi(self.hoivien_window)
        # Truyền user từ Dashboard sang Registration
        self.hoivien_ui.current_user = getattr(self, "current_user", None)
        self.hoivien_window.showMaximized()
        self.hoivien_ui.showWindow()
        self.MainWindow.close()

    def process_member(self):
        """Khởi tạo màn hình Member, truyền dữ liệu và đóng Dashboard"""
        self.member_window = QMainWindow()
        self.member_ui = MemberMainWindowEx()
        self.member_ui.setupUi(self.member_window)

        # Gán current_user từ Dashboard sang Member
        self.member_ui.current_user = getattr(self, "current_user", None)

        # Gọi nạp dữ liệu lên giao diện Member
        self.member_ui.load_member()

        self.member_window.showMaximized()
        self.member_ui.showWindow()
        self.MainWindow.close()

    def process_admin(self):
        # Kiểm tra quyền Admin nếu cần thiết ở đây
        self.admin_window = QMainWindow()
        self.admin_ui = AdminEx()
        self.admin_ui.setupUi(self.admin_window)
        self.admin_window.showMaximized()
        self.admin_ui.showWindow()
        self.MainWindow.close()

    def process_logout(self):
        from ui.home.HomeEx import HomeEx
        self.MainWindow.close()
        self.logout_window = QMainWindow()
        self.logout_ui = HomeEx()
        self.logout_ui.setupUi(self.logout_window)
        self.logout_window.showMaximized()
        self.logout_ui.showWindow()