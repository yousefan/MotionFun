import os
import sys

from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet

from windows.Main import MainWindow
from windows.Login import LoginWindow

# pyinstaller script.spec --hidden-import qt_material --hidden-import PyQt5

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)


if __name__ == '__main__':
    if 'MotionFun' not in os.listdir('C:/'):
        os.makedirs('C:/MotionFun')
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_cyan.xml')
    stylesheet = app.styleSheet()
    with open(resource_path('assets/style.css')) as file:
        app.setStyleSheet(stylesheet + file.read().format(**os.environ))

    window = LoginWindow()
    app.exec()
