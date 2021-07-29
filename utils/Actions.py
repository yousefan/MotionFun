import pyautogui
import pydirectinput
import threading


class Actions:

    def __init__(self):
        self.SINGLE_PRESS = "sp"
        self.MULTI_PRESS = "mp"
        self.FACTOR_PRESS = "fp"
        self.KEY_UP = "ku"
        self.KEY_DOWN = "kd"
        self.K2 = "k2"
        self.DRAG = "drag"
        self.once = []
        self.currentSp = -1

        self.screenSize = pyautogui.size()
        print(self.screenSize)

    def count_single_press_actions(self, commands):
        for command in commands:
            actions = command.get('actions')
            if actions is not None:
                for action in actions:
                    act = action.get('action')
                    if act == self.SINGLE_PRESS:
                        self.once.append(False)
            else:
                self.once = []

    def run_on_keyboard(self, actions, spc):  # spc => single press count
        for action in actions:
            act, key = action.get('action'), action.get('key')
            if act == self.SINGLE_PRESS:
                threading.Thread(target=self.single_press, args=(key, spc,)).start()
            elif act == self.MULTI_PRESS:
                threading.Thread(target=self.multi_press, args=(key,)).start()
            elif act == self.KEY_UP:
                threading.Thread(target=self.key_up, args=(key,)).start()
            elif act == self.KEY_DOWN:
                threading.Thread(target=self.key_down, args=(key,)).start()
            elif act == self.FACTOR_PRESS:
                factor = action.get('factor')
                threading.Thread(target=self.factor_press, args=(key, factor,)).start()
            elif act == self.K2:
                pass

    def run_on_mouse(self, actions, x, y):
        for action in actions:
            act, key = action.get('action'), action.get('key')
            if act == self.DRAG:
                threading.Thread(target=self.mouse_drag, args=(key, x, y,)).start()

    def single_press_release(self, spc):
        if len(self.once) > 0:
            self.once[spc] = False

    def single_press(self, key, spc):
        if not self.once[spc]:
            self.once[spc] = True
            pydirectinput.press(key)

    def multi_press(self, key):
        pydirectinput.press(key)

    def factor_press(self, key, factor):
        pydirectinput.press(key, presses=factor)

    def key_up(self, key):
        pydirectinput.keyUp(key)

    def key_down(self, key):
        pydirectinput.keyDown(key)

    def mouse_drag(self, key, x, y):
        pydirectinput.mouseDown(button=key)
        pydirectinput.moveTo(x=int(x * self.screenSize.width), y=int(y * self.screenSize.height))