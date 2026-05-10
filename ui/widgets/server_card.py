from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox
from ui.widgets.helper import *

_STATUS_STYLES = {
    #              text         text color       bg color               border color
    "online":   ("● Online",   "#00cc88", "rgba(0,204,136,12)",   "rgba(0,204,136,55)"),
    "offline":  ("● Offline",  "#ff4466", "rgba(255,68,102,12)",  "rgba(255,68,102,55)"),
    "checking": ("● Cheking",  "#888899", "rgba(255,255,255,7)",  "rgba(255,255,255,25)"),
}


def server_key(s: dict) -> str:
    """Stable unique key for a server entry."""
    return f"{s['name']}|{s['host']}|{s['user']}"


class ServerCard(QWidget):

    clicked    = Signal(dict)
    delete_req = Signal(dict)
    edit_req   = Signal(dict)

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

        actions = QWidget()
        actions.setStyleSheet("background: transparent; border: none;")

        actions_layout = QHBoxLayout(actions)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setSpacing(4)

        # =========================================================
        # Edit button
        # =========================================================
        edit_container = QWidget()
        edit_container.setCursor(Qt.PointingHandCursor)
        edit_container.setStyleSheet(f"""
            QWidget {{
                background-color: rgba(255,255,255,8);
                border: 1px solid rgba(255,255,255,12);
                border-radius: 4px;
            }}

            QWidget:hover {{
                border: 1px solid rgba(85,187,255,120);
                background-color: rgba(85,187,255,12);
            }}
        """)

        edit_layout = QHBoxLayout(edit_container)
        edit_layout.setContentsMargins(8, 3, 8, 3)
        edit_layout.setSpacing(6)

        edit_icon = load_image("edit.png", 10, 10)
        edit_icon.setStyleSheet("background: transparent; border: none;")

        edit_text = make_label("Edit", color=BW_TEXT_DIM, size=10)
        edit_text.setStyleSheet("background: transparent; border: none;")

        edit_layout.addWidget(edit_icon)
        edit_layout.addWidget(edit_text)

        edit_container.mousePressEvent = lambda e: self.edit_req.emit(self._server)

        # =========================================================
        # Delete button
        # =========================================================
        delete_container = QWidget()
        delete_container.setCursor(Qt.PointingHandCursor)
        delete_container.setStyleSheet(f"""
            QWidget {{
                background-color: rgba(255,255,255,8);
                border: 1px solid rgba(255,255,255,12);
                border-radius: 4px;
            }}

            QWidget:hover {{
                border: 1px solid rgba(255,68,102,120);
                background-color: rgba(255,68,102,12);
            }}
        """)

        delete_layout = QHBoxLayout(delete_container)
        delete_layout.setContentsMargins(8, 3, 8, 3)
        delete_layout.setSpacing(0)

        delete_icon = load_image("delete.png", 8, 8)
        delete_icon.setStyleSheet("background: transparent; border: none;")

        delete_layout.addWidget(delete_icon)

        def on_delete(_e):

            msg = QMessageBox(self)
            msg.setWindowTitle("Delete Server")
            msg.setText(
                f"Are you sure you want to delete <b>{self._server['name']}</b>?"
            )
            msg.setIcon(QMessageBox.NoIcon)

            # =========================================================
            # Buttons
            # =========================================================
            yes_btn = msg.addButton("Delete", QMessageBox.AcceptRole)
            no_btn = msg.addButton("Cancel", QMessageBox.RejectRole)

            msg.setDefaultButton(no_btn)

            # =========================================================
            # Style
            # =========================================================
            msg.setStyleSheet(f"""
                QMessageBox {{
                    background-color: rgba(20, 20, 28, 255);
                }}

                QLabel {{
                    color: {BW_TEXT};
                    font-size: 12px;
                    background: transparent;
                    border: none;
                }}

                QMessageBox QLabel {{
                    color: {BW_TEXT};
                    background: transparent;
                }}

                QPushButton {{
                    background-color: rgba(255,255,255,10);
                    border: 1px solid rgba(255,255,255,16);
                    border-radius: 8px;
                    color: {BW_TEXT_DIM};
                    min-width: 90px;
                    min-height: 32px;
                    padding: 4px 12px;
                    font-size: 11px;
                }}

                QPushButton:hover {{
                    background-color: rgba(255,255,255,16);
                    color: {BW_TEXT};
                }}
            """)

            # =========================================================
            # Delete style
            # =========================================================
            yes_btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255,68,102,18);
                    border: 1px solid rgba(255,68,102,60);
                    color: #ff4466;
                    font-weight: bold;
                }

                QPushButton:hover {
                    background-color: rgba(255,68,102,28);
                }
            """)

            msg.exec()

            # =========================================================
            # Action
            # =========================================================
            if msg.clickedButton() == yes_btn:
                self.delete_req.emit(self._server)

        delete_container.mousePressEvent = on_delete

        actions_layout.addWidget(edit_container)
        actions_layout.addWidget(delete_container)

        top.addWidget(actions, alignment=Qt.AlignTop)

        outer.addLayout(top)

        bottom = QHBoxLayout()
        bottom.setContentsMargins(0, 0, 0, 0)
        bottom.setSpacing(0)

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

        self._status_badge = QLabel()
        self._status_badge.setStyleSheet("background: transparent; border: none;")

        bottom.addWidget(auth_tag, alignment=Qt.AlignLeft | Qt.AlignVCenter)
        bottom.addStretch()
        bottom.addWidget(self._status_badge, alignment=Qt.AlignRight | Qt.AlignVCenter)

        outer.addLayout(bottom)

        self.set_status("checking")

    def set_status(self, state: str):
        """state: 'online' | 'offline' | 'checking'"""
        text, color, bg, border = _STATUS_STYLES.get(state, _STATUS_STYLES["checking"])
        self._status_badge.setText(text)
        self._status_badge.setStyleSheet(f"""
            QLabel {{
                background-color: {bg};
                border: 1px solid {border};
                border-radius: 4px;
                padding: 2px 8px;
                color: {color};
                font-size: 10px;
            }}
        """)

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