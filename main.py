import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from ui.main_window import MainWindow
from pathlib import Path

def resource_path(path):
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return str(base / path)

app = QApplication(sys.argv)
app.setApplicationName("BlackWire")
app.setOrganizationName("BlackWire")
app.setWindowIcon(QIcon(resource_path("assets/icons/LogoBlackWire.png")))

window = MainWindow()
window.show()

app.aboutToQuit.connect(window.on_quit)

sys.exit(app.exec())