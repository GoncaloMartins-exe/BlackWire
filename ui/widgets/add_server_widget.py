from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QPushButton, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QComboBox, QSizePolicy
)
from ui.widgets.helper import *
from PySide6.QtWidgets import QFileDialog

_INPUT_STYLE = f"""
    QLineEdit, QComboBox {{
        background-color: rgba(255, 255, 255, 8);
        border: 1px solid rgba(255, 255, 255, 14);
        border-radius: 8px;
        color: {BW_TEXT};
        font-size: 12px;
        padding: 6px 12px;
        selection-background-color: {BW_CYAN};
    }}
    QLineEdit:focus, QComboBox:focus {{
        border: 1px solid {BW_CYAN};
        background-color: rgba(255, 255, 255, 11);
    }}
    QLineEdit::placeholder {{
        color: {BW_TEXT_DIM};
    }}
    QComboBox::drop-down {{
        border: none;
        width: 24px;
    }}
    QComboBox::down-arrow {{
        image: none;
        width: 0;
    }}
    QComboBox QAbstractItemView {{
        background-color: #1e1e2a;
        border: 1px solid rgba(255, 255, 255, 14);
        border-radius: 8px;
        color: {BW_TEXT};
        selection-background-color: rgba(255, 255, 255, 12);
        padding: 4px;
    }}
"""

_ADD_BTN_STYLE = f"""
    QPushButton {{
        background-color: rgba(255, 255, 255, 15);
        border: 1px solid rgba(255, 255, 255, 25);
        border-radius: 8px;
        color: {BW_TEXT_DIM};
        font-size: 11px;
        padding: 5px 14px;
        margin-left: 12px;
    }}
    QPushButton:hover {{
        background-color: rgba(255, 255, 255, 20);
        color: {BW_TEXT};
    }}
"""


class AddServerForm(QWidget):

    submitted = Signal(dict)
    cancelled = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("AddServerForm")
        self.setStyleSheet("""
            QWidget#AddServerForm {
                background-color: rgba(255, 255, 255, 7);
                border: 1px solid rgba(255, 255, 255, 14);
                border-radius: 12px;
            }
        """)
        self._build()

    def _build(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(20, 16, 20, 16)
        outer.setSpacing(14)

        # ======================================================================
        # Title row
        # ======================================================================
        title_row = QHBoxLayout()
        title_row.setContentsMargins(0, 0, 0, 0)
        title_row.addWidget(make_label("New server", color=BW_TEXT, size=13, bold=True))
        title_row.addStretch()

        close = make_label("✕", color=BW_TEXT_DIM, size=12)
        close.setCursor(Qt.PointingHandCursor)
        close.setFixedSize(24, 24)
        close.setAlignment(Qt.AlignCenter)

        close.setStyleSheet("""
            QLabel { background: transparent; border: none; border-radius: 4px; }
            QLabel:hover { color: #ff4466; }
        """)

        close.mousePressEvent = lambda _e: self.cancelled.emit()

        title_row.addWidget(close, alignment=Qt.AlignTop)

        outer.addLayout(title_row)

        # ======================================================================
        # Fields row
        # ======================================================================
        fields_row = QHBoxLayout()
        fields_row.setSpacing(12)
        fields_row.setContentsMargins(0, 0, 0, 0)

        self._name = self._make_input("e.g. Production")
        self._host = self._make_input("e.g. 192.168.1.10")
        self._user = self._make_input("e.g. root")

        # ======================================================================
        # Auth selector
        # ======================================================================
        self._auth = QComboBox()

        self._auth.addItems([
            "password",
            "key"
        ])

        self._auth.setFixedHeight(34)
        self._auth.setStyleSheet(_INPUT_STYLE)

        self._auth.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )

        # ======================================================================
        # Password field
        # ======================================================================
        self._password = self._make_input("SSH password")

        self._password.setEchoMode(
            QLineEdit.Password
        )

        # ======================================================================
        # SSH key field
        # ======================================================================
        self._key_path = self._make_input(
            "SSH private key"
        )

        self._key_path.setReadOnly(True)

        self._browse_btn = QPushButton("Browse")

        self._browse_btn.setFixedHeight(34)
        self._browse_btn.setStyleSheet(_ADD_BTN_STYLE)

        self._browse_btn.clicked.connect(
            self._browse_key
        )

        key_row = QHBoxLayout()

        key_row.setContentsMargins(0, 0, 0, 0)
        key_row.setSpacing(6)

        key_row.addWidget(self._key_path)
        key_row.addWidget(self._browse_btn)

        self.key_widget = QWidget()
        self.key_widget.setLayout(key_row)
        self.key_widget.setStyleSheet("background: transparent;")

        # ======================================================================
        # Add fields
        # ======================================================================
        fields_row.addLayout(self._labeled("Name", self._name))

        fields_row.addLayout(self._labeled("Host", self._host))

        fields_row.addLayout(self._labeled("User", self._user))

        self._auth_stack = QStackedWidget()
        self._auth_stack.setStyleSheet("background: transparent;")
        self._auth_stack.addWidget(self._password)
        self._auth_stack.addWidget(self.key_widget)

        stack_col, self._auth_stack_label = self._labeled_with_label("Password", self._auth_stack)

        fields_row.addLayout(self._labeled("Auth", self._auth))
        fields_row.addLayout(stack_col)

        outer.addLayout(fields_row)

        # ======================================================================
        # Auth visibility
        # ======================================================================
        self._auth.currentTextChanged.connect(
            self._update_auth_visibility
        )

        self._update_auth_visibility()

        # ======================================================================
        # Action buttons
        # ======================================================================
        btn_row = QHBoxLayout()

        btn_row.setContentsMargins(0, 0, 0, 0)
        btn_row.setSpacing(10)

        btn_row.addStretch()

        cancel_btn = QPushButton("Cancel")

        cancel_btn.setCursor(
            Qt.PointingHandCursor
        )

        cancel_btn.setFixedHeight(32)

        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: 1px solid rgba(255, 255, 255, 18);
                border-radius: 8px;
                color: {BW_TEXT_DIM};
                font-size: 11px;
                padding: 0 16px;
            }}

            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 10);
                color: {BW_TEXT};
            }}
        """)
        cancel_btn.clicked.connect(self.cancelled.emit)

        add_btn = QPushButton("Add server")
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.setFixedHeight(32)

        add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {BW_CYAN};
                border: none;
                border-radius: 8px;
                color: #000000;
                font-size: 11px;
                font-weight: bold;
                padding: 0 18px;
            }}

            QPushButton:pressed {{
                background-color: rgba(0, 200, 200, 200);
            }}
        """)
        add_btn.clicked.connect(self._on_submit)

        btn_row.addWidget(cancel_btn)
        btn_row.addWidget(add_btn)

        outer.addLayout(btn_row)

    # ======================================================================
    # Helpers
    # ======================================================================

    def _browse_key(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select SSH Private Key"
        )

        if path:
            self._key_path.setText(path)


    def _update_auth_visibility(self):
        is_key = self._auth.currentText() == "key"
        self._auth_stack.setCurrentIndex(1 if is_key else 0)
        self._auth_stack_label.setText("SSH Key" if is_key else "Password")

    def _make_input(self, placeholder: str) -> QLineEdit:
        w = QLineEdit()
        w.setPlaceholderText(placeholder)
        w.setFixedHeight(34)
        w.setStyleSheet(_INPUT_STYLE)
        w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        return w

    @staticmethod
    def _labeled(label_text: str, widget: QWidget) -> QVBoxLayout:
        col = QVBoxLayout()
        col.setSpacing(5)
        col.setContentsMargins(0, 0, 0, 0)
        col.addWidget(make_label(label_text, color=BW_TEXT_DIM, size=10))
        col.addWidget(widget)
        return col

    def _on_submit(self):
        name = self._name.text().strip()
        host = self._host.text().strip()
        user = self._user.text().strip()

        # Reset styles
        for field in (self._name, self._host, self._user):
            field.setStyleSheet(_INPUT_STYLE)

        # RED Highlight
        invalid = False
        for field, val in [(self._name, name), (self._host, host), (self._user, user)]:
            if not val:
                field.setStyleSheet(_INPUT_STYLE + "QLineEdit { border: 1px solid #ff4466; }")
                invalid = True

        if invalid:
            return

        self.submitted.emit({
            "name": name,
            "host": host,
            "user": user,
            "auth": self._auth.currentText(),
            "password": self._password.text().strip(),
            "key_path": self._key_path.text().strip(),
        })

    @staticmethod
    def _labeled_with_label(label_text: str, widget: QWidget):
        lbl = make_label(label_text, color=BW_TEXT_DIM, size=10)
        col = QVBoxLayout()
        col.setSpacing(5)
        col.setContentsMargins(0, 0, 0, 0)
        col.addWidget(lbl)
        col.addWidget(widget)
        return col, lbl

    def clear(self):
        for child in self.findChildren(QLineEdit):
            child.clear()
        for field in (self._name, self._host, self._user):
            field.setStyleSheet(_INPUT_STYLE)