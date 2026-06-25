from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QTimer
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
import warnings

# Cores predefinidas
TOAST_RED   = ("rgba(244,67,54,220)",  "rgba(244,67,54,255)",  "#FFFFFF")
TOAST_GREEN = ("rgba(0,204,136,220)",  "rgba(0,204,136,255)",  "#FFFFFF")
TOAST_CYAN  = ("rgba(0,212,255,220)",  "rgba(0,212,255,255)",  "#111827")
TOAST_WARN  = ("rgba(232,168,56,220)", "rgba(232,168,56,255)", "#111827")

# Posições
TOAST_TOP   = "top"
TOAST_RIGHT = "right"


class ToastNotification(QWidget):

    def __init__(
        self,
        parent=None,
        message: str = "Notification",
        color: tuple = TOAST_RED,
        position: str = TOAST_TOP,
        auto_hide_ms: int = 0,
    ):
        super().__init__(parent)

        self._position = position
        self._color    = color
        self._auto_hide_ms = auto_hide_ms

        if position == TOAST_RIGHT:
            self.setFixedSize(220, 34)
        else:
            self.setFixedSize(220, 34)

        self.setAttribute(Qt.WA_StyledBackground, True)
        self._apply_style(color)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)

        self._label = QLabel(message)
        self._label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._label)

        self._anim = QPropertyAnimation(self, b"pos")
        self._anim.setDuration(260)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

        self.hide()

    # Estilo ────────────────────────────────────────────────────────────────

    def _apply_style(self, color: tuple):
        bg, border, text_color = color
        self.setStyleSheet(f"""
            ToastNotification {{
                background-color: {bg};
                border: 1px solid {border};
                border-radius: 8px;
            }}
            QLabel {{
                background: transparent;
                border: none;
                color: {text_color};
                font-size: 11px;
                font-weight: 600;
            }}
        """)

    def set_color(self, color: tuple):
        self._color = color
        self._apply_style(color)

    def set_message(self, message: str):
        self._label.setText(message)

    # Posição ───────────────────────────────────────────────────────────────

    def _get_positions(self):
        parent = self.parent()
        pw, ph = parent.width(), parent.height()
        w,  h  = self.width(),   self.height()

        if self._position == TOAST_TOP:
            x       = (pw - w) // 2
            start   = QPoint(x, -50)
            end     = QPoint(x, 18)
            hide_to = QPoint(x, -50)

        else:
            y       = ph // 8
            start   = QPoint(pw + 10, y)
            end     = QPoint(pw - w - 16, y)
            hide_to = QPoint(pw + 10, y)

        return start, end, hide_to

    # Animações ─────────────────────────────────────────────────────────────

    def show_animation(self):
        if not self.parent():
            return

        start, end, _ = self._get_positions()

        self.move(start)
        self.show()
        self.raise_()

        self._anim.stop()
        self._anim.setStartValue(start)
        self._anim.setEndValue(end)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self._anim.finished.disconnect()

        self._anim.start()

        if self._auto_hide_ms > 0:
            QTimer.singleShot(self._auto_hide_ms, self.hide_animation)

    def hide_animation(self):
        if not self.parent():
            self.hide()
            return

        _, end, hide_to = self._get_positions()

        self._anim.stop()
        self._anim.setStartValue(self.pos())
        self._anim.setEndValue(hide_to)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self._anim.finished.disconnect()

        self._anim.finished.connect(self.hide)
        self._anim.start()