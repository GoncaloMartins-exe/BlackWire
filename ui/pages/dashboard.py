from PySide6.QtCore import Qt, QRectF, QPointF, QTimer
from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QPainterPath, QLinearGradient
from ui.widgets.helper import *
from collections import deque
from ui.widgets.network_widget import NetworkWidget
from ui.widgets.circular_gauge_widget import CircularGauge
from ui.widgets.service_card_widget import ServiceCard
import random

def format_bytes(num_bytes: int):
    units = ["B", "KB", "MB", "GB", "TB", "PB"]

    size = float(num_bytes)

    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f}", unit

        size /= 1024

class DashboardPage(QWidget):

    def __init__(self, server=None, client=None, parent=None):
        super().__init__(parent)

        self.server = server
        self.client = client

        self.setStyleSheet(f"background-color: {BW_BG};")
        self._setup_ui()

        self.refresh_all()
        
        # Timers
        self._test_tick = 0
        self._test_timer = self._setup_timer(5000, self._push_test_data, call_immediately=True)
        
        self._stats_timer = self._setup_timer(2000, self.refresh_cpu_ram)
        
        self._uptime_timer = self._setup_timer(60000, self.refresh_uptime)

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

        refresh_btn = QPushButton("⟳  Refresh")
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
        self._storage = CircularGauge("STORAGE USAGE",       "STORAGE", "GB",   BW_GREEN)

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
        self.refresh_all()

    def _push_test_data(self):
        import math
        t = self._test_tick
        up   = round(10 + 8  * math.sin(t * 0.4), 1)
        down = round(40 + 30 * math.sin(t * 0.3 + 1.0), 1)
        lat  = round(15 + 10 * math.sin(t * 0.5), 1)
        self._network.push(up, down, iface="eth0", lat_ms=lat)
        self._test_tick += 1
    
    def run_command(self, cmd: str):
        if not self.client:
            return None

        return self.client.execute(cmd)
    
    def attach_session(self, server, client):
        self.server = server
        self.client = client

        self.refresh_all()

    def refresh_all(self):
        self.refresh_storage()
        self.refresh_cpu_ram()
        self.refresh_uptime()

    def refresh_storage(self):
        if not self.client:
            return

        try:
            result = self.run_command("df -B1 / | tail -1")

            if not result:
                return

            stdout = result.get("stdout", "").strip()

            if not stdout:
                return

            parts = stdout.split()

            total_bytes = int(parts[1])
            used_bytes  = int(parts[2])

            usage = used_bytes / total_bytes

            used_value, used_unit = format_bytes(used_bytes)
            total_value, total_unit = format_bytes(total_bytes)

            self._storage.set_value(
                usage,
                f"{used_value} {used_unit}",
                f"/ {total_value} {total_unit}"
            )

        except Exception as e:
            print("Storage refresh error:", e)

    def refresh_cpu_ram(self):
        if not self.client:
            return

        try:
            result = self.run_command("top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'")
            if result:
                stdout = result.get("stdout", "").strip()
                if stdout:
                    cpu = float(stdout)
                    self._cpu.set_value(cpu / 100, f"{cpu:.0f}%")

            # RAM: MemTotal e MemAvailable em kB
            result = self.run_command("grep -E '^(MemTotal|MemAvailable):' /proc/meminfo")
            if result:
                stdout = result.get("stdout", "").strip()
                if stdout:
                    lines = {line.split()[0].rstrip(":"): int(line.split()[1])
                             for line in stdout.splitlines()}
                    total_kb = lines.get("MemTotal", 0)
                    avail_kb = lines.get("MemAvailable", 0)
                    used_kb  = total_kb - avail_kb

                    total_gb = total_kb / (1024 ** 2)
                    used_gb  = used_kb  / (1024 ** 2)

                    self._ram.set_value(
                        used_gb / total_gb,
                        f"{used_gb:.1f} GB",
                        f"/ {total_gb:.0f} GB"
                    )

        except Exception as e:
            print("CPU/RAM refresh error:", e)

    def refresh_uptime(self):
        if not self.client:
            return

        try:
            result = self.run_command("cat /proc/uptime")
            if result:
                stdout = result.get("stdout", "").strip()
                if stdout:
                    seconds = int(float(stdout.split()[0]))
                    self.update_uptime(seconds)

        except Exception as e:
            print("Uptime refresh error:", e)

    def _setup_timer(self, interval_ms: int, callback, call_immediately: bool = False):
        timer = QTimer(self)
        timer.setInterval(interval_ms)
        timer.timeout.connect(callback)
        timer.start()
        
        if call_immediately:
            callback()
            
        return timer