import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from ui.main_window import MainWindow

app = QApplication(sys.argv)
app.setApplicationName("BlackWire")
app.setOrganizationName("BlackWire")

window = MainWindow()
window.show()

app.exec()