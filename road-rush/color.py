import cv2
from PIL import ImageGrab
import numpy as np
from matplotlib import pyplot as plt

import win32gui

hwnd = win32gui.FindWindow(None, 'Road Rush - Google Chrome')

lower = [0, 0, 0]
upper = [255, 255, 255]


def capture():
    # Take screenshot
    window_rect = win32gui.GetWindowRect(hwnd)
    screenshot = ImageGrab.grab(window_rect)

    return screenshot

# def change_hue():


while (True):
    screenshot = np.array(capture())
    screenshot_rgb = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
    screenshot_hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)

    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    lower_yellow = np.array([0, 100, 100])
    upper_yellow = np.array([60, 100, 100])

    mask_yellow = cv2.inRange(screenshot_hsv, lower_yellow, upper_yellow)

    # res = cv2.bitwise_and(screenshot, screenshot, mask=mask)

    template = cv2.imread('templates/coll_coin.png', 0)
    w, h = template.shape[::-1]

    # res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    # threshold = 0.5
    # loc = np.where(res >= threshold)

    # for pt in zip(*loc[::-1]):
    #     cv2.rectangle(screenshot_gray, pt,
    #                   (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    cv2.imshow("Result", mask_yellow)
    cv2.createTrackbar("Hue", "Slider", 0, 255, )

    if (cv2.waitKey(5) == ord('q')):
        cv2.destroyAllWindows()
        break
