import cv2
import math
import time
import os
import shutil

from wincap import WinCap
from control import Control
from identifier import Identifier


wincap = WinCap('Rock Paper Scissors - Google Chrome')
control = Control(debug=False)

# control.start()


while(True):
    h_char = 0
    cap = wincap.get_screenshot()
    cap_hsv = cv2.cvtColor(cap, cv2.COLOR_RGB2HSV)

    cap_h_half = math.floor(cap_hsv.shape[0] / 2)
    cap_w_half = math.floor(cap_hsv.shape[1] / 2)

    crop = cap_hsv[240:cap_h_half, 0:wincap.w]
    left = crop[0:crop.shape[0], 0:cap_w_half]
    right = crop[0:crop.shape[0], cap_w_half: crop.shape[1]]

    id_left = Identifier('Left', left)
    id_right = Identifier('Right', right)
    # id_char = Identifier('Character', cap_char)
    # id_terrain = Identifier('Terrain', cap_terrain)
    # id_hole = Identifier('Hole', cap_hole)

    hand_filter = [(3, 0, 0), (20, 255, 255)]

    thresh_left = id_left.apply_hsv_filter(hand_filter)
    thresh_right = id_right.apply_hsv_filter(hand_filter)

    # thresh_terrain = id_terrain.apply_hsv_filter([(0, 0, 0), (36, 255, 255)])
    # thresh_hole = id_hole.apply_hsv_filter([(50, 0, 0), (71, 255, 255)])

    rects_left = id_left.find_contours()
    rects_right = id_right.find_contours()

    cv2.drawContours(left, rects_left, -1, (255, 0, 0), 2)
    cv2.drawContours(right, rects_right, -1, (0, 0, 255), 2)

    # rects_hole = id_hole.find_contours()

    # cv2.imshow('Character', cap_char)
    # cv2.imshow('Terrain', cap_terrain)
    # cv2.imshow('Hole', cap_hole)
    cv2.imshow('Left', thresh_left)
    cv2.imshow('Right', thresh_right)

    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
