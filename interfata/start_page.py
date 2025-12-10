from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QGraphicsOpacityEffect, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QSequentialAnimationGroup
from PySide6.QtGui import QPainter, QLinearGradient, QColor, QPixmap
import sys

class StartPage(QWidget):
    def __init__(self):
        super().__init__()

        # Colors
        self.bgStart = QColor("#0A0E1A")
        self.bgEnd = QColor("#001F30")
        self.accentPink = QColor("#E21ADB")
        self.accentCyan = QColor("#00E0FF")

        # 480x800 layout like portrait tablet
        self.setMinimumSize(480, 800)

        self._build_ui()
        self._animate()

    def _build_ui(self):
        # ---------   ROBOT   -------------
        self.robot = QLabel(self)
        self.robot.setPixmap(QPixmap("robo.png").scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.robot.setAlignment(Qt.AlignCenter)
        self.robot.setFixedSize(250, 250)
        # Poziție fixă - centrat orizontal, la 300px de sus
        self.robot.move((480 - 250) // 2, 300)
        
        # Glow effect pentru robot
        self.glow_effect = QGraphicsDropShadowEffect()
        self.glow_effect.setBlurRadius(40)
        self.glow_effect.setColor(QColor("#E21ADB"))
        self.glow_effect.setOffset(0, 0)
        self.robot.setGraphicsEffect(self.glow_effect)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        # Add stretch to push content to center
        self.layout.addStretch()

        # ------------  TITLU  ------------
        self.title = QLabel("Hello, viitor student!")
        self.title.setStyleSheet("font-size:38px; font-weight:bold; color:#E21ADB;")
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)

        # ---------- SUBTITLU -------------
        self.subtitle = QLabel("Facultatea ACIEE te așteaptă!")
        self.subtitle.setStyleSheet("font-size:16px; color:#00E0FF;")
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.subtitle)

        # Spațiu pentru robot (care e poziționat absolut)
        self.layout.addSpacing(290)

        # ----------  BUTONUL START ----------
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
        
        # Add stretch to push content to center
        self.layout.addStretch()

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, self.bgStart)
        gradient.setColorAt(1, self.bgEnd)
        painter.fillRect(self.rect(), gradient)

    def _animate(self):
        # Floating robot animation - ultra smooth
        self.float_up = QPropertyAnimation(self.robot, b"pos")
        self.float_up.setDuration(4000)
        pos = self.robot.pos()
        self.float_up.setStartValue(pos)
        self.float_up.setEndValue(pos + self.robot.pos().__class__(0, -25))
        self.float_up.setEasingCurve(QEasingCurve.InOutQuart)
        
        self.float_down = QPropertyAnimation(self.robot, b"pos")
        self.float_down.setDuration(4000)
        self.float_down.setStartValue(pos + self.robot.pos().__class__(0, -25))
        self.float_down.setEndValue(pos)
        self.float_down.setEasingCurve(QEasingCurve.InOutQuart)
        
        self.float_sequence = QSequentialAnimationGroup()
        self.float_sequence.addAnimation(self.float_up)
        self.float_sequence.addAnimation(self.float_down)
        self.float_sequence.setLoopCount(-1)
        self.float_sequence.start()

        # Glow flicker animation - alternează între roz și cyan
        self.glow_anim1 = QPropertyAnimation(self.glow_effect, b"color")
        self.glow_anim1.setDuration(1500)
        self.glow_anim1.setStartValue(QColor("#E21ADB"))  # Pink
        self.glow_anim1.setEndValue(QColor("#00E0FF"))    # Cyan
        self.glow_anim1.setEasingCurve(QEasingCurve.InOutSine)
        
        self.glow_anim2 = QPropertyAnimation(self.glow_effect, b"color")
        self.glow_anim2.setDuration(1500)
        self.glow_anim2.setStartValue(QColor("#00E0FF"))  # Cyan
        self.glow_anim2.setEndValue(QColor("#E21ADB"))    # Pink
        self.glow_anim2.setEasingCurve(QEasingCurve.InOutSine)
        
        self.glow_sequence = QSequentialAnimationGroup()
        self.glow_sequence.addAnimation(self.glow_anim1)
        self.glow_sequence.addAnimation(self.glow_anim2)
        self.glow_sequence.setLoopCount(-1)
        self.glow_sequence.start()
        
        # Glow intensity flicker
        self.blur_anim1 = QPropertyAnimation(self.glow_effect, b"blurRadius")
        self.blur_anim1.setDuration(1000)
        self.blur_anim1.setStartValue(30)
        self.blur_anim1.setEndValue(50)
        self.blur_anim1.setEasingCurve(QEasingCurve.InOutQuad)
        
        self.blur_anim2 = QPropertyAnimation(self.glow_effect, b"blurRadius")
        self.blur_anim2.setDuration(1000)
        self.blur_anim2.setStartValue(50)
        self.blur_anim2.setEndValue(30)
        self.blur_anim2.setEasingCurve(QEasingCurve.InOutQuad)
        
        self.blur_sequence = QSequentialAnimationGroup()
        self.blur_sequence.addAnimation(self.blur_anim1)
        self.blur_sequence.addAnimation(self.blur_anim2)
        self.blur_sequence.setLoopCount(-1)
        self.blur_sequence.start()
