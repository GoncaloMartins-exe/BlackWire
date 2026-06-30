import os
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QPixmap

# Paleta de cores BlackWire ────────────────────────────────
BW_BG         = "#0b0f1a"
BW_SURFACE    = "#111827"
BW_SURFACE2   = "#1a2235"
BW_SURFACE3   = "#212d42"
BW_BORDER     = "#1e2d40"
BW_CYAN       = "#00d4ff"
BW_GREEN      = "#00ff88"
BW_TEXT       = "#e0eaf5"
BW_TEXT_DIM   = "#5a7a99"
SIDEBAR_WIDTH = 200

def resource_path(*parts) -> str:
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base, *parts)

BW_PILL_STYLE = f"""
    QLabel, QPushButton {{
        background-color: rgba(255, 255, 255, 15);
        border: 1px solid rgba(255, 255, 255, 25);
        border-radius: 8px;
        color: {BW_TEXT_DIM};
        font-size: 11px;
        padding: 4px 14px;
        min-height: 24px;
        max-height: 24px;
    }}
    QPushButton:hover {{
        background-color: rgba(255, 255, 255, 20);
        color: {BW_TEXT};
    }}
"""

BW_CARD_STYLE = """
    QWidget {
        background-color: rgba(255, 255, 255, 5);
        border: 1px solid rgba(255, 255, 255, 10);
        border-radius: 8px;
    }
"""

def load_image(
    filename: str,
    width: int,
    height: int,
    style: str = "border: none; background: transparent",
    folder: str = "assets/icons",
) -> QLabel:
    label = QLabel()
    label.setFixedSize(width, height)
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet(style)

    path = resource_path(*folder.split("/"), filename)
    pixmap = QPixmap(path)

    if not pixmap.isNull():
        label.setPixmap(
            pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

    return label


def make_separator(
    horizontal: bool = True,
    color: str = BW_BORDER,
    thickness: int = 1,
) -> QWidget:
    sep = QWidget()
    sep.setStyleSheet(f"background-color: {color}; border: none;")
    if horizontal:
        sep.setFixedHeight(thickness)
    else:
        sep.setFixedWidth(thickness)
    return sep


def make_label(
    text: str,
    color: str = BW_TEXT,
    size: int = 13,
    bold: bool = False,
    letter_spacing: str = "normal",
    align: Qt.AlignmentFlag = Qt.AlignVCenter,
    extra_style: str = "",
) -> QLabel:
    label = QLabel(text)
    label.setAlignment(align)
    weight = "700" if bold else "500"
    label.setStyleSheet(f"""
        color: {color};
        font-size: {size}px;
        font-weight: {weight};
        letter-spacing: {letter_spacing};
        background: transparent;
        border: none;
        {extra_style}
    """)
    return label


def make_hbox(*widgets, margins=(0, 0, 0, 0), spacing=8) -> QWidget:
    container = QWidget()
    container.setStyleSheet("border: none;")
    layout = QHBoxLayout(container)
    layout.setContentsMargins(*margins)
    layout.setSpacing(spacing)
    layout.setAlignment(Qt.AlignVCenter)
    for w in widgets:
        layout.addWidget(w)
    return container

def format_bytes(num_bytes: int) -> tuple[str, str]:
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = float(num_bytes)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f}", unit
        size /= 1024

def make_pill_label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet(BW_PILL_STYLE)
    return lbl

def make_pill_button(text: str, margin_left: int = 0) -> QPushButton:
    btn = QPushButton(text)
    style = BW_PILL_STYLE
    if margin_left > 0:
        style += f" QPushButton {{ margin-left: {margin_left}px; }}"
    btn.setStyleSheet(style)
    return btn

def make_widget_card(title: str, widget: QWidget) -> QWidget:
    card = QWidget()
    card.setStyleSheet(BW_CARD_STYLE)
    layout = QVBoxLayout(card)
    layout.setAlignment(Qt.AlignCenter)
    layout.setSpacing(10)
    layout.setContentsMargins(0, 24, 0, 24)
    layout.addWidget(
        make_label(title, color=BW_TEXT_DIM, size=10,
                   letter_spacing="1.5px", align=Qt.AlignCenter)
    )
    layout.addWidget(widget, alignment=Qt.AlignCenter)
    return card