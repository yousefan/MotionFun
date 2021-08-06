import cv2
import mediapipe as mp
import numpy as np
from PySide6.QtCore import QThread, Signal


class WebcamThread(QThread):
    change_pixmap_signal = Signal(np.ndarray)
    detection = Signal(bool)
    landmark_results = Signal(list)

    def __init__(self, webcam_id, pose_type):
        super().__init__()
        self.run_flag = True
        self.y = 0
        self.speed = 40
        self.webcam_id = webcam_id
        self.bodyPose = mp.solutions.pose
        self.handPose = mp.solutions.hands
        self.pose_type = pose_type

    def run(self):
        cap = cv2.VideoCapture(self.webcam_id)

        if self.pose_type == "body":
            with self.bodyPose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.5) as pose:
                while self.run_flag:
                    ret, image = cap.read()
                    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                    image.flags.writeable = False
                    results = pose.process(image)
                    image.flags.writeable = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    if results.pose_landmarks is None:
                        self.detection.emit(False)
                    else:
                        self.detection.emit(True)
                        self.landmark_results.emit(results.pose_landmarks.landmark)

                    self.draw_horizontal_line(image)
                    self.change_pixmap_signal.emit(image)

                cap.release()

        elif self.pose_type == "hand":
            with self.handPose.Hands(min_detection_confidence=0.6, min_tracking_confidence=0.5,
                                     max_num_hands=1) as pose:
                while self.run_flag:
                    ret, image = cap.read()
                    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                    image.flags.writeable = False
                    results = pose.process(image)
                    image.flags.writeable = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    if results.multi_hand_landmarks is None:
                        self.detection.emit(False)
                    else:
                        self.detection.emit(True)
                        for hand_landmark in results.multi_hand_landmarks:
                            self.landmark_results.emit(hand_landmark.landmark)

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
