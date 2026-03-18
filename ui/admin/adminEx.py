from ui.admin.admin import Ui_MainWindow

import os
class AdminEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.MainWindow.resize(900, 600)

        current_dir = os.path.dirname(os.path.abspath(__file__))

        img_path = os.path.abspath(os.path.join(current_dir, "..", "..", "images", "fit lifestyle.jpg")).replace("\\", "/")

        self.centralwidget.setStyleSheet(f"""
        #centralwidget {{
            background-image: url({img_path});
            background-repeat: no-repeat;
            background-position: center;
            background-size: contain;
        }}
        """)
    def showWindow(self):
        self.MainWindow.show()