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

battle = [
    ['c', 'l', 'r'],
    ['r', 'c', 'l'],
    ['l', 'r', 'c']
]


while(True):
    h_char = 0
    cap = wincap.get_screenshot()
    cap_hsv = cv2.cvtColor(cap, cv2.COLOR_RGB2HSV)

    crop = cap_hsv[250:450, 150:wincap.w - 150]
    crop_w_half = math.floor(crop.shape[1] / 2)

    id_center = Identifier('Center', crop)

    hand_filter = [(3, 0, 0), (20, 255, 255)]

    thresh_center = id_center.apply_hsv_filter(hand_filter)
    # thresh_right = id_right.apply_hsv_filter(hand_filter)

    # thresh_terrain = id_terrain.apply_hsv_filter([(0, 0, 0), (36, 255, 255)])
    # thresh_hole = id_hole.apply_hsv_filter([(50, 0, 0), (71, 255, 255)])

    rects_center = id_center.find_contours()

    # print(crop_w_half)
    left = 0
    right = 0
    if (len(rects_center) > 0):
        # print(rects_center)
        for i in rects_center:
            if (i[0] > crop_w_half):
                right += 1
                cv2.rectangle(crop, i, (0, 0, 255), 1)
            else:
                left += 1
                cv2.rectangle(crop, i, (255, 0, 0), 1)

        if (left > 0):
            left -= 1
        if (right > 0):
            right -= 1

    res = battle[left][right]

    print(left, right, res)
    control.click(res)
    # rects_right = id_right.find_contours()

    cv2.imshow('Center', crop)
    time.sleep(0.8)
    # cv2.imshow('Right', thresh_right)

    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
