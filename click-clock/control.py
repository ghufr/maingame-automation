import pyautogui


class Control:
    start_pos = (244, 835)

    debug = False

    def __init__(self, debug=False):
        self.debug = debug
        pyautogui.PAUSE = 0.07

    def start(self):
        if (not self.debug):
            pyautogui.click(self.start_pos)

    def click(self):
        if (not self.debug):
            pyautogui.click(self.start_pos)
