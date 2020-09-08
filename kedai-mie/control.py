import pyautogui


positions = {
    'Bakso': (120, 692),
    'Sawi': (209, 692),
    'Telur': (296, 692),
    'Udang': (120, 621),
    'Kornet': (209, 621),
    'Sosis': (296, 621)
}

positions_addon = {
    'Esteh': (46, 622),
    'Esjeruk': (46, 689),
    'Bakwan': (405, 534),
    'Tempe': (459, 534),
    'Tahu': (338, 534)
}


class Control:
    debug = False

    def __init__(self, debug=False):
        self.debug = debug

    def serve(self):
        if not self.debug:
            pyautogui.click(240, 811, duration=0.01)

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
            pyautogui.click(419, 631, duration=0.101)

    def pick_toppings(self, toppings):
        if not self.debug:
            for top in toppings:
                pyautogui.click(positions[top], duration=0.06)

    def pick_addons(self, additionals):
        if not self.debug:
            for add in additionals:
                pyautogui.click(positions_addon[add], duration=0.01)

    def trash(self):
        if not self.debug:
            pyautogui.click(86, 954, duration=0.1)
