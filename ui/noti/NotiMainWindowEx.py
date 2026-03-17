import os
from ui.noti.NotiMainWindow import Ui_MainWindow


class NotiMainWindowEx(Ui_MainWindow):

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.abspath(os.path.join(current_dir, "..", "..", "images", "thongbao_anh.jpg")).replace("\\","/")
        current_stylesheet = self.centralwidget.styleSheet()
        old_path = "E:/MyFinalProject_BackgroundUi/images/thongbao_anh.jpg"
        new_stylesheet = current_stylesheet.replace(old_path, img_path)
        self.centralwidget.setStyleSheet(new_stylesheet)
    def showWindow(self):
        self.MainWindow.show()