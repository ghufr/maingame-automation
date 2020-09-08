import pyautogui

positions = {
    'meses': (43, 847),
    'kacang': (122, 847),
    'keju': (205, 847),
    'matcha': (287, 847),
    'oreo': (368, 847),
    'strawberry': (449, 847),
    'nuttella': (36, 654),
    'skacang': (36, 748),
}


class Control:
    debug = False

    def __init__(self, debug=False):
        self.debug = debug

    def pick_topping(self, top):
        if not self.debug:
            # print(top, end=" ")
            pyautogui.click(positions[top], duration=0.01, clicks=2)

    def serve(self):
        if not self.debug:
            pyautogui.click(440, 968)

    def butter(self):
        if not self.debug:
            pyautogui.click(460, 628)

    def trash(self):
        if not self.debug:
            pyautogui.click(63, 974)
    def start(self):
        if not self.debug:
            pyautogui.click(250, 813)
