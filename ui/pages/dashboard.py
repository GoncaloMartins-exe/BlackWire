from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from ui.widgets.helper import *


class DashboardPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background-color: {BW_BG};")
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        placeholder = QLabel("Dashboard")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet(f"""
            color: {BW_TEXT_DIM};
            font-size: 22px;
            font-weight: 600;
        """)
        layout.addWidget(placeholder)