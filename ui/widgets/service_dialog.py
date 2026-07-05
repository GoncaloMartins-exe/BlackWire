from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QWidget

from ui.widgets.helper import *

_DIALOG_STYLE = f"""
    QDialog {{
        background-color: {BW_BG};
        border: 1px solid rgba(255, 255, 255, 14);
        border-radius: 12px;
    }}
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
"""


class ServiceDialog(QDialog):
    """Janela genérica (vazia) para um serviço, com o mesmo estilo do IconPickerDialog."""

    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setStyleSheet(_DIALOG_STYLE)
        self.setFixedSize(520, 480)

        self._build(title)

    def _build(self, title: str):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(20, 20, 20, 20)
        outer.setSpacing(12)

        header = make_label(title, color=BW_TEXT, size=15, bold=True)
        outer.addWidget(header)

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        outer.addWidget(content, 1)