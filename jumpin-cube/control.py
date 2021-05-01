import pyautogui


class Control:
    short_pos = (94, 874)
    long_pos = (394, 874)
    start_pos = (251, 816)

    debug = False

    def __init__(self, debug=False):
        self.debug = debug

    def start(self):
        pyautogui.click(self.start_pos)

    def long(self):
        if not self.debug:
            pyautogui.click(self.long_pos)
        else:
            print("Long")

    def short(self):
        if not self.debug:
            pyautogui.click(self.short_pos)
        else:
            print("Short")
