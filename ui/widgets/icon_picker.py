import os

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QGridLayout, QPushButton, QScrollArea,
    QWidget, QSizePolicy
)

from ui.widgets.helper import *

SERVER_LOGOS_DIR = os.path.join("assets", "server_logos")

DEFAULT_SERVER_ICON = "domain-servers1.png"

_SUPPORTED_EXTS = (".png", ".jpg", ".jpeg", ".svg", ".webp")

_DIALOG_STYLE = f"""
    QDialog {{
        background-color: #1e1e2a;
        border: 1px solid rgba(255, 255, 255, 14);
        border-radius: 12px;
    }}
    QScrollArea {{
        background: transparent;
        border: none;
    }}
    QScrollBar:vertical {{
        background: transparent;
        width: 8px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background: rgba(255, 255, 255, 30);
        border-radius: 4px;
        min-height: 24px;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0;
    }}
"""

_ICON_BTN_STYLE = f"""
    QPushButton {{
        background-color: rgba(255, 255, 255, 8);
        border: 1px solid rgba(255, 255, 255, 14);
        border-radius: 10px;
    }}
    QPushButton:hover {{
        background-color: rgba(255, 255, 255, 14);
        border: 1px solid {BW_CYAN};
    }}
    QPushButton:checked {{
        background-color: rgba(0, 200, 200, 40);
        border: 1px solid {BW_CYAN};
    }}
"""


def list_server_icons(directory: str = SERVER_LOGOS_DIR) -> list[str]:
    """Devolve os nomes de ficheiro (sem caminho) dos ícones disponíveis."""
    if not os.path.isdir(directory):
        return []

    names = [
        f for f in os.listdir(directory)
        if f.lower().endswith(_SUPPORTED_EXTS)
    ]
    names.sort(key=str.lower)

    # Garante que o ícone por omissão aparece sempre em primeiro lugar
    if DEFAULT_SERVER_ICON in names:
        names.remove(DEFAULT_SERVER_ICON)
        names.insert(0, DEFAULT_SERVER_ICON)

    return names


def server_icon_path(filename: str, directory: str = SERVER_LOGOS_DIR) -> str:
    return os.path.join(directory, filename)


class IconPickerDialog(QDialog):
    """Popup com grelha de miniaturas para escolher o ícone de um servidor."""

    COLUMNS = 5
    THUMB_SIZE = 56

    def __init__(self, current_icon: str = "", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Choose icon")
        self.setModal(True)
        self.setStyleSheet(_DIALOG_STYLE)
        self.setFixedSize(380, 360)

        self._selected = current_icon or DEFAULT_SERVER_ICON
        self._buttons: dict[str, QPushButton] = {}

        self._build()

    def _build(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(16, 16, 16, 16)
        outer.setSpacing(12)

        title = make_label("Choose an icon", color=BW_TEXT, size=13, bold=True)
        outer.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        grid_holder = QWidget()
        grid_holder.setStyleSheet("background: transparent;")
        grid = QGridLayout(grid_holder)
        grid.setSpacing(10)
        grid.setContentsMargins(2, 2, 2, 2)

        icons = list_server_icons()

        if not icons:
            empty = make_label(
                "No icons found in assets/server_logos/",
                color=BW_TEXT_DIM, size=11
            )
            empty.setWordWrap(True)
            grid.addWidget(empty, 0, 0, 1, self.COLUMNS)
        else:
            for index, filename in enumerate(icons):
                row, col = divmod(index, self.COLUMNS)
                btn = self._make_icon_button(filename)
                grid.addWidget(btn, row, col)
                self._buttons[filename] = btn

        grid.setRowStretch(grid.rowCount(), 1)
        scroll.setWidget(grid_holder)
        outer.addWidget(scroll, 1)

        self._sync_checked_state()

    def _make_icon_button(self, filename: str) -> QPushButton:
        btn = QPushButton()
        btn.setCheckable(True)
        btn.setFixedSize(self.THUMB_SIZE, self.THUMB_SIZE)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(_ICON_BTN_STYLE)
        btn.setToolTip(filename)
        btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        pixmap = QPixmap(server_icon_path(filename))
        if not pixmap.isNull():
            btn.setIcon(QIcon(pixmap))
            btn.setIconSize(QSize(self.THUMB_SIZE - 16, self.THUMB_SIZE - 16))

        btn.clicked.connect(lambda _checked, f=filename: self._select(f))
        return btn

    def _select(self, filename: str):
        self._selected = filename
        self._sync_checked_state()
        self.accept()

    def _sync_checked_state(self):
        for filename, btn in self._buttons.items():
            btn.setChecked(filename == self._selected)

    def selected_icon(self) -> str:
        return self._selected