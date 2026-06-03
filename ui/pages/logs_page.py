from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPlainTextEdit, QLineEdit
from PySide6.QtGui import QFont
from ui.widgets.helper import *

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
        padding: 5px 14px;
    }}
"""

LOG_DISPLAY_STYLE = f"""
    QPlainTextEdit {{
        background-color: {BW_SURFACE};
        border: 1px solid {BW_BORDER};
        border-radius: 8px;
        color: {BW_GREEN};
        padding: 12px;
        selection-background-color: {BW_CYAN};
        selection-color: {BW_SURFACE};
    }}
"""


class LogsPage(QWidget):
    def __init__(self, server=None, client=None, parent=None):
        super().__init__(parent)
        self.server = server
        self.client = client
        self.setStyleSheet(f"background-color: {BW_BG};")
        self._setup_ui()

        self._timer = QTimer(self, interval=15000)
        self._timer.timeout.connect(self.refresh_logs)

    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 40)
        root.setSpacing(16)

        # Header
        self._log_selector = QComboBox(styleSheet=COMBO_STYLE)
        self._log_selector.addItems([label for label, _ in LOG_COMMANDS])
        self._log_selector.currentIndexChanged.connect(self._on_log_changed)

        self._custom_path = QLineEdit(placeholderText="/var/log/nginx/access.log", visible=False)

        self._refresh_btn = make_pill_button("⟳  Refresh")
        self._refresh_btn.clicked.connect(self.refresh_logs)

        header = QHBoxLayout()
        header.addWidget(make_label("System Logs", color=BW_TEXT, size=20, bold=True))
        header.addStretch()
        for w in (self._log_selector, self._custom_path, self._refresh_btn):
            header.addWidget(w)
        root.addLayout(header)

        # Log display
        self._log_display = QPlainTextEdit(readOnly=True, styleSheet=LOG_DISPLAY_STYLE)
        self._log_display.setFont(QFont("Consolas", 10))
        root.addWidget(self._log_display)

    def attach_session(self, server, client):
        self.server, self.client = server, client
        self.refresh_logs()
        self._timer.start()

    def _on_log_changed(self):
        self._custom_path.setVisible(self._log_selector.currentIndex() == 3)
        self._log_display.setPlainText("Loading logs...")
        self.refresh_logs()

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
        except Exception as e:
            self._log_display.setPlainText(f"Erro ao ler logs: {e}")

        QTimer.singleShot(800, lambda: self._refresh_btn.setEnabled(True))