import pyautogui


class Control:
    start_pos = (244, 835)

    debug = False

    def __init__(self, debug=False):
        self.debug = debug
        pyautogui.PAUSE = 0.09

    def start(self):
        if (not self.debug):
            pyautogui.click(self.start_pos)

    def add(self, clicks):
        if (not self.debug):
            print(clicks)
            pyautogui.click(self.start_pos, clicks=clicks,
                            interval=0.08, duration=0.08)

    def down(self):
        if (not self.debug):
            pyautogui.mouseDown(_pause=False)

    def up(self):
        if (not self.debug):
            pyautogui.mouseUp(_pause=False, duration=0.0)
