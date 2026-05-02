from PySide6.QtCore import Qt, QRectF, QPointF, QTimer
from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QPainterPath, QLinearGradient
from ui.widgets.helper import *
from collections import deque
from ui.widgets.network_widget import NetworkWidget
import random

class CircularGauge(QWidget):

    def __init__(self, title: str, label: str, unit: str, color: str, parent=None):
        super().__init__(parent)
        self.title = title
        self.label = label
        self.unit = unit
        self.color = color
        self._value = 0.0
        self._display = "—"
        self._sub = ""
        self.setFixedSize(200, 200)

    def set_value(self, value: float, display: str, sub: str = ""):
        """value: 0.0 a 1.0 (percentagem), display: texto central, sub: linha abaixo."""
        self._value = max(0.0, min(1.0, value))
        self._display = display
        self._sub = sub
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        margin = 18
        rect = QRectF(margin, margin, w - margin * 2, h - margin * 2)

        # ===========================================================================
        # Arco de fundo
        # ===========================================================================
        pen_bg = QPen(QColor("#1e2d40"), 8)
        pen_bg.setCapStyle(Qt.RoundCap)
        painter.setPen(pen_bg)
        painter.drawArc(rect, -220 * 16, -280 * 16)

        # ===========================================================================
        # Arco de valor
        # ===========================================================================
        if self._value > 0:
            pen_fg = QPen(QColor(self.color), 8)
            pen_fg.setCapStyle(Qt.RoundCap)
            painter.setPen(pen_fg)
            span = int(-280 * 16 * self._value)
            painter.drawArc(rect, -220 * 16, span)

        cx, cy = w // 2, h // 2

        # ===========================================================================
        # Label topo
        # ===========================================================================
        painter.setPen(QColor(BW_TEXT_DIM))
        f = QFont("Segoe UI", 9)
        painter.setFont(f)
        painter.drawText(QRectF(0, cy - 38, w, 20), Qt.AlignCenter, self.label)

        # ===========================================================================
        # Valor principal
        # ===========================================================================
        painter.setPen(QColor(BW_TEXT))
        f2 = QFont("Segoe UI", 22, QFont.Bold)
        painter.setFont(f2)
        painter.drawText(QRectF(0, cy - 18, w, 36), Qt.AlignCenter, self._display)

        # ===========================================================================
        # Sub-texto
        # ===========================================================================
        if self._sub:
            painter.setPen(QColor(BW_TEXT_DIM))
            f3 = QFont("Segoe UI", 9)
            painter.setFont(f3)
            painter.drawText(QRectF(0, cy + 18, w, 20), Qt.AlignCenter, self._sub)

        painter.end()


class ServiceCard(QWidget):
    
    def __init__(self, icon_file: str, name: str, active: bool, detail: str, parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 90)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: rgba(255, 255, 255, 15);
                border: 1px solid rgba(255, 255, 255, 25);
                border-radius: 16px;
            }}
            QWidget:hover {{
                background-color: rgba(255, 255, 255, 20);
                color: {BW_TEXT};
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        icon = load_image(icon_file, 36, 36)
        icon.setStyleSheet(f"""
            background-color: rgba(255, 255, 255, 10);
            border-radius: 10px;
            padding: 5px;
        """)

        text_col = QWidget()
        text_col.setStyleSheet("background: transparent; border: none;")
        text_layout = QVBoxLayout(text_col)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)

        status_color = BW_GREEN if active else "#ff4466"
        status_text  = "ACTIVE" if active else "INACTIVE"

        text_layout.addWidget(make_label(name, color=BW_TEXT, size=13, bold=True))
        text_layout.addWidget(make_label(status_text, color=status_color, size=10, bold=True, letter_spacing="1px"))
        text_layout.addWidget(make_label(detail, color=BW_TEXT_DIM, size=11))

        layout.addWidget(icon)
        layout.addWidget(text_col)


class DashboardPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background-color: {BW_BG};")
        self._setup_ui()

    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 40)
        root.setSpacing(0)

        # ===========================================================================
        # Header
        # ===========================================================================
        header = QWidget()
        header.setStyleSheet("background: transparent")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 16)
        header_layout.setSpacing(0)

        title = make_label("Dashboard", color=BW_TEXT, size=20, bold=True)
        header_layout.addWidget(title)
        header_layout.addStretch()

        self._uptime_label = QLabel("Uptime: -")
        self._uptime_label.setStyleSheet(f"""
            QLabel {{
                background-color: rgba(255, 255, 255, 15);
                border: 1px solid rgba(255, 255, 255, 25);
                border-radius: 8px;
                color: {BW_TEXT_DIM};
                font-size: 11px;
                padding: 5px 14px;
            }}
        """)

        header_layout.addWidget(self._uptime_label)

        refresh_btn = QPushButton("↻  Refresh")
        refresh_btn.setStyleSheet(f"""
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
        """)

        refresh_btn.clicked.connect(self._on_refresh)
        header_layout.addWidget(refresh_btn)

        root.addWidget(header)

        # ===========================================================================
        # Gauges
        # ===========================================================================
        gauges_widget = QWidget()
        gauges_widget.setStyleSheet("background: transparent;")
        gauges_layout = QHBoxLayout(gauges_widget)
        gauges_layout.setSpacing(20)
        gauges_layout.setContentsMargins(0, 0, 0, 0)

        self._cpu     = CircularGauge("CPU UTILIZATION",     "CPU",     "%",    BW_CYAN)
        self._ram     = CircularGauge("RAM USAGE",           "RAM",     "GB",   BW_CYAN)
        self._storage = CircularGauge("STORAGE AVAILABILITY","STORAGE", "GB",   BW_GREEN)

        self._cpu.set_value(1, "100%")
        self._ram.set_value(0.5, "0 GB", "/ 0 GB")
        self._storage.set_value(0, "0 GB", "/ 0 GB")

        for gauge in [self._cpu, self._ram, self._storage]:
            col = QWidget()
            col.setStyleSheet(f"""
                QWidget {{
                    background-color: rgba(255, 255, 255, 5);
                    border: 1px solid rgba(255,255,255,10);
                    border-radius: 8px;
                }}
            """)
            col_layout = QVBoxLayout(col)
            col_layout.setAlignment(Qt.AlignCenter)
            col_layout.setSpacing(10)
            col_layout.setContentsMargins(0, 24, 0, 24)
            col_layout.addWidget(make_label(gauge.title, color=BW_TEXT_DIM, size=10, letter_spacing="1.5px", align=Qt.AlignCenter))
            col_layout.addWidget(gauge, alignment=Qt.AlignCenter)
            gauges_layout.addWidget(col, stretch=1)
        
        root.addWidget(gauges_widget)
        root.addSpacing(12)

        # ===========================================================================
        # Network card
        # ===========================================================================
        self._network = NetworkWidget()
        self._network.setStyleSheet(f"""
            QWidget {{
                background-color: rgba(255, 255, 255, 5);
                border: 1px solid rgba(255,255,255,10);
                border-radius: 8px;
                p
            }}
        """)
        root.addWidget(self._network, stretch=2)

        # ===========================================================================
        # Service cards
        # ===========================================================================
        cards_widget = QWidget()
        cards_widget.setStyleSheet("background: transparent;")
        cards_layout = QHBoxLayout(cards_widget)
        cards_layout.setAlignment(Qt.AlignCenter)
        cards_layout.setSpacing(20)
        cards_layout.setContentsMargins(0, 0, 0, 0)

        cards_layout.addWidget(ServiceCard("placeholder.png", "WireGuard VPN", True,  "X Users Connected"))
        cards_layout.addWidget(ServiceCard("placeholder.png", "Samba NAS",     True,  "X Shared Folders"))

        root.addWidget(cards_widget, stretch=1)

    def update_stats(self, cpu: float, ram_used: float, ram_total: float, storage_free: float, storage_total: float):
        self._cpu.set_value(cpu / 100, f"{cpu:.0f}%")
        self._ram.set_value(ram_used / ram_total, f"{ram_used:.1f} GB", f"/ {ram_total:.0f} GB")
        self._storage.set_value(storage_free / storage_total, f"{storage_free:.1f} GB", f"/ {storage_total:.1f}")

    def update_uptime(self, seconds: int):
        days, r = divmod(seconds, 86400)
        hours, r = divmod(r, 3600)
        mins = r // 60
        self._uptime_label.setText(f"Uptime:  {days}d {hours}h {mins}m")

    def _on_refresh(self):
        # tenho de ligar ao servidor aqui
        pass