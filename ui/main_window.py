import sys
import os

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QStackedWidget
)
from PySide6.QtGui import QFont
from ui.pages.dashboard import DashboardPage
from ui.widgets.helper import *


class SidebarButton(QWidget):

    def __init__(self, icon_file: str, label: str, parent=None):
        super().__init__(parent)
        self._label = label
        self._active = False
        self._hover = False

        self.setAttribute(Qt.WA_StyledBackground, True)

        self.setFixedHeight(48)
        self.setCursor(Qt.PointingHandCursor)
        self.setObjectName("SidebarButton")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignCenter)

        self._icon = load_image(icon_file, 20, 20)
        self._text = make_label(label, color=BW_TEXT_DIM)

        layout.addWidget(self._icon)
        layout.addWidget(self._text)
        layout.addStretch()

        self._update_style()

    def set_active(self, active: bool):
        self._active = active
        self._update_style()

    def _update_style(self):
        if self._active:
            self.setStyleSheet(f"""
                QWidget#SidebarButton {{
                    background-color: {BW_SURFACE2};
                    border-left: 3px solid {BW_CYAN};
                }}
            """)
            self._text.setStyleSheet(f"color: {BW_CYAN}; font-size: 13px; font-weight: 500; border: none; background-color: transparent;")
        else:
            self.setStyleSheet("""
                QWidget#SidebarButton {
                    background: transparent;
                    border-left: 3px solid transparent;
                }
            """)
            self._text.setStyleSheet(f"color: {BW_TEXT_DIM}; font-size: 13px; font-weight: 500; border: none; background-color: transparent;")

    def enterEvent(self, event):
        if not self._active:
            self.setStyleSheet(f"""
                QWidget#SidebarButton {{
                    background-color: {BW_SURFACE3};
                    border-left: 3px solid transparent;
                }}
            """)
            self._text.setStyleSheet(f"color: {BW_TEXT}; font-size: 13px; font-weight: 500; border: none; background-color: transparent;")

    def leaveEvent(self, event):
        self._update_style()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if hasattr(self, '_on_click'):
                self._on_click(self._label)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BlackWire")
        self.setMinimumSize(QSize(1080, 720))
        self.resize(1080, 720)
        self.setStyleSheet(f"""
                           QMainWindow {{ background-color: {BW_BG}; }}
                           """)
        
        root = QWidget()
        root.setStyleSheet(f"background-color: {BW_BG};")
        self.setCentralWidget(root)

        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        root_layout.addWidget(self._build_sidebar())
        root_layout.addWidget(self._build_pages())

    # Sidebar__________________________________________________________________________________
    def _build_sidebar(self) -> QWidget:
        sidebar = QWidget()
        sidebar.setFixedWidth(SIDEBAR_WIDTH)
        sidebar.setStyleSheet(f"background-color: {BW_SURFACE}; border-right: 1px solid {BW_BORDER};")

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Logo_________________________________________________________________________________
        logo = make_hbox(
            load_image("LogoBlackWire.png", 36, 36),
            make_label("BLACKWIRE", color=BW_CYAN, size=13, bold=True, letter_spacing="2px"),
            margins=(16, 0, 16, 0),
            spacing=10,
        )
        logo.setFixedHeight(72)
        layout.addWidget(logo)

        layout.addWidget(make_separator())
        layout.addSpacing(12)

        # Botões de navegação_________________________________________________________________
        pages = [
            ("placeholder.png", "Dashboard"),
            ("placeholder.png", "Logs"),
            ("placeholder.png", "Files"),
            ("placeholder.png", "Settings"),
        ]

        self._sidebar_buttons = []
        for icon_file, label in pages:
            btn = SidebarButton(icon_file, label)
            btn._on_click = self._navigate
            layout.addWidget(btn)
            self._sidebar_buttons.append(btn)

        self._sidebar_buttons[0].set_active(True)

        layout.addStretch()

        layout.addWidget(make_separator())
        layout.addWidget(make_label("v0.1.0", color=BW_TEXT_DIM, size=11, align=Qt.AlignCenter, extra_style="padding: 10px 0;"))

        return sidebar

    # Stack de páginas________________________________________________________________________
    def _build_pages(self) -> QStackedWidget:
        self._stack = QStackedWidget()
        self._stack.setStyleSheet(f"background-color: {BW_BG};")

        self._pages = {
            "Dashboard": DashboardPage(),
            "Logs":      self._placeholder("Logs"),
            "Files":     self._placeholder("Files"),
            "Settings":  self._placeholder("Settings"),
        }

        for page in self._pages.values():
            self._stack.addWidget(page)

        return self._stack

    # Navegação_______________________________________________________________________________
    def _navigate(self, label: str):
        keys = list(self._pages.keys())
        if label in keys:
            self._stack.setCurrentIndex(keys.index(label))
        for btn in self._sidebar_buttons:
            btn.set_active(btn._label == label)

    # Placeholder genérico____________________________________________________________________
    def _placeholder(self, name: str) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignVCenter)
        layout.setSpacing(16)

        layout.addWidget(load_image("placeholder.png", 64, 64), alignment=Qt.AlignCenter)
        layout.addWidget(make_label(name, color=BW_TEXT_DIM, size=20, bold=True, align=Qt.AlignCenter))
        layout.addWidget(make_label("Em breve...", color=BW_CYAN, size=12, letter_spacing="2px", align=Qt.AlignCenter))

        return page