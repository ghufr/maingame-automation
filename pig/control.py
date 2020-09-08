import pyautogui
import time


class Control:
    def jump(self):
        print('Jump')
        pyautogui.mouseDown(200, 200)
        time.sleep(0.38)
        pyautogui.mouseUp()


i = 0
limit = 320
control = Control()

while (i < limit):
    control.jump()
    time.sleep(0.5)
    i += 1
    print(i, end=":")
