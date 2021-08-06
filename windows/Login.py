import requests
from PySide6 import QtGui
from PySide6.QtCore import QFile, QIODeviceBase
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow, QMessageBox

from windows.Main import MainWindow


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_file = QFile("assets/ui/login.ui")
        ui_file.open(QIODeviceBase.ReadOnly)
        self.window = QUiLoader().load(ui_file)
        ui_file.close()

        self.mainWindow = None
        self.loginApi = 'http://aigc.yousefan.ir/api/login.php'

        self.window.setWindowIcon(QtGui.QIcon('assets/logo.png'))
        self.window.setWindowTitle("Login")

        self.loginBtn = self.window.loginBtn
        self.usernameField = self.window.usernameField
        self.passwordField = self.window.passwordField
        self.loginLogo = self.window.loginLogo

        self.pixmap = QtGui.QPixmap('assets/logo-light.png')
        self.loginLogo.setPixmap(self.pixmap)

        self.loginBtn.setProperty('class', 'btn-fill-rounded')
        self.loginBtn.clicked.connect(self.login)

        self.window.show()

    def login(self):
        username = self.usernameField.text()
        password = self.passwordField.text()
        data = {
            'username': username,
            'password': password
        }
        res = requests.post(self.loginApi, data=data)
        if res.text == 'ok':
            self.mainWindow = MainWindow()
            self.window = None
        elif res.text == 'error':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Wrong password or username")
            msg.setWindowTitle("Login Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
