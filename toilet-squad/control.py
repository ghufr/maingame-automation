import pyautogui


class Control:
    debug = False

    def __init__(self, debug=False):
        self.debug = debug
        # pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0.1

    def left(self):
        print('Save')
        if not self.debug:
            pyautogui.click(99, 820, duration=0.1)

    def right(self):
        print('Kill')

        if not self.debug:
            pyautogui.click(386, 820, duration=0.1)

    def center(self):
        # print('Ram')

        if not self.debug:
            pyautogui.click(239, 820)
