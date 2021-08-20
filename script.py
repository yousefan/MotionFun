import os
import sys

from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet

from windows.Login import LoginWindow
from windows.Main import MainWindow

if __name__ == '__main__':
    if 'MotionFun' not in os.listdir('C:/'):
        os.makedirs('C:/MotionFun')
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_cyan.xml')
    stylesheet = app.styleSheet()
    with open('assets/style.css') as file:
        app.setStyleSheet(stylesheet + file.read().format(**os.environ))

    window = MainWindow()
    app.exec()
