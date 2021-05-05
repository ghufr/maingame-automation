import pyautogui

pos = {
    "r": (416, 935),
    "c": (248, 935),
    "l": (83, 935)
}


class Control:
    left_pos = (83, 935)
    center_pos = (248, 935)
    right_pos = (416, 935)

    debug = False

    def __init__(self, debug=False):
        self.debug = debug

    def click(self, res):
        if (not self.debug):
            pyautogui.click(pos[res])

    # def left(self):
    #     if (not self.debug):
    #         pyautogui.click(self.left_pos)

    # def right(self):
    #     if (not self.debug):
    #         pyautogui.click(self.right_pos)

    # def center(self):
    #     if (not self.debug):
    #         pyautogui.click(self.center_pos)
