from PySide6.QtWidgets import QApplication
from start_page import StartPage
import sys

app = QApplication(sys.argv)
page = StartPage()
page.show()
sys.exit(app.exec())
