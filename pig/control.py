import pyautogui
import time


class Control:
    def jump(self, i):
        print('Jump', i)
        pyautogui.mouseDown(210, 612)
        a = min(i * 0.0003, 0.03)
        time.sleep(0.35 + a)
        pyautogui.mouseUp()


i = 0
limit = 622
control = Control()

while (i < limit):
    control.jump(i)
    time.sleep(0.6)
    i += 1
    print(i, end=":")
