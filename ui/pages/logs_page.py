from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPlainTextEdit, QLineEdit
from PySide6.QtGui import QFont
from ui.widgets.helper import *
from ui.widgets.toast_notification_widget import ToastNotification
from ui.services.service_config_store import load_service

LOG_COMMANDS = [
    ("System / Service (journalctl)", "journalctl -n 100 --no-pager"),
    ("Kernel Ring Buffer (dmesg)",    "dmesg | tail -n 100"),
    ("Authentication (auth.log)",     "tail -n 100 /var/log/auth.log 2>/dev/null || tail -n 100 /var/log/secure"),
    ("Custom Log File",               None),
]

COMBO_STYLE = f"""
    QComboBox {{
        background-color: rgba(255,255,255,15);
        border: 1px solid rgba(255,255,255,25);
        border-radius: 8px;
        color: {BW_TEXT};
        padding: 4px 14px;
        min-height: 24px;
        max-height: 24px;
    }}
"""

LOG_DISPLAY_STYLE = f"""
    QPlainTextEdit, QPlainTextEdit viewport{{
        background-color: {BW_SURFACE};
        border: 1px solid {BW_BORDER};
        border-radius: 8px;
        color: {BW_GREEN};
        padding: 12px;
    }}
    QScrollBar:vertical {{
        background-color: {BW_SURFACE};
        width: 10px;
        margin: 0;
        border: none;
    }}
    QScrollBar::handle:vertical {{
        background-color: rgba(255, 255, 255, 15);
        border-radius: 5px;
        min-height: 30px;
    }}
    QScrollBar::handle:vertical:hover {{
        background-color: rgba(255, 255, 255, 20);
    }}
    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {{
        height: 0;
        background: none;
    }}
    QScrollBar::add-page:vertical,
    QScrollBar::sub-page:vertical {{
        background-color: {BW_SURFACE};
    }}
"""


class LogsPage(QWidget):
    def __init__(self, server=None, client=None, service_key=None, parent=None):
        super().__init__(parent)
        self.server = server
        self.client = client
        self._connection_lost = False

        self.service_key = service_key
        self._service_cmd = None
        self._service_label = None
        if service_key:
            cfg = load_service(service_key)
            unit = cfg.get("unit", service_key)
            lines = cfg.get("log_lines", 100)
            self._service_label = cfg.get("display_name", service_key)
            self._service_cmd = f"journalctl -u {unit} -n {lines} --no-pager"

        self.setStyleSheet(f"background-color: {BW_BG};")
        self._setup_ui()

        self._timer = QTimer(self, interval=2000 if service_key else 3000)
        self._timer.timeout.connect(self.refresh_logs)

    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 40)
        root.setSpacing(16)

        self._disconnect_popup = ToastNotification(self, "SSH connection lost")
        self._disconnect_popup.hide()

        # Header
        self._log_selector = QComboBox(styleSheet=COMBO_STYLE)
        self._log_selector.addItems([label for label, _ in LOG_COMMANDS])
        self._log_selector.currentIndexChanged.connect(self._on_log_changed)

        self._custom_path = QLineEdit(placeholderText="/var/log/nginx/access.log", visible=False)

        self._refresh_btn = make_pill_button("⟳  Refresh")
        self._refresh_btn.clicked.connect(self.refresh_logs)

        header = QHBoxLayout()
        title_text = f"{self._service_label} — Live Logs" if self.service_key else "System Logs"
        header.addWidget(make_label(title_text, color=BW_TEXT, size=20, bold=True))
        header.addStretch()

        if self.service_key:
            self._log_selector = None
            self._custom_path = None
        else:
            header.addWidget(self._log_selector)
            header.addWidget(self._custom_path)

        header.addWidget(self._refresh_btn)
        root.addLayout(header)

        # Log display
        self._log_display = QPlainTextEdit(readOnly=True, styleSheet=LOG_DISPLAY_STYLE)
        self._log_display.setFont(QFont("Consolas", 10))
        root.addWidget(self._log_display)

    def _handle_connection_lost(self):
        if self._connection_lost:
            return
        self._connection_lost = True
        self._disconnect_popup.show_animation()

    def _handle_reconnected(self):
        if not self._connection_lost:
            return
        self._connection_lost = False
        self._disconnect_popup.hide()

    def attach_session(self, server, client):
        self.server, self.client = server, client
        self._connection_lost = False
        self._disconnect_popup.hide()
        self._timer.stop()
        self._timer.start()

    def _on_log_changed(self):
        self._custom_path.setVisible(self._log_selector.currentIndex() == 3)
        self._log_display.setPlainText("Loading logs...")
        self.refresh_logs()

    def showEvent(self, event):
        super().showEvent(event)
        if self.client:
            self.refresh_logs()
            if not self._timer.isActive():
                self._timer.start()

    def _scroll_to_bottom(self):
        sb = self._log_display.verticalScrollBar()
        sb.setValue(sb.maximum())

    def refresh_logs(self):
        if not self.client:
            self._log_display.setPlainText("Sem ligação SSH ativa. Seleciona um servidor no Home.")
            return

        self._refresh_btn.setEnabled(False)
        idx = self._log_selector.currentIndex()
        _, cmd = LOG_COMMANDS[idx]

        if cmd is None:  # Custom log
            path = self._custom_path.text().strip()
            if not path:
                self._log_display.setPlainText("Introduz o caminho do ficheiro de log.")
                self._refresh_btn.setEnabled(True)
                return
            cmd = f"tail -n 100 '{path}'"

        try:
            result = self.client.execute(cmd)
            output = (result or {}).get("stdout", "").strip()
            self._log_display.setPlainText(output or "O ficheiro de log está vazio ou não foi encontrado.")
            self._scroll_to_bottom()
            self._handle_reconnected()
        except Exception as e:
            self._log_display.setPlainText(f"Erro ao ler logs: {e}")
            self._handle_connection_lost()
        finally:
            QTimer.singleShot(800, lambda: self._refresh_btn.setEnabled(True))
            if not self._timer.isActive():
                self._timer.start()