import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PySide6.QtGui import QIcon
from ui.main_window import MainWindow

app = QApplication(sys.argv)
app.setApplicationName("BlackWire")
app.setOrganizationName("BlackWire")
app.setWindowIcon(QIcon("assets/icons/LogoBlackWire"))

window = MainWindow()
window.show()

app.exec()