from getmac import get_mac_address
import os
import sys

from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QMainWindow
from getmac import get_mac_address

from windows.Main import MainWindow


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window = uic.loadUi(resource_path('assets/ui/start.ui'), self)

        self.mainWindow = None

        self.window.setWindowIcon(QtGui.QIcon('assets/logo.png'))
        self.window.setWindowTitle("Login")

        self.loginBtn = self.window.loginBtn
        self.loginLogo = self.window.loginLogo

        self.pixmap = QtGui.QPixmap('assets/logo-light.png')
        self.loginLogo.setPixmap(self.pixmap)

        self.loginBtn.setProperty('class', 'btn-fill-rounded')
        self.loginBtn.clicked.connect(self.login)

        self.systemMacAddress = get_mac_address()

        self.window.show()

    def login(self):

        if self.systemMacAddress == macAddress:
            self.mainWindow = MainWindow()
            self.window = None
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Application cannot be used for this computer")
            msg.setWindowTitle("Authentication Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()