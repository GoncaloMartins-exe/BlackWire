from collections import deque
from PySide6.QtCore import Qt, QRectF, QPointF, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QPainterPath, QLinearGradient
from ui.widgets.helper import *

MAX_POINTS = 13  # 13 × 5s = 60s de histórico


class NetworkGraph(QWidget):

    # Emite (index, upload_mbps, download_mbps) ao fazer hover numa coluna
    # index == -1 significa que o rato saiu - repor valores actuais
    column_hovered = Signal(int, float, float)
    pad_l, pad_r, pad_t, pad_b = 8, 52, 8, 20

    def __init__(self, parent=None):
        super().__init__(parent)
        self._upload   = deque([0.0] * MAX_POINTS, maxlen=MAX_POINTS)
        self._download = deque([0.0] * MAX_POINTS, maxlen=MAX_POINTS)
        self._peak     = 1.0
        self._hover_i  = -1          # coluna actualmente sob o cursor
        self.setMinimumHeight(80)
        self.setMouseTracking(True)

    def push(self, upload_mbps: float, download_mbps: float):
        self._upload.append(upload_mbps)
        self._download.append(download_mbps)
        self._peak = max(1.0, max(self._upload), max(self._download))
        self.update()

    # ==================================================================
    # Eventos de rato
    # ==================================================================
    def mouseMoveEvent(self, event):
        w = self.width()
        usable = w - self.pad_l - self.pad_r
        x = event.position().x() - self.pad_l
        i = int(round(x / usable * (MAX_POINTS - 1)))
        i = max(0, min(MAX_POINTS - 1, i))
        if i != self._hover_i:
            self._hover_i = i
            up_list = list(self._upload)
            dn_list = list(self._download)
            self.column_hovered.emit(i, up_list[i], dn_list[i])
            self.update()

    def leaveEvent(self, event):
        self._hover_i = -1
        self.column_hovered.emit(-1, 0.0, 0.0)
        self.update()

    # ==================================================================
    # Pintura
    # ==================================================================
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()

        def x_of(i):
            return self.pad_l + i * (w - self.pad_l - self.pad_r) / (MAX_POINTS - 1)

        def y_of(v):
            return self.pad_t + (1.0 - v / self._peak) * (h - self.pad_t - self.pad_b)

        # Grid horizontal
        for frac in [0.25, 0.5, 0.75, 1.0]:
            gy = self.pad_t + (1.0 - frac) * (h - self.pad_t - self.pad_b)
            painter.setPen(QPen(QColor("#1e2d40"), 1, Qt.SolidLine))
            painter.drawLine(QPointF(self.pad_l, gy), QPointF(w - self.pad_r, gy))
            lbl = f"{self._peak * frac:.0f}" if frac < 1.0 else f"{self._peak:.0f} MB/s"
            painter.setPen(QColor("#334155"))
            painter.setFont(QFont("Segoe UI", 8))
            painter.drawText(QRectF(w - self.pad_r + 4, gy - 7, self.pad_r - 4, 14), Qt.AlignLeft, lbl)

        # Marcas de tempo eixo X
        painter.setPen(QColor("#334155"))
        painter.setFont(QFont("Segoe UI", 8))
        for i, label in [
            (0,               f"-{(MAX_POINTS - 1) * 5}s"),
            (MAX_POINTS // 2, f"-{(MAX_POINTS - 1 - MAX_POINTS // 2) * 5}s"),
            (MAX_POINTS - 1,  "now"),
        ]:
            painter.drawText(
                QRectF(x_of(i) - 18, h - self.pad_b + 3, 36, 14),
                Qt.AlignCenter, label
            )

        # Linha de hover vertical
        if self._hover_i >= 0:
            hx = x_of(self._hover_i)
            pen_h = QPen(QColor("#ffffff"), 1, Qt.DashLine)
            pen_h.setDashPattern([3, 4])
            painter.setPen(pen_h)
            painter.setOpacity(0.25)
            painter.drawLine(QPointF(hx, self.pad_t), QPointF(hx, h - self.pad_b))
            painter.setOpacity(1.0)

        def draw_series(data, color_hex, alpha_fill=40):
            points = [QPointF(x_of(i), y_of(v)) for i, v in enumerate(data)]

            # Área preenchida
            path = QPainterPath()
            path.moveTo(points[0].x(), h - self.pad_b)
            for p in points:
                path.lineTo(p)
            path.lineTo(points[-1].x(), h - self.pad_b)
            path.closeSubpath()

            grad = QLinearGradient(0, self.pad_t, 0, h - self.pad_b)
            c = QColor(color_hex); c.setAlpha(alpha_fill)
            grad.setColorAt(0, c)
            c2 = QColor(color_hex); c2.setAlpha(0)
            grad.setColorAt(1, c2)
            painter.fillPath(path, grad)

            # Linha
            line = QPainterPath()
            line.moveTo(points[0])
            for p in points[1:]:
                line.lineTo(p)
            painter.setPen(QPen(QColor(color_hex), 1.5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawPath(line)

            # Ponto de hover
            if self._hover_i >= 0:
                hp = points[self._hover_i]
                painter.setPen(QPen(QColor(color_hex), 2))
                painter.setBrush(QColor(color_hex))
                painter.drawEllipse(hp, 4, 4)
                painter.setBrush(Qt.NoBrush)

        draw_series(self._download, BW_CYAN,  alpha_fill=35)
        draw_series(self._upload,   BW_GREEN, alpha_fill=25)

        painter.end()

class NetworkWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)

        # Valores actuais (usados para repor a legenda ao sair do hover)
        self._cur_up   = 0.0
        self._cur_down = 0.0
        self._cur_lat  = None   # ms ou None se desconhecido

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 18)
        root.setSpacing(10)

        # Header: título + interface
        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)
        header.setSpacing(0)

        header.addWidget(
            make_label("NETWORK I/O", color=BW_TEXT_DIM, size=10, letter_spacing="1.5px")
        )
        header.addStretch()

        # Badge da interface (ex: "eth0" ou "wlan0")
        self._iface_badge = QWidget()
        self._iface_badge.setAttribute(Qt.WA_StyledBackground, True)
        self._iface_badge.setStyleSheet("""
            QWidget {
                background-color: rgba(255,255,255,8);
                border: 1px solid rgba(255,255,255,15);
                border-radius: 5px;
            }
        """)
        badge_layout = QHBoxLayout(self._iface_badge)
        badge_layout.setContentsMargins(8, 3, 8, 3)
        badge_layout.setSpacing(5)

        # Ícone: ponto colorido (verde = com fio, azul = wireless)
        self._iface_dot = QWidget()
        self._iface_dot.setFixedSize(6, 6)
        self._iface_dot.setAttribute(Qt.WA_StyledBackground, True)
        self._iface_dot.setStyleSheet("background-color: #22c55e; border-radius: 3px; border: none;")

        self._iface_label = make_label("—", color=BW_TEXT_DIM, size=10)
        badge_layout.addWidget(self._iface_dot)
        badge_layout.addWidget(self._iface_label)
        header.addWidget(self._iface_badge)

        root.addLayout(header)

        # Gráfico
        self._graph = NetworkGraph()
        self._graph.column_hovered.connect(self._on_hover)
        root.addWidget(self._graph, stretch=1)

        # Legenda inferior
        legend = QHBoxLayout()
        legend.setContentsMargins(0, 4, 0, 0)
        legend.setSpacing(0)

        # Download
        dn_col,  self._dn_val,  self._dn_lbl  = self._make_legend_col("↓  —",  BW_CYAN,  "Download", Qt.AlignLeft)
        # Upload
        up_col,  self._up_val,  self._up_lbl  = self._make_legend_col("↑  —",  BW_GREEN, "Upload",   Qt.AlignCenter)
        # Latência
        lat_col, self._lat_val, self._lat_lbl = self._make_legend_col("— ms",  BW_TEXT,  "Latency",  Qt.AlignRight)

        legend.addWidget(dn_col,  stretch=1)
        legend.addWidget(up_col,  stretch=1)
        legend.addWidget(lat_col, stretch=1)

        root.addLayout(legend)

    # ------------------------------------------------------------------
    # Slots
    # ------------------------------------------------------------------
    def _on_hover(self, index: int, upload: float, download: float):
        if index == -1:
            # Repor valores actuais
            self._update_legend(self._cur_up, self._cur_down, self._cur_lat, hover=False)
        else:
            offset = MAX_POINTS - 1 - index          # quantos segundos atrás
            ago    = offset * 5
            suffix = f"  ({ago}s before)" if ago > 0 else "  (now)"
            self._dn_val.setText(f"↓  {download:.1f} MB/s{suffix}")
            self._up_val.setText(f"↑  {upload:.1f} MB/s{suffix}")
            self._dn_lbl.setText("Download")
            self._up_lbl.setText("Upload")

    def _update_legend(self, up: float, down: float, lat_ms, hover=False):
        self._dn_val.setText(f"↓  {down:.1f} MB/s")
        self._up_val.setText(f"↑  {up:.1f} MB/s")
        self._dn_lbl.setText("Download")
        self._up_lbl.setText("Upload")
        if lat_ms is not None:
            self._lat_val.setText(f"{lat_ms:.0f} ms")
            color = BW_GREEN if lat_ms < 30 else (BW_CYAN if lat_ms < 80 else "#f59e0b")
            self._lat_val.setStyleSheet(f"color: {color}; font-size: 13px; font-weight: bold; background: transparent;")
        else:
            self._lat_val.setText("— ms")

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------
    def push(self, upload_mbps: float, download_mbps: float,
             iface: str = "", lat_ms: float = None):
        
        self._cur_up, self._cur_down, self._cur_lat = upload_mbps, download_mbps, lat_ms
        self._graph.push(upload_mbps, download_mbps)
        self._update_legend(upload_mbps, download_mbps, lat_ms)

        if iface:
            self._iface_label.setText(iface)
            
            is_wireless = iface.startswith("w") # Wireless se o nome começar por 'w', com fio nos restantes
            dot_color   = BW_CYAN if is_wireless else "#22c55e"
            self._iface_dot.setStyleSheet(
                f"background-color: {dot_color}; border-radius: 3px; border: none;"
            )

    def _make_legend_col(self, val_text, val_color, lbl_text, alignment=Qt.AlignLeft):
        col = QWidget()
        col.setStyleSheet("background: transparent; border: none;")
        layout = QVBoxLayout(col)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)
        layout.setAlignment(alignment)
        val = make_label(val_text, color=val_color, size=13, bold=True)
        lbl = make_label(lbl_text, color=BW_TEXT_DIM, size=10)
        val.setAlignment(alignment)
        lbl.setAlignment(alignment)
        layout.addWidget(val)
        layout.addWidget(lbl)
        return col, val, lbl