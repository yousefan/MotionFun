import pyautogui
import pydirectinput
import threading


class Actions:

    def __init__(self):
        self.SINGLE_PRESS = "sp"
        self.MULTI_PRESS = "mp"
        self.FACTOR_PRESS = "fp"
        self.K2 = "k2"
        self.once = []
        self.currentSp = -1

    def count_single_press_actions(self, commands):
        for command in commands:
            actions = command.get('actions')
            for action in actions:
                act, _ = action.split(".")[0], action.split(".")[1]
                if act == self.SINGLE_PRESS:
                    self.once.append(False)

    def run(self, actions):
        for action in actions:
            act, key = action.split(".")[0], action.split(".")[1]
            if act == self.SINGLE_PRESS:
                self.currentSp += 1
                threading.Thread(target=self.single_press, args=(key,)).start()

            elif act == self.MULTI_PRESS:
                threading.Thread(target=self.multi_press, args=(key,)).start()
            elif act == self.FACTOR_PRESS:
                key, factor = key.split("@")[0], key.split("@")[1]
                threading.Thread(target=self.factor_press, args=(key, factor,)).start()
            elif act == self.K2:
                pass

    def single_press_release(self):
        if len(self.once) > 0:
            self.once[self.currentSp] = False

    def single_press(self, key):
        if not self.once[self.currentSp]:
            # pydirectinput.press(key)
            print("single press: "+key)
            self.once[self.currentSp] = True

    def multi_press(self, key):
        # pydirectinput.press(key)
        print("multi press: "+key)

    def factor_press(self, key, factor):
        pass

    def keydown_keyup(self, key):
        pass
