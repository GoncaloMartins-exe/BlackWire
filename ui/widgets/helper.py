import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QPixmap

# Paleta de cores BlackWire ────────────────────────────────
BW_BG         = "#0b0f1a"
BW_SURFACE    = "#111827"
BW_SURFACE2   = "#1a2235"
BW_BORDER     = "#1e2d40"
BW_CYAN       = "#00d4ff"
BW_GREEN      = "#00ff88"
BW_TEXT       = "#e0eaf5"
BW_TEXT_DIM   = "#5a7a99"
SIDEBAR_WIDTH = 200

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_image(
    filename: str,
    width: int,
    height: int,
    style: str = "border: none;",
    folder: str = "assets/icons",
) -> QLabel:
    label = QLabel()
    label.setFixedSize(width, height)
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet(style)

    path = os.path.join(PROJECT_ROOT, *folder.split("/"), filename)
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