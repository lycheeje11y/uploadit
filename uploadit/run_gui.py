from PyQt5.QtWidgets import QApplication
from app import MainWindow

import sys

def gui_app():
    gui_app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return gui_app.exec()