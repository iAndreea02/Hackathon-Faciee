from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QGraphicsOpacityEffect, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QSequentialAnimationGroup, QPoint
from PyQt5.QtGui import QPainter, QLinearGradient, QColor, QPixmap
import sys

class StartPage(QWidget):
    def __init__(self):
        super().__init__()

        # Colors
        self.bgStart = QColor("#0A0E1A")
        self.bgEnd = QColor("#001F30")

        self.setMinimumSize(480, 800)
        self._build_ui()
        self._animate()

    def _build_ui(self):
        # ROBOT
        self.robot = QLabel(self)
        self.robot.setPixmap(QPixmap("robo.png").scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.robot.setAlignment(Qt.AlignCenter)
        self.robot.setFixedSize(250, 250)
        self.robot.move((480 - 250) // 2, 300)

        self.glow = QGraphicsDropShadowEffect()
        self.glow.setBlurRadius(40)
        self.glow.setColor(QColor("#E21ADB"))
        self.glow.setOffset(0, 0)
        self.robot.setGraphicsEffect(self.glow)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        self.layout.addStretch()

        # TITLU
        self.title = QLabel("Hello, viitor student!")
        self.title.setStyleSheet("font-size:38px; font-weight:bold; color:#E21ADB;")
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)

        # SUBTITLU
        self.subtitle = QLabel("Facultatea ACIEE te așteaptă!")
        self.subtitle.setStyleSheet("font-size:16px; color:#00E0FF;")
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.subtitle)

        self.layout.addSpacing(290)

        # BUTTON
        self.button = QPushButton("Intră în aplicație")
        self.button.setStyleSheet("""
            QPushButton {
                background:#E21ADB;
                color:white;
                font-size:22px;
                font-weight:bold;
                padding:15px;
                border-radius:8px;
            }
            QPushButton:hover {
                background:#f545e6;
            }
        """)
        self.layout.addWidget(self.button)

        self.layout.addStretch()

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, self.bgStart)
        gradient.setColorAt(1, self.bgEnd)
        painter.fillRect(self.rect(), gradient)

    def _animate(self):
        # Floating robot
        start = self.robot.pos()
        end = QPoint(start.x(), start.y() - 25)

        self.up = QPropertyAnimation(self.robot, b"pos")
        self.up.setDuration(4000)
        self.up.setStartValue(start)
        self.up.setEndValue(end)
        self.up.setEasingCurve(QEasingCurve.InOutQuad)

        self.down = QPropertyAnimation(self.robot, b"pos")
        self.down.setDuration(4000)
        self.down.setStartValue(end)
        self.down.setEndValue(start)
        self.down.setEasingCurve(QEasingCurve.InOutQuad)

        self.float = QSequentialAnimationGroup()
        self.float.addAnimation(self.up)
        self.float.addAnimation(self.down)
        self.float.setLoopCount(-1)
        self.float.start()

        # Glow pulsation
        self.glow_anim1 = QPropertyAnimation(self.glow, b"blurRadius")
        self.glow_anim1.setDuration(1200)
        self.glow_anim1.setStartValue(30)
        self.glow_anim1.setEndValue(55)

        self.glow_anim2 = QPropertyAnimation(self.glow, b"blurRadius")
        self.glow_anim2.setDuration(1200)
        self.glow_anim2.setStartValue(55)
        self.glow_anim2.setEndValue(30)

        self.glow_seq = QSequentialAnimationGroup()
        self.glow_seq.addAnimation(self.glow_anim1)
        self.glow_seq.addAnimation(self.glow_anim2)
        self.glow_seq.setLoopCount(-1)
        self.glow_seq.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = StartPage()
    win.show()
    sys.exit(app.exec_())
