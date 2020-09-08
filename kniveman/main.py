import cv2
from PIL import ImageGrab
import numpy as np
from matplotlib import pyplot as plt


import win32gui

hwnd = win32gui.FindWindow(None, 'The Greatest Kniveman - Google Chrome')
toolbar_h = 200


def capture():
    # Take screenshot
    window_rect = win32gui.GetWindowRect(hwnd)

    w = window_rect[2] - window_rect[0]
    h = window_rect[3] - window_rect[1]

    crop_top = h * 0.4
    crop_bottom = h - (h * 0.4)
    crop_right = w - (w * 0.3)
    crop_left = w * 0.3

    screenshot = ImageGrab.grab(window_rect)
    screenshot = screenshot.crop(
        (crop_left, crop_top, crop_right, crop_bottom))

    return screenshot


while (True):
    screenshot = np.array(capture())
    screenshot_hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    template = cv2.imread('templates/obstacle.png', 0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)

    cv2.imshow("Screen", )

    if (cv2.waitKey(25) == ord('q')):
        cv2.destroyAllWindows()
        break
