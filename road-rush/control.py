# from pynput.mouse import Button, Controller

import win32api
import win32con
import pyautogui

import time

# mouse = Controller()


class Control:
    x = 0
    y = 0
    debug = False

    def __init__(self, w, h, debug=False):
        self.x = int(w / 2)
        self.y = int(h / 2)
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0.01
        self.debug = debug

        # pyautogui.mouseInfo()

        # pyautogui.moveTo(self.x, self.y)
        # win32api.SetCursorPos((self.x, self.y))
        # win32api.mouse_event(win32con.MOUSEEVENTF_MOVE |
        #                      win32con.MOUSEEVENTF_ABSOLUTE, self.x, self.y)

    def swipe(self, dis):

        # win32api.SetCursorPos((self.x, self.y))

        # win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, dis * -1, 0)
        # time.sleep(0.05)

        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,
        #                      self.x, self.y, 0, 0)
        # time.sleep(0.05)
        # win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, dis, 0)
        # pyautogui.dragTo(self.x + dis, self.y, 0.19,
        #                  button='left')
        # pyautogui.mouseDown(self.x, self.y)
        # pyautogui.moveRel(dis)
        # pyautogui.mouseUp(self.x, self.y)
        # pyautogui.mouseDown(self.x, self.y)
        # pyautogui.moveTo(dis + self.x, self.y, 0)
        # pyautogui.moveTo(self.x + dis, self.y, duration=0.1)
        # pyautogui.mouseUp(self.x + dis, self.y)
        # print('Move to: ', self.x - dis)
        # pyautogui.dragRel(self.x - dis, self.y)
        if not self.debug:
            pyautogui.moveTo(self.x, self.y, duration=0)
            pyautogui.dragRel(dis, 0, button='left', duration=0.101)

        # time.sleep(0.01)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,
        #                      self.x, self.y, 0, 0)
        # mouse.position = (self.x, self.y)
        # mouse.press(Button.left)
        # mouse.move(dis, 0)
        # mouse.release(Button.left)

    def turn_left(self):
        print('TURN LEFT')
        self.swipe(-80)

    def turn_right(self):
        print('TURN RIGHT')
        self.swipe(80)

    def turn(self, move):
        if move == 'L':
            self.turn_left()
        elif move == 'R':
            self.turn_right()


# control = Control(500, 1000)
# # control.turn_left()


# for i in range(0, 5):
#     control.turn_left()
#     time.sleep(0.5)
#     control.turn_right()
#     time.sleep(0.5)
