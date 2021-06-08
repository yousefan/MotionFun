import math
import os
import time
from playsound import playsound
from win32gui import GetWindowText, GetForegroundWindow
import pyautogui
import pydirectinput
import threading


class AIGC:
    def __init__(self):
        self.marks = {
            'NOSE': 0,
            'LEFT_EYE_INNER': 1,
            'LEFT_EYE': 2,
            'LEFT_EYE_OUTER': 3,
            'RIGHT_EYE_INNER': 4,
            'RIGHT_EYE': 5,
            'RIGHT_EYE_OUTER': 6,
            'LEFT_EAR': 7,
            'RIGHT_EAR': 8,
            'MOUTH_LEFT': 9,
            'MOUTH_RIGHT': 10,
            'LEFT_SHOULDER': 11,
            'RIGHT_SHOULDER': 12,
            'LEFT_ELBOW': 13,
            'RIGHT_ELBOW': 14,
            'LEFT_WRIST': 15,
            'RIGHT_WRIST': 16,
            'LEFT_PINKY': 17,
            'RIGHT_PINKY': 18,
            'LEFT_INDEX': 19,
            'RIGHT_INDEX': 20,
            'LEFT_THUMB': 21,
            'RIGHT_THUMB': 22,
            'LEFT_HIP': 23,
            'RIGHT_HIP': 24,
            'LEFT_KNEE': 25,
            'RIGHT_KNEE': 26,
            'LEFT_ANKLE': 27,
            'RIGHT_ANKLE': 28,
            'LEFT_HEEL': 29,
            'RIGHT_HEEL': 30,
            'LEFT_FOOT_INDEX': 31,
            'RIGHT_FOOT_INDEX': 32
        }

    @staticmethod
    def calculate_angle(point1, point2):
        delta_x = point1.x - point2.x
        delta_y = point1.y - point2.y
        theta = math.degrees(math.atan2(delta_y, delta_x))
        return theta

    def load_game_config(self,game):
        pass

    def control(self, landmarks):
        pass

    def get_available_games(self):
        gameConfigs = os.listdir('C:/AIGC')
        games = []
        for gc in gameConfigs:
            if ".aigc" in gc:
                games.append(gc.replace(".aigc",""))
        return games

    def GT(self):
        pass

    def FACTION(self):
        pass

    def ANGLE(self):
        pass

    def SIT(self):
        pass