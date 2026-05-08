from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout
)
from ui.widgets.helper import *

class ServerCard(QWidget):

    clicked    = Signal(dict)
    delete_req = Signal(dict)

    def __init__(self, server: dict, parent=None):
        super().__init__(parent)
        self._server = server
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(110)
        self._set_style(False)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(20, 16, 20, 16)
        outer.setSpacing(6)

        top = QHBoxLayout()
        top.setSpacing(12)
        top.setContentsMargins(0, 0, 0, 0)

        icon = load_image("server.png", 28, 28)
        icon.setStyleSheet("background: transparent; border: none;")
        top.addWidget(icon)

        name_col = QWidget()
        name_col.setStyleSheet("background: transparent; border: none;")
        nc = QVBoxLayout(name_col)
        nc.setContentsMargins(0, 0, 0, 0)
        nc.setSpacing(2)
        nc.addWidget(make_label(server["name"], color=BW_TEXT, size=13, bold=True))
        nc.addWidget(make_label(
            f"{server['user']}@{server['host']}",
            color=BW_TEXT_DIM, size=11
        ))
        top.addWidget(name_col, stretch=1)

        del_btn = make_label("✕", color=BW_TEXT_DIM, size=12)
        del_btn.setCursor(Qt.PointingHandCursor)
        del_btn.setFixedSize(24, 24)
        del_btn.setAlignment(Qt.AlignCenter)
        del_btn.setStyleSheet("""
            QLabel { background: transparent; border: none; border-radius: 4px; }
            QLabel:hover { color: #ff4466; }
        """)
        del_btn.mousePressEvent = lambda e: self.delete_req.emit(self._server)
        top.addWidget(del_btn, alignment=Qt.AlignTop)

        outer.addLayout(top)

        auth_tag = make_label(
            "Password" if server.get("auth") == "password" else "Key",
            color=BW_TEXT_DIM, size=10
        )
        auth_tag.setStyleSheet(f"""
            QLabel {{
                background-color: rgba(255,255,255,8);
                border: 1px solid rgba(255,255,255,12);
                border-radius: 4px;
                padding: 2px 8px;
                color: {BW_TEXT_DIM};
            }}
        """)
        outer.addWidget(auth_tag, alignment=Qt.AlignLeft)

    def _set_style(self, hover: bool):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {"rgba(255,255,255,12)" if hover else "rgba(255,255,255,7)"};
                border: 1px solid {BW_CYAN if hover else "rgba(255,255,255,12)"};
                border-radius: 12px;
            }}
        """)

    def enterEvent(self, e): self._set_style(True)
    def leaveEvent(self, e): self._set_style(False)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.clicked.emit(self._server)