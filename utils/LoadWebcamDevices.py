from PySide6.QtCore import QThread, Signal
import cv2


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
