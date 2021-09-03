import os
import os
import sys

from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from lib.Globals import device_id
from windows.Main import MainWindow


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)


class LoginWindow(QMainWindow):
    def __init__(self, system_id):
        super().__init__()

        self.system_id = system_id

        self.window = uic.loadUi(resource_path('assets/ui/start.ui'), self)

        self.mainWindow = None

        self.window.setWindowIcon(QtGui.QIcon(resource_path('assets/logo.png')))
        self.window.setWindowTitle("Login")

        self.loginBtn = self.window.loginBtn
        self.loginLogo = self.window.loginLogo

        self.pixmap = QtGui.QPixmap(resource_path('assets/logo-light.png'))
        self.loginLogo.setPixmap(self.pixmap)

        self.loginBtn.setProperty('class', 'btn-fill-rounded')
        self.loginBtn.clicked.connect(self.login)

        self.window.show()

    def login(self):
        if self.system_id == device_id:
            self.mainWindow = MainWindow()
            self.window.close()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Application cannot be used for this device")
            msg.setWindowTitle("Authentication Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()