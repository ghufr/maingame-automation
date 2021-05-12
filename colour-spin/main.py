import cv2
import math
import time
import os
import shutil

from wincap import WinCap
from control import Control
from identifier import Identifier

# Platformnya Game Nasional
wincap = WinCap('Colour Spin - Google Chrome')
# test = wincap.get_screenshot()
# wincap.save_screenshot('output/test.png')
control = Control(debug=False)

control.start()

red = [(138, 113, 0), (180, 255, 255)]
yellow = [(0, 113, 0), (36, 255, 255)]
green = [(38, 113, 0), (81, 255, 255)]
blue = [(90, 113, 0), (107, 255, 255)]

colors = [
    {
        "name": "yellow",
        "color": (0, 255, 255),
        "filter": [(0, 113, 0), (36, 255, 255)]
    },
    {
        "name": "red",
        "color": (0, 0, 255),
        "filter": [(138, 113, 0), (180, 255, 255)]

    },
    {
        "name": "blue",
        "color": (255, 0, 0),
        "filter": [(90, 113, 0), (107, 255, 255)]
    },
    {
        "name": "green",
        "color": (0, 255, 0),
        "filter": [(38, 113, 0), (81, 255, 255)]
    }
]

count = 0

while(True):
    cap = wincap.get_screenshot()
    # out.write(cap)
    cap_hsv = cv2.cvtColor(cap, cv2.COLOR_BGR2HSV)

    id_char = Identifier('Main', cap_hsv, 100)
    h = cap_hsv.shape[0]
    w = cap_hsv.shape[1]

    h_half = math.floor(h/2)
    w_half = math.floor(w/2)

    match = True
    count = 0

    for item in colors:
        thresh = id_char.apply_hsv_filter(item["filter"])
        rects = id_char.find_contours()
        if (len(rects) > 0):
            count += 1

        if (len(rects) >= 2):
            print(item["name"], rects)
            cv2.rectangle(cap_hsv, rects[0], item["color"], 1)
            match = True
            break
        else:
            match = False

    if (not match and count >= 2):
        control.left()
    # thresh_yellow = id_char.apply_hsv_filter(yellow)

    # thresh_green = id_char.apply_hsv_filter(green)
    # rects_green = id_char.find_contours()
    # print(rects_green)
    # cv2.rectangle(cap_hsv, rects_green[0], (0,255,0), 1)

    # thresh_blue = id_char.apply_hsv_filter(blue)

    # crop_top = cap_hsv[0:100, 100:150]
    # crop_left = ""
    # crop_right = ""
    # crop_bottom = ""

    cv2.imshow('Main', cap_hsv)
    # cv2.imshow('Top', crop_top)

    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
