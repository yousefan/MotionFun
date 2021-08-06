import cv2
import numpy as np
from PySide6 import QtGui
from PySide6.QtCore import Slot, Qt, QFile, QIODeviceBase
from PySide6.QtGui import QPixmap
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow, QMessageBox

from utils.AIGC import AIGC
from utils.LoadWebcamDevices import LoadWebcamDevices
from utils.WebcamThread import WebcamThread


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ui_file = QFile("assets/ui/main.ui")
        ui_file.open(QIODeviceBase.ReadOnly)
        self.window = QUiLoader().load(ui_file)
        ui_file.close()

        self.window.setWindowIcon(QtGui.QIcon('assets/logo.png'))
        self.window.setWindowTitle("AIGC")

        self.startBtn = self.window.startBtn
        self.startBtn.setProperty('class', 'btn-fill-rounded')
        self.gameSelection = self.window.gameSelection
        self.webcamSelection = self.window.webcamSelection
        self.selectedGameLabel = self.window.selectedGameLabel
        self.fpsLabel = self.window.fpsLabel
        self.statusLabel = self.window.statusLabel
        self.imageLabel = self.window.imageLabel

        self.window.show()

        self.width = 200
        self.height = 120
        self.started = False
        self.thread = None
        self.loadWebcamsThread = None
        self.aigc = AIGC()

        self.load_webcam_devices()
        self.load_games()
        self.startBtn.clicked.connect(self.start)

    def start(self):
        if self.webcamSelection.currentText() == '':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("No webcam selected")
            msg.setWindowTitle("Webcam Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
        else:
            if not self.started:
                webcam_id = int(self.webcamSelection.currentText().replace("webcam ", ""))
                selectedGame = self.gameSelection.currentText()
                poseType, gameName = self.aigc.load_game_config(selectedGame)
                self.thread = WebcamThread(webcam_id, poseType)
                self.thread.change_pixmap_signal.connect(self.update_image)
                self.thread.detection.connect(self.detection)
                self.thread.landmark_results.connect(self.landmarks)
                self.thread.start()
                self.started = True
                self.startBtn.setText("Stop")
                self.statusLabel.setStyleSheet("color: rgb(85, 170, 127);")
                self.statusLabel.setText("Running")
                self.selectedGameLabel.setText(gameName)
            else:
                self.thread.stop()
                self.started = False
                self.startBtn.setText("Start")
                self.statusLabel.setStyleSheet("color: rgb(255, 85, 127);")
                self.statusLabel.setText("Stopped")

    def load_games(self):
        games = self.aigc.get_available_games()
        for g in games:
            self.gameSelection.addItem(g)

    def load_webcam_devices(self):
        self.startBtn.setText("Loading...")
        self.startBtn.setEnabled(False)
        self.webcamSelection.clear()
        self.loadWebcamsThread = LoadWebcamDevices()
        self.loadWebcamsThread.devices.connect(self.on_loaded_webcams)
        self.loadWebcamsThread.start()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @Slot(list)
    def landmarks(self, landmarks):
        fps = self.aigc.control(landmarks=landmarks)
        self.fpsLabel.setText(str(fps))

    @Slot(list)
    def on_loaded_webcams(self, webcams):
        self.startBtn.setEnabled(True)
        self.startBtn.setText("Start")
        for webcam in webcams:
            self.webcamSelection.addItem("webcam " + str(webcam))

    @Slot(np.ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.imageLabel.setPixmap(qt_img)

    @Slot(bool)
    def detection(self, detected):
        pass

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.width, self.height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)