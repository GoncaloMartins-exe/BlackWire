import time

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from ui.widgets.helper import *
from ui.widgets.network_widget import NetworkWidget
from ui.widgets.circular_gauge_widget import CircularGauge
from ui.widgets.server_card_widget import server_key
from ui.widgets.service_card_widget import ServiceCard
from ui.widgets.toast_notification_widget import ToastNotification
from ui.widgets.cpu_temp_widget import CpuTempCard


# Dashboard Page _________________________________________________________________

class DashboardPage(QWidget):

    def __init__(self, server=None, client=None, parent=None):
        super().__init__(parent)

        self.server = server
        self.client = client
        self._connection_lost = False

        self.network_interface = None

        self._prev_cpu_idle: int | None = None
        self._prev_cpu_total: int | None = None
        self._prev_rx: int | None = None
        self._prev_tx: int | None = None
        self._prev_time: float | None = None

        self.setStyleSheet(f"background-color: {BW_BG};")
        self._setup_ui()

        self.refresh_all()

        self._stats_timer   = self._setup_timer(dash_settings.get("cpu_ram_interval"), self.refresh_cpu_ram)
        self._uptime_timer  = self._setup_timer(dash_settings.get("uptime_interval"),  self.refresh_uptime)
        self._network_timer = self._setup_timer(dash_settings.get("network_interval"), self.refresh_network, call_immediately=True)
        self._temp_timer    = self._setup_timer(dash_settings.get("temp_interval"),    self.refresh_cpu_temp, call_immediately=True)

        dash_settings.changed.connect(self._on_settings_changed)

    # UI Construction ____________________________________________________________

    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 40)
        root.setSpacing(0)

        root.addWidget(self._build_header())

        self._disconnect_popup = ToastNotification(self, "SSH connection lost")
        self._disconnect_popup.hide()

        root.addWidget(self._build_gauges())
        root.addSpacing(12)
        root.addWidget(self._build_network(), stretch=2)
        root.addWidget(self._build_service_cards(), stretch=1)

    def _build_header(self) -> QWidget:
        header = QWidget()
        header.setStyleSheet("background: transparent")
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 16)
        layout.setSpacing(0)

        layout.addWidget(make_label("Dashboard", color=BW_TEXT, size=20, bold=True))
        layout.addStretch()

        self._uptime_label = make_pill_label("Uptime: -")
        layout.addWidget(self._uptime_label)

        self._refresh_btn = make_pill_button("⟳  Refresh", margin_left=12)
        self._refresh_btn.clicked.connect(self._on_refresh)
        layout.addWidget(self._refresh_btn)

        return header

    def _build_gauges(self) -> QWidget:
        self._cpu     = CircularGauge("CPU UTILIZATION", "CPU",     "%",  BW_CYAN)
        self._ram     = CircularGauge("RAM USAGE",       "RAM",     "GB", BW_CYAN)
        self._storage = CircularGauge("STORAGE USAGE",   "STORAGE", "GB", BW_GREEN)

        self._cpu.set_value(0, "0%")
        self._ram.set_value(0, "0 GB", "/ 0 GB")
        self._storage.set_value(0, "0 GB", "/ 0 GB")
        self._cpu_temp = CpuTempCard()

        container = QWidget()
        container.setStyleSheet("background: transparent;")
        layout = QHBoxLayout(container)
        layout.setSpacing(20)
        layout.setContentsMargins(0, 0, 0, 0)

        for gauge in [self._cpu, self._ram, self._storage, self._cpu_temp]:
            layout.addWidget(make_widget_card(gauge.title, gauge), stretch=1)

        return container

    def _build_network(self) -> NetworkWidget:
        self._network = NetworkWidget()
        self._network.setStyleSheet(BW_CARD_STYLE)
        return self._network

    def _build_service_cards(self) -> QWidget:
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        layout = QHBoxLayout(container)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(ServiceCard("placeholder.png", "WireGuard VPN", True, "X Users Connected"))
        layout.addWidget(ServiceCard("placeholder.png", "Samba NAS",     True, "X Shared Folders"))

        return container

    # Timer Helpers __________________________________________________________________

    def _setup_timer(self, interval_ms: int, callback, call_immediately=False) -> QTimer:
        timer = QTimer(self)
        timer.setInterval(interval_ms)
        timer.timeout.connect(callback)
        timer.start()
        if call_immediately:
            callback()
        return timer

    def _restart_timers(self):
        self._prev_rx = self._prev_tx = self._prev_time = None
        self.network_interface = None
        for timer in [self._stats_timer, self._uptime_timer, self._network_timer, self._temp_timer]:
            timer.stop()
            timer.start()
        self.refresh_network()
        QTimer.singleShot(500, self.refresh_network)

    def _on_settings_changed(self):
        self._stats_timer.setInterval(dash_settings.get("cpu_ram_interval"))
        self._uptime_timer.setInterval(dash_settings.get("uptime_interval"))
        self._network_timer.setInterval(dash_settings.get("network_interval"))
        self._temp_timer.setInterval(dash_settings.get("temp_interval"))

    # Data Refresh ____________________________________________________________________

    def run_command(self, cmd: str):
        if not self.client:
            return None
            
        if getattr(self, '_connection_lost', False):
            return None

        try:
            return self.client.execute(cmd)
        except Exception as e:
            self.handle_connection_lost()
            return None

    def _get_stdout(self, cmd: str) -> str | None:
        """Run a command and return stripped stdout, or None on failure."""
        result = self.run_command(cmd)
        if not result:
            return None
        stdout = result.get("stdout", "").strip()
        return stdout or None
    
    def _detect_network_interface(self):
        stdout = self._get_stdout("ip route show default | awk '{print $5}' | head -1")
        if stdout:
            self.network_interface = stdout.strip()

    def refresh_all(self):
        self.refresh_storage()
        self.refresh_cpu_ram()
        self.refresh_uptime()
        self.refresh_network()
        self.refresh_cpu_temp()

    def refresh_storage(self):
        if not self.client:
            return

        try:
            stdout = self._get_stdout("df -B1 / | tail -1")
            if not stdout:
                return

            parts = stdout.split()
            total_bytes, used_bytes = int(parts[1]), int(parts[2])
            used_val,  used_unit  = format_bytes(used_bytes)
            total_val, total_unit = format_bytes(total_bytes)
            self._storage.set_value(
                used_bytes / total_bytes,
                f"{used_val} {used_unit}",
                f"/ {total_val} {total_unit}",
            )

        except Exception as e:
            print("Storage refresh error:", e)

    def refresh_cpu_ram(self):
        if not self.client:
            return
        try:
            self._refresh_cpu()
            self._refresh_ram()
        except Exception as e:
            print("CPU/RAM refresh error:", e)

    def _refresh_cpu(self):
        stdout = self._get_stdout("head -1 /proc/stat")
        if not stdout:
            return
        parts = list(map(int, stdout.split()[1:]))
        idle = parts[3] + parts[4]
        total = sum(parts)

        if self._prev_cpu_total is not None:
            delta_idle = idle - self._prev_cpu_idle
            delta_total = total - self._prev_cpu_total
            if delta_total > 0:
                cpu_pct = 100 * (1 - delta_idle / delta_total)
                self._cpu.set_value(cpu_pct / 100, f"{cpu_pct:.0f}%")

        self._prev_cpu_idle, self._prev_cpu_total = idle, total

    def _refresh_ram(self):
        stdout = self._get_stdout("grep -E '^(MemTotal|MemAvailable):' /proc/meminfo")
        if not stdout:
            return
        lines = {
            line.split()[0].rstrip(":"): int(line.split()[1])
            for line in stdout.splitlines()
        }
        total_kb = lines.get("MemTotal", 0)
        used_kb  = total_kb - lines.get("MemAvailable", 0)
        total_gb = total_kb / 1024 ** 2
        used_gb  = used_kb  / 1024 ** 2
        self._ram.set_value(used_gb / total_gb, f"{used_gb:.1f} GB", f"/ {total_gb:.0f} GB")

    def refresh_uptime(self):
        if not self.client:
            return

        try:
            stdout = self._get_stdout("cat /proc/uptime")
            if stdout:
                self.update_uptime(int(float(stdout.split()[0])))
        except Exception as e:
            print("Uptime refresh error:", e)

    def refresh_network(self):
        if not self.client:
            return
        
        if not self.network_interface:
            self._detect_network_interface()
            if not self.network_interface:
                return

        try:
            stdout = self._get_stdout("cat /proc/net/dev")
            if not stdout:
                return

            iface_line = next(
                (l for l in stdout.splitlines() if l.strip().startswith(f"{self.network_interface}:")), None
            )
            if not iface_line:
                return

            stats    = iface_line.split(":")[1].split()
            rx_bytes = int(stats[0])
            tx_bytes = int(stats[8])

            now = time.time()
            if self._prev_rx is None:
                self._prev_rx, self._prev_tx, self._prev_time = rx_bytes, tx_bytes, now
                return

            dt = now - self._prev_time
            if dt <= 0:
                return

            down_mbps = (rx_bytes - self._prev_rx) / dt / (1024 * 1024)
            up_mbps   = (tx_bytes - self._prev_tx) / dt / (1024 * 1024)
            self._prev_rx, self._prev_tx, self._prev_time = rx_bytes, tx_bytes, now

            self._network.push(up_mbps, down_mbps, iface=self.network_interface, lat_ms=self._fetch_ping())

        except (ValueError, IndexError) as e:
            print("Network refresh error:", e)

    def _fetch_ping(self) -> float | None:
        stdout = self._get_stdout("ping -c 1 8.8.8.8 | tail -1 | awk -F'/' '{print $5}'")
        try:
            return float(stdout) if stdout else None
        except ValueError:
            return None
        
    def refresh_cpu_temp(self):
        if not self.client:
            return
        cmd = (
            "for z in /sys/class/thermal/thermal_zone*; do "
            "t=$(cat $z/type 2>/dev/null); "
            "if echo \"$t\" | grep -qiE 'x86_pkg_temp|coretemp|cpu-thermal|cpu_thermal'; then "
            "cat $z/temp; break; fi; "
            "done"
        )
        stdout = self._get_stdout(cmd)
        if stdout:
            self._cpu_temp.update_temp(float(stdout) / 1000.0)

    # UI Updates ____________________________________________________________________

    def update_uptime(self, seconds: int):
        days,  r    = divmod(seconds, 86400)
        hours, r    = divmod(r, 3600)
        mins        = r // 60
        self._uptime_label.setText(f"Uptime:  {days}d {hours}h {mins}m")

    # Connection Handling ___________________________________________________________

    def attach_session(self, server, client):
        self.server = server
        self.client = client
        self._connection_lost = False
        self._disconnect_popup.hide()
        self.refresh_all()
        self._restart_timers()

    def _on_refresh(self):
        self._refresh_btn.setEnabled(False)
        self.refresh_all()
        self._restart_timers()
        QTimer.singleShot(800, lambda: self._refresh_btn.setEnabled(True))

    def handle_connection_lost(self):
        if self._connection_lost:
            return

        self._connection_lost = True
        
        if self.client:
            self.client.close()
            self.client = None

        if callable(getattr(self, 'on_connection_lost', None)):
            self.on_connection_lost(self.server)

        if hasattr(self.server, 'checker'):
             self.server.checker.disconnect(server_key(self.server))

        self._disconnect_popup.show_animation()

        if hasattr(self, '_stats_timer'): self._stats_timer.stop()
        if hasattr(self, '_uptime_timer'): self._uptime_timer.stop()
        if hasattr(self, '_network_timer'): self._network_timer.stop()
        if hasattr(self, '_test_timer'): self._test_timer.stop()

        self._cpu.set_value(0, "OFF")
        self._ram.set_value(0, "OFF", "")
        self._storage.set_value(0, "OFF", "")
        self._uptime_label.setText("Uptime: Offline")
        self._cpu_temp.reset()
        self._prev_rx = self._prev_tx = self._prev_time = None
        self.network_interface = None
        self._network.reset()

    def handle_reconnected(self):
        if not self._connection_lost:
            return
        self._connection_lost = False
        self._disconnect_popup.hide()
        self.refresh_all()
        self._restart_timers()
        self.refresh_network()