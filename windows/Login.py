import requests
from getmac import get_mac_address
from lib.Globals import macAddress
from PySide6 import QtGui
from PySide6.QtCore import QFile, QIODeviceBase
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow, QMessageBox

from windows.Main import MainWindow


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_file = QFile("assets/ui/start.ui")
        ui_file.open(QIODeviceBase.ReadOnly)
        self.window = QUiLoader().load(ui_file)
        ui_file.close()

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