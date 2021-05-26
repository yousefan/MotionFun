from PySide6.QtWidgets import QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6 import QtGui
from PySide6.QtCore import QFile, QObject, QIODeviceBase


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_file = QFile("assets/ui/login.ui")
        ui_file.open(QIODeviceBase.ReadOnly)
        self.window = QUiLoader().load(ui_file)
        ui_file.close()

        self.window.setWindowIcon(QtGui.QIcon('assets/logo.png'))
        self.window.setWindowTitle("Login")
        self.window.loginBtn.setProperty('class', 'btn-fill-rounded')
        self.window.show()

