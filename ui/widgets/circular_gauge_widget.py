from PySide6.QtCore import Qt, QRectF
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from ui.widgets.helper import *

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