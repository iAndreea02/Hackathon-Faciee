from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QGraphicsOpacityEffect, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QSequentialAnimationGroup, QPoint
from PyQt5.QtGui import QPainter, QLinearGradient, QColor, QPixmap
import sys
from start_page import StartPage
import sys


app = QApplication(sys.argv)
win = StartPage()
win.show()
sys.exit(app.exec_())
