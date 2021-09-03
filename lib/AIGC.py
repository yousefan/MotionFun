import json
import math
import os
import time

from cryptography.fernet import Fernet as fer
from win32gui import GetWindowText, GetForegroundWindow

from lib.Actions import Actions
from lib.Globals import encryptionKey


class AIGC:
    def __init__(self):
        self.bodyMarks = {
            'NOSE': 0,
            'LEFT_EYE_INNER': 4,
            'LEFT_EYE': 5,
            'LEFT_EYE_OUTER': 6,
            'RIGHT_EYE_INNER': 1,
            'RIGHT_EYE': 2,
            'RIGHT_EYE_OUTER': 3,
            'LEFT_EAR': 8,
            'RIGHT_EAR': 7,
            'MOUTH_LEFT': 10,
            'MOUTH_RIGHT': 9,
            'LEFT_SHOULDER': 12,
            'RIGHT_SHOULDER': 11,
            'LEFT_ELBOW': 14,
            'RIGHT_ELBOW': 13,
            'LEFT_WRIST': 16,
            'RIGHT_WRIST': 15,
            'LEFT_PINKY': 18,
            'RIGHT_PINKY': 17,
            'LEFT_INDEX': 20,
            'RIGHT_INDEX': 19,
            'LEFT_THUMB': 22,
            'RIGHT_THUMB': 21,
            'LEFT_HIP': 24,
            'RIGHT_HIP': 23,
            'LEFT_KNEE': 26,
            'RIGHT_KNEE': 25,
            'LEFT_ANKLE': 28,
            'RIGHT_ANKLE': 27,
            'LEFT_HEEL': 30,
            'RIGHT_HEEL': 29,
            'LEFT_FOOT_INDEX': 32,
            'RIGHT_FOOT_INDEX': 31
        }
        self.handMarks = {
            'WRIST': 0,
            'THUMB_CMC': 1,
            'THUMB_MCP': 2,
            'THUMB_IP': 3,
            'THUMB_TIP': 4,
            'INDEX_FINGER_MCP': 5,
            'INDEX_FINGER_PIP': 6,
            'INDEX_FINGER_DIP': 7,
            'INDEX_FINGER_TIP': 8,
            'MIDDLE_FINGER_MCP': 9,
            'MIDDLE_FINGER_PIP': 10,
            'MIDDLE_FINGER_DIP': 11,
            'MIDDLE_FINGER_TIP': 12,
            'RING_FINGER_MCP': 13,
            'RING_FINGER_PIP': 14,
            'RING_FINGER_DIP': 15,
            'RING_FINGER_TIP': 16,
            'PINKY_MCP': 17,
            'PINKY_PIP': 18,
            'PINKY_DIP': 19,
            'PINKY_TIP': 20
        }
        self.marks = None
        self.commands = []
        self.prevTime = 0
        self.prevPose = []
        self.index = 0
        self.singlePressCount = 0
        self.action = None
        self.cipher = fer(encryptionKey)
        self.gameName = None
        self.prevProcTime = 0
        self.fps = 0

    def calculate_angle(self, point1, point2):
        delta_x = point1.x - point2.x
        delta_y = point1.y - point2.y
        theta = math.degrees(math.atan2(delta_y, delta_x))
        return theta

    def load_game_config(self, game):
        configAddress = 'C:/MotionFun/' + game + '.aigc'
        f = open(configAddress, "rb")
        decrypted_content = self.cipher.decrypt(f.read())
        gameConfig = json.loads(decrypted_content)
        gameConfig = gameConfig.get('game')
        self.gameName = gameConfig.get('name')
        self.commands = gameConfig.get('commands')
        poseType = gameConfig.get('PoseType')
        if poseType == "body":
            self.marks = self.bodyMarks
        elif poseType == "hand":
            self.marks = self.handMarks
        for command in self.commands:
            if command.get('command') == "FACTION":
                self.prevPose.append(0)
        self.action = Actions()
        self.action.count_single_press_actions(commands=self.commands)
        return poseType, self.gameName

    def control(self, landmarks):
        self.index = 0
        self.singlePressCount = 0

        if GetWindowText(GetForegroundWindow()) == self.gameName:
            for command in self.commands:
                c = command.get('command')
                if c == 'GT':
                    self.GT(command.get('points1')[0], command.get('points2')[0], command.get('axis'),
                            command.get('actions'), landmarks)
                elif c == 'FACTION':
                    self.FACTION(command.get('points')[0], command.get('velocity'), command.get('axis'),
                                 command.get('actions'), landmarks)
                    self.index += 1
                elif c == 'ANGLE':
                    self.ANGLE(command.get('points1')[0], command.get('points2')[0], command.get('threshold'),
                               command.get('actions'), landmarks)
                elif c == 'SIT':
                    pass
    
                elif c == 'MOUSE':
                    self.MOUSE(command.get('points')[0], command.get('actions'), landmarks)
    
                self.singlePressCount += 1

        self.fps = 1 / (time.time() - self.prevProcTime)
        self.prevProcTime = time.time()
        return int(self.fps)

    def get_available_games(self):
        gameConfigs = os.listdir('C:/MotionFun')
        games = []
        for gc in gameConfigs:
            if ".aigc" in gc:
                games.append(gc.replace(".aigc", ""))
        return games

    def GT(self, points1, points2, axis, actions, landmarks):
        p1 = landmarks[self.marks.get(points1)]
        p2 = landmarks[self.marks.get(points2)]
        if axis == 'x':
            if p1.x > p2.x:
                self.action.run(actions, self.singlePressCount)
            else:
                self.action.single_press_release(self.singlePressCount)
        elif axis == 'y':
            if p1.y > p2.y:
                self.action.run(actions, self.singlePressCount)
            else:
                self.action.single_press_release(self.singlePressCount)

    def FACTION(self, points, vel, axis, actions, landmarks):
        point = landmarks[self.marks.get(points)]
        dt = 0.05
        vel = float(vel)
        if axis == 'x':
            dx = point.x - self.prevPose[self.index]
            v = dx / dt
            if v < vel < 0:  # fast action left
                self.action.run(actions, self.singlePressCount)
            elif abs(v) < 0.1:
                self.action.single_press_release(self.singlePressCount)

            if v > vel > 0:  # fast action right
                self.action.run(actions, self.singlePressCount)
            elif abs(v) < 0.1:
                self.action.single_press_release(self.singlePressCount)

            self.prevPose[self.index] = point.x
            self.prevTime = time.time()
        elif axis == 'y':
            dy = point.y - self.prevPose[self.index]
            v = dy / dt
            if v < vel < 0:  # fast action up
                self.action.run(actions, self.singlePressCount)
            elif abs(v) < 0.1:
                self.action.single_press_release(self.singlePressCount)

            if v > vel > 0:  # fast action down
                self.action.run(actions, self.singlePressCount)
            elif abs(v) < 0.1:
                self.action.single_press_release(self.singlePressCount)
            self.prevPose[self.index] = point.y

    def ANGLE(self, points1, points2, threshold, actions, landmarks):
        p1 = landmarks[self.marks.get(points1)]
        p2 = landmarks[self.marks.get(points2)]
        theta = self.calculate_angle(p2, p1)
        # print(theta)
        if float(threshold[0]) < theta < float(threshold[1]):
            self.action.run(actions, self.singlePressCount)
        else:
            self.action.single_press_release(self.singlePressCount)

    def MOUSE(self, points, actions, landmarks):
        p = landmarks[self.marks.get(points)]
        self.action.run(actions, x=p.x, y=p.y)

    def SIT(self):
        pass
