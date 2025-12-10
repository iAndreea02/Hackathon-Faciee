from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from PySide6.QtGui import QPainter, QLinearGradient, QColor, QPixmap
import sys


class StartPage(QWidget):
    def __init__(self):
        super().__init__()

        # Culori background
        self.bgStart = QColor("#0A0E1A")
        self.bgEnd = QColor("#001F30")

        self.setMinimumSize(480, 800)

        self._build_ui()
        self._animate_robot()

    def _build_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        # ---------- TITLU ----------
        self.title = QLabel("Hello, viitor student!")
        self.title.setStyleSheet("font-size:32px; font-weight:bold; color:#E21ADB;")
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)

        # ---------- SUBTITLU ----------
        self.subtitle = QLabel("Facultatea ACIEE te așteaptă!")
        self.subtitle.setStyleSheet("font-size:16px; color:#00E0FF;")
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.subtitle)

        # ---------- SPAȚIU ----------
        self.layout.addSpacing(40)

        # ---------- ROBOT ----------
        self.robot = QLabel(self)
        self.robot.setPixmap(QPixmap("robo.png").scaled(230, 230, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.robot.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.robot)

        # ---------- SPAȚIU ----------
        self.layout.addSpacing(40)

        # ---------- BUTON ----------
        self.button = QPushButton("Intră în aplicație")
        self.button.setStyleSheet("""
            QPushButton {
                background:#E21ADB;
                color:white;
                font-size:22px;
                font-weight:bold;
                padding:12px;
                border-radius:10px;
            }
            QPushButton:hover {
                background:#f545e6;
            }
        """)
        self.layout.addWidget(self.button)

        self.layout.addStretch()

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, self.bgStart)
        gradient.setColorAt(1, self.bgEnd)
        painter.fillRect(self.rect(), gradient)

    def _animate_robot(self):
        # animație foarte light → nu generează lag pe Raspberry
        start_rect = self.robot.geometry()
        end_rect = QRect(start_rect.x(), start_rect.y() + 20, start_rect.width(), start_rect.height())

        self.anim = QPropertyAnimation(self.robot, b"geometry")
        self.anim.setDuration(3000)
        self.anim.setStartValue(start_rect)
        self.anim.setEndValue(end_rect)
        self.anim.setEasingCurve(QEasingCurve.InOutSine)
        self.anim.setLoopCount(-1)
        self.anim.start()

