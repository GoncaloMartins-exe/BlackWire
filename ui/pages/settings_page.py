from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QSlider, QComboBox
)
from ui.widgets.helper import *

def _combo_index(items: list[str], value: str) -> int:
    try:
        return items.index(value)
    except ValueError:
        return 0


# Settings Section Header ________________________________________________________

def _make_section(title: str) -> QWidget:
    section = QWidget()
    section.setStyleSheet("background: transparent;")
    layout = QVBoxLayout(section)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    layout.addWidget(make_label(
        title, color=BW_TEXT_DIM, size=10,
        bold=True, letter_spacing="1.5px"
    ))
    layout.addSpacing(2)
    layout.addWidget(make_separator())
    layout.addSpacing(12)

    return section, layout


# Settings Row ___________________________________________________________________

def _make_row(label: str, description: str, control: QWidget) -> QWidget:
    row = QWidget()
    row.setStyleSheet(f"""
        QWidget {{
            background-color: rgba(255, 255, 255, 5);
            border: 1px solid rgba(255, 255, 255, 10);
            border-radius: 8px;
        }}
    """)

    layout = QHBoxLayout(row)
    layout.setContentsMargins(16, 14, 16, 14)
    layout.setSpacing(12)

    text_col = QWidget()
    text_col.setStyleSheet("background: transparent; border: none;")
    text_layout = QVBoxLayout(text_col)
    text_layout.setContentsMargins(0, 0, 0, 0)
    text_layout.setSpacing(3)
    text_layout.addWidget(make_label(label, color=BW_TEXT, size=12))
    text_layout.addWidget(make_label(description, color=BW_TEXT_DIM, size=10))

    layout.addWidget(text_col, stretch=1)

    control.setStyleSheet(control.styleSheet() + "background: transparent; border: none;")
    layout.addWidget(control, alignment=Qt.AlignVCenter)

    return row


# Toggle Switch __________________________________________________________________

class ToggleSwitch(QWidget):

    def __init__(self, initial=False, parent=None):
        super().__init__(parent)
        self._on = initial
        self.setFixedSize(44, 24)
        self.setCursor(Qt.PointingHandCursor)
        self.setAttribute(Qt.WA_StyledBackground, True)

    def is_on(self) -> bool:
        return self._on

    def set_on(self, value: bool):
        self._on = value
        self.update()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._on = not self._on
            self.update()

    def paintEvent(self, e):
        from PySide6.QtGui import QPainter, QColor, QPainterPath
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        track_color = BW_CYAN if self._on else "#2a3a4a"
        p.setBrush(QColor(track_color))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(0, 4, 44, 16, 8, 8)

        knob_x = 22 if self._on else 2
        p.setBrush(QColor("#e0eaf5"))
        p.drawEllipse(knob_x, 2, 20, 20)
        p.end()


# Settings Page __________________________________________________________________

class SettingsPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background-color: {BW_BG};")
        self._setup_ui()

    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(0)

        # Header ─────────────────────────────────────────────────────────────────
        root.addWidget(make_label("Settings", color=BW_TEXT, size=20, bold=True))
        root.addSpacing(4)
        root.addWidget(make_label("Customize your BlackWire experience.", color=BW_TEXT_DIM, size=12))
        root.addSpacing(24)

        # Scroll area ─────────────────────────────────────────────────────────────
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setStyleSheet(f"""
            QScrollArea {{ background: transparent; border: none; }}
            QScrollBar:vertical {{
                background: transparent; width: 10px; margin: 4px 0 0 0;
            }}
            QScrollBar::handle:vertical {{
                background-color: rgba(255,255,255,15);
                border-radius: 5px; min-height: 30px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: rgba(255,255,255,20);
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0; background: none;
            }}
        """)

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 16, 0)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignTop)

        # ── Section: Connection ───────────────────────────────────────────────
        sec_conn, sec_conn_layout = _make_section("CONNECTION")
        layout.addWidget(sec_conn)

        self._combo_cpu_ram = QComboBox()
        self._combo_cpu_ram.addItems(["1s", "2s", "5s", "10s"])
        self._combo_cpu_ram.setCurrentIndex(_combo_index(["1s", "2s", "5s", "10s"], f"{dash_settings.get('cpu_ram_interval') // 1000}s"))
        self._combo_cpu_ram.currentTextChanged.connect(
            lambda t: dash_settings.set("cpu_ram_interval", int(t.replace("s", "")) * 1000)
        )
        sec_conn_layout.addWidget(_make_row(
            "CPU & RAM Refresh",
            "How often CPU and RAM usage are polled.",
            self._combo_cpu_ram,
        ))
        sec_conn_layout.addSpacing(8)

        self._combo_network = QComboBox()
        self._combo_network.addItems(["2s", "5s", "10s", "30s"])
        self._combo_network.setCurrentIndex(_combo_index(["2s", "5s", "10s", "30s"], f"{dash_settings.get('network_interval') // 1000}s"))
        self._combo_network.currentTextChanged.connect(
            lambda t: dash_settings.set("network_interval", int(t.replace("s", "")) * 1000)
        )
        sec_conn_layout.addWidget(_make_row(
            "Network Refresh",
            "How often upload, download and ping are polled.",
            self._combo_network,
        ))
        sec_conn_layout.addSpacing(8)

        self._combo_temp = QComboBox()
        self._combo_temp.addItems(["2s", "5s", "10s", "30s"])
        self._combo_temp.setCurrentIndex(_combo_index(["2s", "5s", "10s", "30s"], f"{dash_settings.get('temp_interval') // 1000}s"))
        self._combo_temp.currentTextChanged.connect(
            lambda t: dash_settings.set("temp_interval", int(t.replace("s", "")) * 1000)
        )
        sec_conn_layout.addWidget(_make_row(
            "CPU Temperature Refresh",
            "How often the CPU temperature sensor is read.",
            self._combo_temp,
        ))

        # ── Section: About ────────────────────────────────────────────────────
        sec3, sec3_layout = _make_section("ABOUT")
        layout.addWidget(sec3)

        about_card = QWidget()
        about_card.setStyleSheet(f"""
            QWidget {{
                background-color: rgba(255,255,255,5);
                border: 1px solid rgba(255,255,255,10);
                border-radius: 8px;
            }}
        """)
        about_layout = QHBoxLayout(about_card)
        about_layout.setContentsMargins(16, 14, 16, 14)
        about_layout.setSpacing(0)

        about_left = QVBoxLayout()
        about_left.setSpacing(4)
        about_left.setContentsMargins(0, 0, 0, 0)
        lbl_app = make_label("BlackWire", color=BW_TEXT, size=13, bold=True)
        lbl_app.setStyleSheet(lbl_app.styleSheet() + "background: transparent; border: none;")
        lbl_ver = make_label("Version 0.1.0", color=BW_TEXT_DIM, size=10)
        lbl_ver.setStyleSheet(lbl_ver.styleSheet() + "background: transparent; border: none;")
        lbl_desc = make_label("SSH Server Management Tool", color=BW_TEXT_DIM, size=10)
        lbl_desc.setStyleSheet(lbl_desc.styleSheet() + "background: transparent; border: none;")
        about_left.addWidget(lbl_app)
        about_left.addWidget(lbl_ver)
        about_left.addWidget(lbl_desc)

        about_layout.addLayout(about_left)
        about_layout.addStretch()

        logo = load_image("LogoBlackWire.png", 36, 36)
        logo.setStyleSheet("background: transparent; border: none;")
        about_layout.addWidget(logo, alignment=Qt.AlignVCenter)

        sec3_layout.addWidget(about_card)

        layout.addStretch()

        scroll.setWidget(content)
        root.addWidget(scroll)