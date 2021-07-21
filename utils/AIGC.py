import math
import os
import time
from playsound import playsound
from win32gui import GetWindowText, GetForegroundWindow
from utils.Actions import Actions


class AIGC:
    def __init__(self):
        self.marks = {
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
        self.commands = []
        self.prevTime = 0
        self.prevPose = []
        self.index = 0
        self.singlePressCount = 0
        self.action = None

    def calculate_angle(self, point1, point2):
        delta_x = point1.x - point2.x
        delta_y = point1.y - point2.y
        theta = math.degrees(math.atan2(delta_y, delta_x))
        return theta

    def load_game_config(self, game):
        configAddress = 'C:/AIGC/' + game + '.aigc'
        f = open(configAddress, "r")
        lines = f.read().split('\n')
        self.commands = []
        for line in lines:
            split = line.split(',')
            command = split[0]
            if command == 'GT':
                points1 = [p for p in split[1].replace("[", "").replace("]", "").split("|")]
                points2 = [p for p in split[2].replace("[", "").replace("]", "").split("|")]
                axis = split[3].replace("[", "").replace("]", "")
                actions = [p for p in split[4].replace("[", "").replace("]", "").split("|")]
                self.commands.append(
                    {'command': command, 'points1': points1, 'points2': points2, 'axis': axis, 'actions': actions})
            elif command == 'FACTION':
                points = [p for p in split[1].replace("[", "").replace("]", "").split("|")]
                velocity = split[2].replace("[", "").replace("]", "")
                axis = split[3].replace("[", "").replace("]", "")
                actions = [p for p in split[4].replace("[", "").replace("]", "").split("|")]
                self.prevPose.append(0)
                self.commands.append(
                    {'command': command, 'points': points, 'velocity': velocity, 'axis': axis, 'actions': actions})
            elif command == 'ANGLE':
                points1 = [p for p in split[1].replace("[", "").replace("]", "").split("|")]
                points2 = [p for p in split[2].replace("[", "").replace("]", "").split("|")]
                threshold = [p for p in split[3].replace("[", "").replace("]", "").split("|")]
                actions = [p for p in split[4].replace("[", "").replace("]", "").split("|")]
                self.commands.append(
                    {'command': command, 'points1': points1, 'points2': points2, 'threshold': threshold,
                     'actions': actions})
            elif command == 'SIT':
                actions = [p for p in split[1].replace("[", "").replace("]", "").split("|")]
                self.commands.append({'command': command, 'actions': actions})
        self.action = Actions()
        self.action.count_single_press_actions(commands=self.commands)
        print(self.commands)

    def control(self, landmarks):
        self.index = 0
        self.singlePressCount = 0
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
            self.singlePressCount += 1

    def get_available_games(self):
        gameConfigs = os.listdir('C:/AIGC')
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

    def SIT(self):
        pass
