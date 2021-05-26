from PySide6 import QtGui
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QThread, Signal, Slot, Qt, QFile, QObject, QIODeviceBase
import numpy as np
import mediapipe as mp
import cv2


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
        self.detectionLabel = self.window.detectionLabel
        self.statusLabel = self.window.statusLabel
        self.imageLabel = self.window.imageLabel

        self.window.show()

        self.width = 200
        self.height = 120
        self.started = False
        self.thread = None
        self.loadWebcamsThread = None

        self.load_webcam_devices()
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
                self.thread = WebcamThread(webcam_id)
                self.thread.change_pixmap_signal.connect(self.update_image)
                self.thread.start()
                self.started = True
                self.startBtn.setText("Stop")
                self.statusLabel.setStyleSheet("color: rgb(85, 170, 127);")
                self.statusLabel.setText("Running")
            else:
                self.thread.stop()
                self.started = False
                self.startBtn.setText("Start")
                self.statusLabel.setStyleSheet("color: rgb(255, 85, 127);")
                self.statusLabel.setText("Stopped")

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
    def on_loaded_webcams(self, webcams):
        self.startBtn.setEnabled(True)
        self.startBtn.setText("Start")
        for webcam in webcams:
            self.webcamSelection.addItem("webcam " + str(webcam))

    @Slot(np.ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.imageLabel.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.width, self.height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


class LoadWebcamDevices(QThread):
    devices = Signal(list)

    def __init__(self):
        super().__init__()

    def run(self):
        webcams = []
        index = 0
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.read()[0]:
                break
            else:
                webcams.append(index)
            cap.release()
            index += 1
        self.devices.emit(webcams)


class WebcamThread(QThread):
    change_pixmap_signal = Signal(np.ndarray)

    def __init__(self, webcam_id):
        super().__init__()
        self.run_flag = True
        self.y = 0
        self.speed = 40
        self.webcam_id = webcam_id

    def run(self):
        cap = cv2.VideoCapture(self.webcam_id)
        while self.run_flag:
            ret, cv_img = cap.read()
            self.y = self.y + self.speed
            if self.y > 485:
                self.speed = self.speed * -1
            elif self.y < 1:
                self.speed = self.speed * -1
            cv2.line(cv_img, (0, self.y), (650, self.y), (255, 208, 77), 5)

            if ret:
                self.change_pixmap_signal.emit(cv_img)
            # shut down capture system
        cap.release()

    def stop(self):
        self.run_flag = False
        self.wait()
