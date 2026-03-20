from PyQt6.QtWidgets import QApplication, QMainWindow

from ui.statistic.StatisticMainWindowEx import StatisticMainWindowEx

# from StatisticMainWindowEx import StatisticMainWindowEx

qApp = QApplication([])
qmainWindow = QMainWindow()

window = StatisticMainWindowEx()
window.setupUi(qmainWindow)
window.show()

qApp.exec()