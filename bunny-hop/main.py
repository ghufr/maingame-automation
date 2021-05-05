import cv2
import math
import time
import os
import shutil

from wincap import WinCap
from control import Control
from identifier import Identifier


wincap = WinCap('Hop Bunny Hop - Google Chrome')
# test = wincap.get_screenshot()
# wincap.save_screenshot('output/test.png')
control = Control(debug=False)

control.start()

count = 0

while(True):
    cap = wincap.get_screenshot()
    cap_hsv = cv2.cvtColor(cap, cv2.COLOR_BGR2HSV)

    id_terrain = Identifier('Terrain', cap_hsv, 2000)
    id_clock = Identifier('Clock', cap_hsv, 200)

    thresh_char = id_terrain.apply_hsv_filter([(38, 129, 0), (80, 255, 189)])
    thresh_clock = id_clock.apply_hsv_filter([(121, 169, 0), (180, 255, 255)])
    rects_terrain = id_terrain.find_contours()
    rects_clock = id_clock.find_contours()

    is_next = False
    is_next_next = False
    is_next_clock = len(rects_clock) > 0 and rects_clock[0][0] < 50

    # cv2.rectangle(cap_hsv, rects_clock[0], (0, 255, 0), 2)

    if (len(rects_terrain) > 0):
        # print(rects_chart)
        for i in rects_terrain:
            if (i[0] < 10):
                is_next = True
            if (i[0] > 60):
                is_next_next = True
            cv2.rectangle(cap_hsv, i, (0, 0, 255), 2)

    if (is_next_next and not is_next_clock):
        control.right()
    else:
        control.left()

    time.sleep(0.2)
    cv2.imshow('Capture', cap_hsv)
    cv2.imshow('Character', thresh_char)
    ratio = 0.5
    if (count > 200):
        count = 1
    res = cv2.resize(cap_hsv, dsize=(round(cap_hsv.shape[1] * ratio), round(cap_hsv.shape[0] * ratio)),
                     interpolation=cv2.INTER_CUBIC)

    cv2.imwrite('output/' + str(count) + '.png', res)

    count += 1

    if cv2.waitKey(1) == ord('q'):
        print("end at count " + str(count))
        cv2.destroyAllWindows()
        break
