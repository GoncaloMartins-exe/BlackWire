from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from ui.widgets.helper import BW_TEXT, BW_TEXT_DIM, BW_CYAN, BW_SURFACE, make_label


# CPU Temperature Card ___________________________________________________________

class CpuTempCard(QWidget):
    """
    Displays current CPU temperature with min/max recorded values.

    Usage:
        card = CpuTempCard()
        card.update_temp(current=62.5, min_temp=41.0, max_temp=78.0)
    """

    # Colour thresholds
    _COLD_COLOR  = BW_CYAN            # below 60 °C_setup_ui
    _WARN_COLOR  = "#E8A838"        # 60–79 °C
    _HOT_COLOR   = "#E85555"        # 80 °C and above

    def __init__(self, parent=None):
        super().__init__(parent)

        self._current: float | None = None
        self._min_temp: float | None = None
        self._max_temp: float | None = None

        self.title = "CPU TEMPERATURE"
        self.setFixedSize(200, 200)

        self._setup_ui()

    # UI Construction ____________________________________________________________

    def _setup_ui(self):

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 0, 20, 16)
        root.setSpacing(0)
        root.setAlignment(Qt.AlignCenter)

        # Main temperature value ────────────────────────────────────────────
        self._temp_label = QLabel("—")
        self._temp_label.setAlignment(Qt.AlignCenter)
        self._temp_label.setStyleSheet(
            f"color: {BW_TEXT}; font-size: 29px; font-weight: 700; background: transparent; border: none;"
        )
        root.addWidget(self._temp_label)

        # Status / description ──────────────────────────────────────────────
        self._status_label = QLabel("")
        self._status_label.setAlignment(Qt.AlignCenter)
        self._status_label.setStyleSheet(
            "color: #666666; font-size: 11px; background: transparent; border: none;"
        )
        root.addWidget(self._status_label)

        root.addSpacing(16)

        # Min / Max row ─────────────────────────────────────────────────────
        minmax_row = QWidget()
        minmax_row.setObjectName("minmaxRow")
        minmax_row.setStyleSheet("""
            QWidget#minmaxRow {
                background: transparent;
                border: none;
            }
        """)
        minmax_layout = QHBoxLayout(minmax_row)
        minmax_layout.setContentsMargins(0, 0, 0, 0)
        minmax_layout.setSpacing(15)

        self._min_widget = self._build_stat("MIN", "—")
        self._max_widget = self._build_stat("MAX", "—")

        minmax_layout.addWidget(self._min_widget, stretch=1)
        minmax_layout.addWidget(self._max_widget, stretch=1)

        root.addWidget(minmax_row)

    def _build_stat(self, label_text: str, initial_value: str) -> QWidget:
        """Build a small labelled stat column (MIN or MAX)."""
        container = QWidget()
        container.setObjectName("statContainer")
        container.setStyleSheet("""
            background: transparent;
            border: 0px;
        """)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignCenter)

        lbl = QLabel(label_text)
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet("""
            color: #555555;
            font-size: 9px;
            font-weight: 700;
            background: transparent;
            letter-spacing: 1px;
            border: none;
        """)

        val = QLabel(initial_value)
        val.setAlignment(Qt.AlignCenter)
        val.setStyleSheet(f"""
            color: {BW_TEXT_DIM};
            font-size: 13px;
            font-weight: 600;
            background: transparent;
            border: none;
        """)

        layout.addWidget(lbl)
        layout.addWidget(val)

        # Store the value label so we can update it later
        container._value_label = val
        return container

    # Public API _________________________________________________________________

    def update_temp(self, current: float, min_temp: float | None = None, max_temp: float | None = None):
        """
        Update the displayed temperature values.

        Args:
            current:   Current CPU temperature in °C.
            min_temp:  Minimum recorded temperature (session).
            max_temp:  Maximum recorded temperature (session).
        """
        self._current = current

        # Track session min / max automatically when not provided
        if min_temp is None:
            self._min_temp = min(self._min_temp, current) if self._min_temp is not None else current
        else:
            self._min_temp = min_temp

        if max_temp is None:
            self._max_temp = max(self._max_temp, current) if self._max_temp is not None else current
        else:
            self._max_temp = max_temp

        color = self._temp_color(current)

        self._temp_label.setText(f"{current:.1f} °C")
        self._temp_label.setStyleSheet(
            f"color: {BW_TEXT}; font-size: 29px; font-weight: 700; background: transparent; border: none;"
        )
        self._status_label.setText(self._status_text(current))
        self._status_label.setStyleSheet(
            f"color: {self._temp_color(current)}; font-size: 14px; background: transparent; border: none;"
        )
        self._min_widget._value_label.setText(f"{self._min_temp:.1f} °C")
        self._max_widget._value_label.setText(f"{self._max_temp:.1f} °C")

    def reset(self):
        """Reset to the offline / disconnected state."""
        self._current = self._min_temp = self._max_temp = None
        self._temp_label.setText("—")
        self._temp_label.setStyleSheet(
            f"color: {BW_CYAN}; font-size: 29px; font-weight: 700; background: transparent; border: none;"
        )
        self._status_label.setText("")
        self._min_widget._value_label.setText("—")
        self._max_widget._value_label.setText("—")

    # Helpers ____________________________________________________________________

    def _temp_color(self, temp: float) -> str:
        if temp >= 80:
            return self._HOT_COLOR
        if temp >= 60:
            return self._WARN_COLOR
        return self._COLD_COLOR

    @staticmethod
    def _status_text(temp: float) -> str:
        if temp >= 80:
            return "Running hot"
        if temp >= 60:
            return "Moderate load"
        return "Normal"