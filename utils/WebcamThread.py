from PySide6.QtCore import QThread, Signal
import numpy as np
import mediapipe as mp
import cv2


class WebcamThread(QThread):
    change_pixmap_signal = Signal(np.ndarray)
    person_detection = Signal(bool)
    landmark_results = Signal(list)

    def __init__(self, webcam_id):
        super().__init__()
        self.run_flag = True
        self.y = 0
        self.speed = 40
        self.webcam_id = webcam_id
        self.pose = mp.solutions.pose

    def run(self):
        cap = cv2.VideoCapture(self.webcam_id)

        with self.pose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.5) as pose:
            while self.run_flag:
                ret, image = cap.read()

                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                results = pose.process(image)
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.pose_landmarks is None:
                    self.person_detection.emit(False)
                else:
                    self.person_detection.emit(True)
                    self.landmark_results.emit(results.pose_landmarks.landmark)

                self.draw_horizontal_line(image)
                self.change_pixmap_signal.emit(image)

            cap.release()

    def draw_horizontal_line(self, img):
        self.y = self.y + self.speed
        if self.y > 485:
            self.speed = self.speed * -1
        elif self.y < 1:
            self.speed = self.speed * -1
        cv2.line(img, (0, self.y), (650, self.y), (255, 208, 77), 5)

    def stop(self):
        self.run_flag = False
        self.wait()