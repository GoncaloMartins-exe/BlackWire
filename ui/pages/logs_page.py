from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QPlainTextEdit)
from PySide6.QtGui import QFont
from ui.widgets.helper import *

class LogsPage(QWidget):
    def __init__(self, server=None, client=None, parent=None):
        super().__init__(parent)
        
        self.server = server
        self.client = client

        self.setStyleSheet(f"background-color: {BW_BG};")
        self._setup_ui()

        # Timer de auto-refresh (ex: a cada 15 segundos)
        self._timer = QTimer(self)
        self._timer.setInterval(15000)
        self._timer.timeout.connect(self.refresh_logs)

    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 40)
        root.setSpacing(16)

        # ===========================================================================
        # Header (Título + ComboBox + Botão Refresh)
        # ===========================================================================
        header_layout = QHBoxLayout()
        title = make_label("System Logs", color=BW_TEXT, size=20, bold=True)
        header_layout.addWidget(title)
        header_layout.addStretch()

        self._log_selector = QComboBox()
        self._log_selector.addItems([
            "System / Service (journalctl)",
            "Kernel Ring Buffer (dmesg)",
            "Authentication (auth.log)"
        ])
        self._log_selector.setStyleSheet(f"""
            QComboBox {{
                background-color: rgba(255, 255, 255, 15);
                border: 1px solid rgba(255, 255, 255, 25);
                border-radius: 8px;
                color: {BW_TEXT};
                padding: 5px 14px;
            }}
        """)
        self._log_selector.currentIndexChanged.connect(self._on_log_changed)
        header_layout.addWidget(self._log_selector)

        self._refresh_btn = QPushButton("⟳  Refresh")
        self._refresh_btn.setStyleSheet(BW_PILL_STYLE) # Reutilizamos o estilo do helper
        self._refresh_btn.clicked.connect(self.refresh_logs)
        header_layout.addWidget(self._refresh_btn)

        root.addLayout(header_layout)

        # ===========================================================================
        # Log Viewer (Terminal Style)
        # ===========================================================================
        self._log_display = QPlainTextEdit()
        self._log_display.setReadOnly(True)
        self._log_display.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {BW_SURFACE};
                border: 1px solid {BW_BORDER};
                border-radius: 8px;
                color: {BW_GREEN};
                padding: 12px;
                selection-background-color: {BW_CYAN};
                selection-color: {BW_SURFACE};
            }}
        """)
        
        font = QFont("Consolas", 10)
        font.setStyleHint(QFont.Monospace)
        self._log_display.setFont(font)
        
        root.addWidget(self._log_display)

    def attach_session(self, server, client):
        self.server = server
        self.client = client
        self.refresh_logs()
        self._timer.start()

    def _on_log_changed(self):
        self._log_display.clear()
        self._log_display.setPlainText("Loading logs...")
        self.refresh_logs()

    def refresh_logs(self):
        if not self.client:
            self._log_display.setPlainText("Sem ligação SSH ativa. Seleciona um servidor no Home.")
            return

        self._refresh_btn.setEnabled(False)

        log_type = self._log_selector.currentIndex()
        if log_type == 0:
            cmd = "journalctl -n 100 --no-pager"
        elif log_type == 1:
            cmd = "dmesg | tail -n 100"
        elif log_type == 2:
            cmd = "tail -n 100 /var/log/auth.log 2>/dev/null || tail -n 100 /var/log/secure"
        
        try:
            result = self.client.execute(cmd)
            if result and "stdout" in result:
                output = result["stdout"].strip()
                self._log_display.setPlainText(output if output else "O ficheiro de log está vazio ou não foi encontrado.")
                
                # Desce automaticamente a barra de scroll para veres o registo mais recente
                scrollbar = self._log_display.verticalScrollBar()
                scrollbar.setValue(scrollbar.maximum())
        except Exception as e:
            self._log_display.setPlainText(f"Erro ao ler logs: {e}")

        # Reativa botão após 800ms
        QTimer.singleShot(800, lambda: self._refresh_btn.setEnabled(True))