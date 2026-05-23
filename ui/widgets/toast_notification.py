from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout


class ToastNotification(QWidget):

    def __init__(self, parent=None, message="SSH connection lost"):
        super().__init__(parent)

        self.setFixedSize(220, 34)

        self.setAttribute(Qt.WA_StyledBackground, True)

        self.setStyleSheet("""
            ToastNotification {
                background-color: rgba(244, 67, 54, 28);
                border: 1px solid rgba(244, 67, 54, 140);
                border-radius: 8px;
            }

            QLabel {
                background: transparent;
                border: none;
                color: #FF8A80;
                font-size: 11px;
                font-weight: 600;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)

        self._label = QLabel(message)
        self._label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self._label)

        self._anim = QPropertyAnimation(self, b"pos")
        self._anim.setDuration(260)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

        self.hide()

    def show_animation(self):
        if not self.parent():
            return

        parent = self.parent()

        x = (parent.width() - self.width()) // 2

        start_y = -50
        end_y = 18

        self.move(x, start_y)

        self.show()
        self.raise_()

        self._anim.stop()

        self._anim.setStartValue(QPoint(x, start_y))
        self._anim.setEndValue(QPoint(x, end_y))

        self._anim.start()

    def hide_animation(self):
        if not self.parent():
            self.hide()
            return

        parent = self.parent()

        x = (parent.width() - self.width()) // 2

        self._anim.stop()

        self._anim.setStartValue(self.pos())
        self._anim.setEndValue(QPoint(x, -50))

        self._anim.finished.connect(self.hide)

        self._anim.start()