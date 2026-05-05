from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
    QGridLayout, QLineEdit, QSizePolicy
)
from ui.widgets.helper import *
from ui.widgets.add_server_widget import AddServerForm, _ADD_BTN_STYLE

_SERVERS: list[dict] = [
    {"name": "Production", "host": "192.168.1.10", "user": "root", "auth": "key"},
    {"name": "Staging",    "host": "192.168.1.20", "user": "ubuntu", "auth": "password"},
    {"name": "Dev",        "host": "127.0.0.1", "user": "dev", "auth": "key"},
    {"name": "Production", "host": "192.168.1.10", "user": "root", "auth": "key"},
    {"name": "Staging",    "host": "192.168.1.20", "user": "ubuntu", "auth": "password"},
    {"name": "Dev",        "host": "127.0.0.1", "user": "dev", "auth": "key"},
    {"name": "Production", "host": "192.168.1.10", "user": "root", "auth": "key"},
    {"name": "Staging",    "host": "192.168.1.20", "user": "ubuntu", "auth": "password"},
    {"name": "Dev",        "host": "127.0.0.1", "user": "dev", "auth": "key"},
    {"name": "Production", "host": "192.168.1.10", "user": "root", "auth": "key"},
    {"name": "Staging",    "host": "192.168.1.20", "user": "ubuntu", "auth": "password"},
    {"name": "Dev",        "host": "127.0.0.1", "user": "dev", "auth": "key"},
    {"name": "Production", "host": "192.168.1.10", "user": "root", "auth": "key"},
    {"name": "Staging",    "host": "192.168.1.20", "user": "ubuntu", "auth": "password"},
    {"name": "Dev",        "host": "127.0.0.1", "user": "dev", "auth": "key"},
]


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

class HomePage(QWidget):

    server_selected = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background-color: {BW_BG};")
        self._setup_ui()

    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(48, 40, 48, 40)
        root.setSpacing(0)

        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)

        title_col = QVBoxLayout()
        title_col.setSpacing(4)
        title_col.addWidget(make_label("Servers", color=BW_TEXT, size=22, bold=True))
        title_col.addWidget(make_label(
            "Select a server to connect.",
            color=BW_TEXT_DIM, size=12
        ))

        header.addLayout(title_col)
        header.addStretch()

        # =========================================================
        # Add server button
        # =========================================================
        self._add_btn = QPushButton("+  Add server")
        self._add_btn.setCursor(Qt.PointingHandCursor)
        self._add_btn.setStyleSheet(_ADD_BTN_STYLE)
        self._add_btn.clicked.connect(self._on_add_clicked)

        header.addWidget(self._add_btn)

        root.addLayout(header)
        root.addSpacing(20)

        # ======================================================================
        # Inline form (hidden by default)
        # ======================================================================
        self._form = AddServerForm()
        self._form.submitted.connect(self._on_server_submitted)
        self._form.cancelled.connect(self._hide_form)
        self._form.setVisible(False)
        root.addWidget(self._form)
        root.addSpacing(20)

        # ======================================================================
        # Scroll / grid
        # ======================================================================
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                background: transparent;
                border: none;
            }}

            QScrollBar:vertical {{
                background: transparent;
                width: 10px;
                margin: 4px 0 4px 0;
            }}

            QScrollBar::handle:vertical {{
                background-color: rgba(255, 255, 255, 15);
                border-radius: 5px;
                min-height: 30px;
            }}

            QScrollBar::handle:vertical:hover {{
                background-color: rgba(255, 255, 255, 20);
            }}

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{
                height: 0;
                background: none;
            }}

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {{
                background: transparent;
            }}
        """)

        container = QWidget()
        self._grid = QGridLayout(container)
        self._grid.setSpacing(16)
        self._grid.setContentsMargins(0, 0, 12, 0)
        self._grid.setAlignment(Qt.AlignTop)

        scroll.setWidget(container)
        root.addWidget(scroll)

        self._refresh_grid()

    # ======================================================================
    # Form
    # ======================================================================
    def _on_add_clicked(self):
        self._form.clear()
        self._form.setVisible(True)
        self._add_btn.setEnabled(False)

    def _hide_form(self):
        self._form.setVisible(False)
        self._add_btn.setEnabled(True)

    def _on_server_submitted(self, server: dict):
        _SERVERS.append(server)
        self._refresh_grid()
        self._hide_form()

    # ======================================================================
    # Grid
    # ======================================================================
    def _refresh_grid(self):
        while self._grid.count():
            item = self._grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        cols = 3
        for i, server in enumerate(_SERVERS):
            card = ServerCard(server)
            card.clicked.connect(self.server_selected.emit)
            card.delete_req.connect(self._delete_server)
            self._grid.addWidget(card, i // cols, i % cols)

    def _delete_server(self, server: dict):
        if server in _SERVERS:
            _SERVERS.remove(server)
            self._refresh_grid()