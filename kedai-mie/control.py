import pyautogui


positions = {
    'Bakso': (120, 706),
    'Sawi': (209, 706),
    'Telur': (296, 706),
    'Udang': (120, 636),
    'Kornet': (209, 636),
    'Sosis': (296, 636)
}

positions_addon = {
    'Esteh': (51, 634),
    'Esjeruk': (51, 699),
    'Bakwan': (390, 554),
    'Tempe': (451, 554),
    'Tahu': (335, 554)
}


class Control:
    debug = False

    def __init__(self, debug=False):
        self.debug = debug

    def serve(self):
        if not self.debug:
            pyautogui.click(240, 811, duration=0.08)

    def pick_plate(self, plate):
        if not self.debug:
            # 0 = Mangkok
            # 1 = Bungkus
            if (plate == 0):
                pyautogui.click(321, 936)
            else:
                pyautogui.click(433, 936)

    def pick_noodle(self):
        if not self.debug:
            pyautogui.click(419, 631, duration=0.105)

    def pick_toppings(self, toppings):
        if not self.debug:
            for top in toppings:
                pyautogui.click(positions[top], duration=0.08)

    def pick_addons(self, additionals):
        if not self.debug:
            for add in additionals:
                pyautogui.click(positions_addon[add], duration=0.08)

    def trash(self):
        if not self.debug:
            pyautogui.click(86, 954, duration=0.08)

    def play_again(self):
        if not self.debug:
            pyautogui.click(243, 611)

    def play(self):
        if not self.debug:
            pyautogui.click(335, 996)

    def start(self):
        if not self.debug:
            pyautogui.click(248, 807)
