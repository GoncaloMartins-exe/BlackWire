from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtWidgets import (
    QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
    QGridLayout
)
from ui.widgets.helper import *
from ui.widgets.add_server_widget import AddServerForm, _ADD_BTN_STYLE
from ui.widgets.server_card_widget import ServerCard, server_key
from core.storage import ServerManager
from core.server_checker import ServerChecker


class HomePage(QWidget):

    server_selected = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background-color: {BW_BG};")

        self.storage = ServerManager()
        self._servers = self.storage.load_servers()

        self._cards = {}
        self._checker = ServerChecker()
        self._editing_index = None

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh_server_status)
        self._timer.start(30000)

        self._setup_ui()

    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(48, 40, 64, 40)
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
        header.setContentsMargins(0, 0, 16, 0)
        header.addStretch()

        # =========================================================
        # Refresh and Add server button
        # =========================================================
        self._refresh_btn = QPushButton("⟳ Refresh")
        self._refresh_btn.setCursor(Qt.PointingHandCursor)
        self._refresh_btn.setStyleSheet(_ADD_BTN_STYLE)
        self._refresh_btn.clicked.connect(self._manual_refresh)

        self._add_btn = QPushButton("+  Add server")
        self._add_btn.setCursor(Qt.PointingHandCursor)
        self._add_btn.setStyleSheet(_ADD_BTN_STYLE)
        self._add_btn.clicked.connect(self._on_add_clicked)

        header.addWidget(self._refresh_btn)
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

        form_layout = QHBoxLayout()
        form_layout.setContentsMargins(0, 0, 16, 0)
        form_layout.addWidget(self._form)
        root.addLayout(form_layout)
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
                margin: 4px 0 0 0;
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
        self._grid.setContentsMargins(0, 0, 16, 0)
        self._grid.setAlignment(Qt.AlignTop)

        scroll.setWidget(container)
        root.addWidget(scroll)

        self._refresh_grid()

    # ======================================================================
    # Form
    # ======================================================================
    def _on_add_clicked(self):
        self._editing_index = None
        self._form.clear()
        self._form.setVisible(True)
        self._add_btn.setEnabled(False)

    def _hide_form(self):
        self._form.setVisible(False)
        self._add_btn.setEnabled(True)

    def _on_server_submitted(self, server: dict):
        # =========================================================
        # Editing existing server
        # =========================================================
        if self._editing_index is not None:

            old_server = self._servers[self._editing_index]
            self.storage.delete_server_creds(old_server)
            self._servers[self._editing_index] = server
            self._editing_index = None

        # =========================================================
        # Adding new server
        # =========================================================
        else:
            self._servers.append(server)

        self.storage.save_all(self._servers)
        self._refresh_grid()
        self._hide_form()

    # ======================================================================
    # Grid
    # ======================================================================
    def _refresh_grid(self):
        self._cards.clear()

        while self._grid.count():
            item = self._grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        cols = 1
        for i, server in enumerate(self._servers):
            card = ServerCard(server)

            key = server_key(server)
            self._cards[key] = card

            card.clicked.connect(self._on_server_clicked)
            card.delete_req.connect(self._delete_server)
            card.edit_req.connect(self._edit_server)
            self._grid.addWidget(card, i // cols, i % cols)

        self._refresh_server_status()

    def _delete_server(self, server: dict):
        if server in self._servers:

            if self._editing_index is not None:
                try:
                    if self._servers[self._editing_index] == server:
                        self._editing_index = None
                        self._hide_form()
                except IndexError:
                    pass

            self.storage.delete_server_creds(server)
            self._servers.remove(server)
            self.storage.save_all(self._servers)
            self._refresh_grid()

    def _edit_server(self, server: dict):
        self._editing_index = self._servers.index(server)

        self._form.set_data(server)
        self._form.setVisible(True)

        self._add_btn.setEnabled(False)

    def _refresh_server_status(self):
        for server in self._servers:
            key = server_key(server)

            card = self._cards.get(key)
            
            client = self._checker.get_connection(key)
            
            if client and not client.is_active():
                self._checker.disconnect(key)
                if card: 
                    card.set_status("offline")
                continue

            if card:
                card.set_status("checking")

            self._checker.check(
                server,
                key,
                self._on_server_checked
            )

    def _on_server_checked(self, key: str, online: bool):
        card = self._cards.get(key)

        if not card:
            return

        card.set_status("online" if online else "offline")
        card.setEnabled(online)

    def _manual_refresh(self):
        self._refresh_btn.setEnabled(False)

        self._checker.reset_running()
        self._refresh_server_status()

        self._timer.stop()
        self._timer.start(30000)

        QTimer.singleShot(800, lambda: self._refresh_btn.setEnabled(True))

    def _on_server_clicked(self, server: dict):
        key = server_key(server)
        client = self._checker.get_connection(key)

        if client and not client.is_active():
            self._checker.disconnect(key)
            card = self._cards.get(key)
            if card: 
                card.set_status("offline")
            return
        
        if not client:
            card = self._cards.get(key)
            if card: 
                card.set_status("checking")
            self._checker.check(server, key, self._on_server_checked)
            return
    
        self.server_selected.emit({
            "server": server,
            "client": client
        })