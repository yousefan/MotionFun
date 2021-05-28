from PySide6.QtWidgets import QApplication
from qt_material import apply_stylesheet
from windows.Login import LoginWindow

import os
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_cyan.xml')
    stylesheet = app.styleSheet()
    with open('assets/style.css') as file:
        app.setStyleSheet(stylesheet + file.read().format(**os.environ))

    window = LoginWindow()
    app.exec()
