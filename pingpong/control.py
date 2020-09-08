import pyautogui
import time


class Control:
    def jump(self):
        print('Jump')
        pyautogui.mouseDown(200, 600)
        time.sleep(0.145)
        pyautogui.mouseUp()


i = 0
limit = 10
control = Control()

pyautogui.click(200, 600)
time.sleep(0.5)

while (i < limit):
    control.jump()
    time.sleep(0.85)
    i += 1
    print(i, end=":")
