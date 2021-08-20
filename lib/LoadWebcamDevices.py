import cv2
from PyQt5.QtCore import QThread, pyqtSignal


class LoadWebcamDevices(QThread):
    devices = pyqtSignal(list)

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
