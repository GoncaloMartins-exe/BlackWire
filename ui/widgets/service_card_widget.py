from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from ui.widgets.helper import *

class ServiceCard(QWidget):
    
    def __init__(self, icon_file: str, name: str, active: bool, detail: str, parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 90)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: rgba(255, 255, 255, 15);
                border: 1px solid rgba(255, 255, 255, 25);
                border-radius: 16px;
            }}
            QWidget:hover {{
                background-color: rgba(255, 255, 255, 20);
                color: {BW_TEXT};
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        icon = load_image(icon_file, 36, 36)
        icon.setStyleSheet(f"""
            background-color: rgba(255, 255, 255, 10);
            border-radius: 10px;
            padding: 5px;
        """)

        text_col = QWidget()
        text_col.setStyleSheet("background: transparent; border: none;")
        text_layout = QVBoxLayout(text_col)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)

        status_color = BW_GREEN if active else "#ff4466"
        status_text  = "ACTIVE" if active else "INACTIVE"

        text_layout.addWidget(make_label(name, color=BW_TEXT, size=13, bold=True))
        text_layout.addWidget(make_label(status_text, color=status_color, size=10, bold=True, letter_spacing="1px"))
        text_layout.addWidget(make_label(detail, color=BW_TEXT_DIM, size=11))

        layout.addWidget(icon)
        layout.addWidget(text_col)
