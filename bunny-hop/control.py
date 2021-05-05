import pyautogui


class Control:
    left_pos = (100, 900)
    right_pos = (350, 900)
    debug = False

    def __init__(self, debug=False):
        self.debug = debug
        pyautogui.PAUSE = 0.09

    def start(self):
        if (not self.debug):
            pyautogui.click(250, 820)

    def left(self):
        if (not self.debug):
            pyautogui.click(self.left_pos)

    def right(self):
        if (not self.debug):
            pyautogui.click(self.right_pos)
