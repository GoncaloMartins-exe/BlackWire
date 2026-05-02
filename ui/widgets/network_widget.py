from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from ui.widgets.helper import *

MAX_POINTS = 13  # 13 × 5s = 60s de histórico


class NetworkGraph(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(80)


class NetworkWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)

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
        self._dn_val.setText(f"↓  {download_mbps:.1f} MB/s")
        self._up_val.setText(f"↑  {upload_mbps:.1f} MB/s")