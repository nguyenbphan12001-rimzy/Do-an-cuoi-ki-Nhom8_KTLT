import os

from ui.member.MemberMainWindow import Ui_MainWindow
from datetime import datetime,timedelta

class MemberMainWindowEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()

        current_dir = os.path.dirname(os.path.abspath(__file__))

        img_path = os.path.abspath(os.path.join(current_dir, "..", "..", "images", "hoivien_anh(update).jpg")).replace("\\", "/")

        self.centralwidget.setStyleSheet(f"#centralwidget {{ border-image: url({img_path}); }}")
    def showWindow(self):
        self.MainWindow.show()
    def setupSignalAndSlot(self):
        pass
