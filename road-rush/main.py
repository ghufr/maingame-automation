import cv2
from PIL import ImageGrab
import numpy as np
from matplotlib import pyplot as plt

import win32gui

hwnd = win32gui.FindWindow(None, 'Road Rush')


while (True):
    window_rect = win32gui.GetWindowRect(hwnd)

    window_w = window_rect[2] - window_rect[0]
    window_h = window_rect[3] - window_rect[1]

    screenshot_raw = ImageGrab.grab(window_rect)
    screenshot = np.array(screenshot_raw)
    screenshot_rgb = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
    screenshot_hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)

    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # lower_yellow = np.array([20, 100, 0])
    # upper_yellow = np.array([100, 255, 255])

    # mask = cv2.inRange(screenshot_hsv, lower_yellow, upper_yellow)
    # res = cv2.bitwise_and(screenshot, screenshot, mask=mask)

    template_player = cv2.imread('templates/player2.png', 0)

    # screenshot_bottom = screenshot_raw.crop(
    #     [50, window_h * 0.5, window_w - 20, window_h - (window_h * 0.1)])
    # screenshot_bottom = cv2.cvtColor(
    #     np.array(screenshot_bottom), cv2.COLOR_BGR2GRAY)

    screenshot_tresh = cv2.threshold(
        screenshot_gray, 127, 255, cv2.THRESH_BINARY)[1]

    # player = cv2.matchTemplate(
    #     screenshot_tresh, template_player, cv2.TM_CCOEFF_NORMED)

    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 15))
    detected_lines = cv2.morphologyEx(
        screenshot_tresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)

    cnts = cv2.findContours(
        detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    # for c in cnts:
    #     cv2.drawContours(screenshot_tresh, [c], -1, (0, 0, 0), 2)

    # cv2.imshow("Player", player)
    # cv2.rectangle(screenshot_tresh, ((window_w / 2) - 200, 10),
    #               (window_w - 200, 50), (0, 0, 0), -1)
    cv2.imshow("Grayscale", screenshot_tresh)

    if (cv2.waitKey(5) == ord('q')):
        cv2.destroyAllWindows()
        break
