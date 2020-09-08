import pyautogui


class Control:
    x = 0

    def __init__(self, x):
        self.x = x

    def shoot(self, angle, power):
        pyautogui.moveTo(self.x, 200)
        pyautogui.dragTo(self.x - 80, 480, duration=0.5)


control = Control(200)

control.shoot(0, 100)
