from collections import deque
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QPainterPath, QLinearGradient
from ui.widgets.helper import *

MAX_POINTS = 13  # 13 × 5s = 60s de histórico


class NetworkGraph(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._upload   = deque([0.0] * MAX_POINTS, maxlen=MAX_POINTS)
        self._download = deque([0.0] * MAX_POINTS, maxlen=MAX_POINTS)
        self._peak     = 1.0
        self.setMinimumHeight(80)

    def push(self, upload_mbps: float, download_mbps: float):
        self._upload.append(upload_mbps)
        self._download.append(download_mbps)
        self._peak = max(1.0, max(self._upload), max(self._download))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        pad_l, pad_r, pad_t, pad_b = 8, 8, 8, 20

        def x_of(i):
            return pad_l + i * (w - pad_l - pad_r) / (MAX_POINTS - 1)

        def y_of(v):
            return pad_t + (1.0 - v / self._peak) * (h - pad_t - pad_b)

        # Grid horizontal
        for frac in [0.25, 0.5, 0.75, 1.0]:
            gy = pad_t + (1.0 - frac) * (h - pad_t - pad_b)
            painter.setPen(QPen(QColor("#1e2d40"), 1, Qt.SolidLine))
            painter.drawLine(QPointF(pad_l, gy), QPointF(w - pad_r, gy))
            lbl = f"{self._peak * frac:.0f}" if frac < 1.0 else f"{self._peak:.0f} MB/s"
            painter.setPen(QColor("#334155"))
            painter.setFont(QFont("Segoe UI", 8))
            painter.drawText(QRectF(w - pad_r - 52, gy - 10, 50, 14), Qt.AlignRight, lbl)

        # Eixo X
        painter.setPen(QColor("#334155"))
        painter.setFont(QFont("Segoe UI", 8))
        for i, label in [
            (0,               f"-{(MAX_POINTS - 1) * 5}s"),
            (MAX_POINTS // 2, f"-{(MAX_POINTS - 1 - MAX_POINTS // 2) * 5}s"),
            (MAX_POINTS - 1,  "now"),
        ]:
            painter.drawText(
                QRectF(x_of(i) - 18, h - pad_b + 3, 36, 14),
                Qt.AlignCenter, label
            )

        def draw_series(data, color_hex, alpha_fill):
            points = [QPointF(x_of(i), y_of(v)) for i, v in enumerate(data)]

            path = QPainterPath()
            path.moveTo(points[0].x(), h - pad_b)
            for p in points:
                path.lineTo(p)
            path.lineTo(points[-1].x(), h - pad_b)
            path.closeSubpath()

            grad = QLinearGradient(0, pad_t, 0, h - pad_b)
            c = QColor(color_hex); c.setAlpha(alpha_fill)
            grad.setColorAt(0, c)
            c2 = QColor(color_hex); c2.setAlpha(0)
            grad.setColorAt(1, c2)
            painter.fillPath(path, grad)

            line = QPainterPath()
            line.moveTo(points[0])
            for p in points[1:]:
                line.lineTo(p)
            painter.setPen(QPen(QColor(color_hex), 1.5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawPath(line)

        draw_series(self._download, BW_CYAN,  alpha_fill=35)
        draw_series(self._upload,   BW_GREEN, alpha_fill=25)

        painter.end()

class NetworkWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._cur_up   = 0.0
        self._cur_down = 0.0

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 18)
        root.setSpacing(10)

        # Título
        root.addWidget(
            make_label("NETWORK I/O", color=BW_TEXT_DIM, size=10, letter_spacing="1.5px")
        )

        # Gráfico
        self._graph = NetworkGraph()
        root.addWidget(self._graph, stretch=1)

        # Legenda inferior
        legend = QHBoxLayout()
        legend.setContentsMargins(0, 4, 0, 0)
        legend.setSpacing(0)

        dn_col = QWidget(); dn_col.setStyleSheet("background: transparent; border: none;")
        dn_l = QVBoxLayout(dn_col); dn_l.setContentsMargins(0,0,0,0); dn_l.setSpacing(1)
        dn_l.setAlignment(Qt.AlignLeft)
        self._dn_val = make_label("↓  —", color=BW_CYAN,  size=13, bold=True)
        self._dn_lbl = make_label("Download", color=BW_TEXT_DIM, size=10)
        dn_l.addWidget(self._dn_val); dn_l.addWidget(self._dn_lbl)
        legend.addWidget(dn_col, stretch=1)

        up_col = QWidget(); up_col.setStyleSheet("background: transparent; border: none;")
        up_l = QVBoxLayout(up_col); up_l.setContentsMargins(0,0,0,0); up_l.setSpacing(1)
        up_l.setAlignment(Qt.AlignCenter)
        self._up_val = make_label("↑  —", color=BW_GREEN, size=13, bold=True)
        self._up_lbl = make_label("Upload", color=BW_TEXT_DIM, size=10)
        self._up_val.setAlignment(Qt.AlignCenter)
        self._up_lbl.setAlignment(Qt.AlignCenter)
        up_l.addWidget(self._up_val); up_l.addWidget(self._up_lbl)
        legend.addWidget(up_col, stretch=1)

        lat_col = QWidget(); lat_col.setStyleSheet("background: transparent; border: none;")
        lat_l = QVBoxLayout(lat_col); lat_l.setContentsMargins(0,0,0,0); lat_l.setSpacing(1)
        lat_l.setAlignment(Qt.AlignRight)
        self._lat_val = make_label("— ms", color=BW_TEXT, size=13, bold=True)
        self._lat_lbl = make_label("Latency", color=BW_TEXT_DIM, size=10)
        self._lat_val.setAlignment(Qt.AlignRight)
        self._lat_lbl.setAlignment(Qt.AlignRight)
        lat_l.addWidget(self._lat_val); lat_l.addWidget(self._lat_lbl)
        legend.addWidget(lat_col, stretch=1)

        root.addLayout(legend)

    def push(self, upload_mbps: float, download_mbps: float):
        self._cur_up, self._cur_down = upload_mbps, download_mbps
        self._graph.push(upload_mbps, download_mbps)
        self._dn_val.setText(f"↓  {download_mbps:.1f} MB/s")
        self._up_val.setText(f"↑  {upload_mbps:.1f} MB/s")