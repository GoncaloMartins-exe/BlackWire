import sys
import os

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)
from PySide6.QtGui import QPixmap

# Palete de cores
BW_BG       = "#0b0f1a"
BW_SURFACE  = "#111827"
BW_BORDER   = "#1e2d40"
BW_CYAN     = "#00d4ff"
BW_GREEN    = "#00ff88"
BW_TEXT     = "#e0eaf5"
BW_TEXT_DIM = "#5a7a99"


class NavButton(QPushButton):
    """Botão de navegação da navbar com estado ativo."""

    def __init__(self, label: str, parent=None):
        super().__init__(label, parent)
        self.setCheckable(True)
        self.setFixedHeight(64)
        self.setMinimumWidth(90)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {BW_TEXT_DIM};
                border: none;
                border-bottom: 2px solid transparent;
                font-size: 12px;
                font-weight: 500;
                letter-spacing: 0.5px;
                padding: 0 16px;
            }}
            QPushButton:hover {{
                color: {BW_TEXT};
            }}
            QPushButton:checked {{
                color: {BW_CYAN};
                border-bottom: 2px solid {BW_CYAN};
            }}
        """)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BlackWire")
        self.setMinimumSize(QSize(1080, 720))
        self.resize(1080, 720)

        self.setStyleSheet(f"QMainWindow {{ background-color: {BW_BG}; }}")

        root = QWidget()
        root.setStyleSheet(f"background-color: {BW_BG};")
        self.setCentralWidget(root)

        layout = QVBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self._build_navbar())
        layout.addWidget(self._build_content())

    # Navbar
    def _build_navbar(self) -> QWidget:
        navbar = QWidget()
        navbar.setFixedHeight(64)
        navbar.setStyleSheet(f"""
            background-color: {BW_SURFACE};
            border-bottom: 1px solid {BW_BORDER};
        """)

        nav_layout = QHBoxLayout(navbar)
        nav_layout.setContentsMargins(24, 0, 24, 0)
        nav_layout.setSpacing(0)

        base_dir = os.path.dirname(os.path.dirname(__file__))
        logo_path = os.path.join(base_dir, "assets", "icons", "LogoBlackWire.png")

        # Imagem
        logo_img = QLabel()
        pixmap = QPixmap(logo_path)
        logo_img.setPixmap(pixmap.scaled(45, 45, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_img.setFixedSize(45, 45)
        logo_img.setStyleSheet("border: none;")

        # Texto
        logo_text = QLabel("BLACKWIRE")
        logo_text.setStyleSheet(f"""
            color: {BW_CYAN};
            font-size: 15px;
            font-weight: 700;
            letter-spacing: 3px;
            padding-left: 8px;
            padding-right: 24px;
        """)

        logo_container = QWidget()
        logo_layout = QHBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setSpacing(0)

        logo_layout.addWidget(logo_img)
        logo_layout.addWidget(logo_text)

        nav_layout.addWidget(logo_container)

        return navbar

    # Conteúdo principal
    def _build_content(self) -> QWidget:
        content = QWidget()
        content.setStyleSheet(f"background-color: {BW_BG};")

        layout = QVBoxLayout(content)
        layout.setAlignment(Qt.AlignCenter)

        placeholder = QLabel("Dashboard")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet(f"""
            color: {BW_TEXT_DIM};
            font-size: 22px;
            font-weight: 600;
        """)
        layout.addWidget(placeholder)

        return content