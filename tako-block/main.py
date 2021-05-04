import cv2
import math
import time
import os
import shutil

from wincap import WinCap
from control import Control
from identifier import Identifier


wincap = WinCap('Tako Block - Google Chrome')
# test = wincap.get_screenshot()
# wincap.save_screenshot('output/test.png')
control = Control(debug=False)

block_height = 46

control.start()

count = 0
last_x_terrain = 0
last_b_terrain = 0
last_diff = 0
is_moving = False
is_down = False
click = 0

while(True):
    cap = wincap.get_screenshot()
    # out.write(cap)
    cap_hsv = cv2.cvtColor(cap, cv2.COLOR_BGR2HSV)

    crop = cap_hsv

    cap_w_half = math.floor(cap_hsv.shape[1] / 2)

    cap_char = crop[0:crop.shape[0] - 70, 50:110]
    cap_terrain = crop[0:crop.shape[0] - 70, 120: crop.shape[1]]
    cap_hole = crop[crop.shape[0] - 50:crop.shape[0],
                    110: crop.shape[1]]
    # cap_ = crop[crop.shape[0] - 100:crop.shape[0], 0:40]

    id_char = Identifier('Character', cap_char, 2000)
    id_terrain = Identifier('Terrain', cap_terrain, 200)
    id_end = Identifier('End', crop, 2000)
    id_hole = Identifier('Hole', cap_hole, 500)

    thresh_char = id_char.apply_hsv_filter([(16, 180, 0), (38, 255, 255)])
    thresh_end = id_end.apply_hsv_filter([(0, 0, 63), (29, 215, 200)])

    thresh_terrain = id_terrain.apply_hsv_filter(
        [(64, 127, 0), (66, 255, 255)])
    thresh_hole = id_hole.apply_hsv_filter([(50, 0, 0), (71, 255, 255)])

    rects_char = id_char.find_contours()
    rects_terrain = id_terrain.find_contours()
    rects_hole = id_hole.find_contours()
    rects_end = id_end.find_contours()

    b_terrain = 0
    h_terrain = 0
    x_terrain = 0

    b_char = 0
    h_char = 0
    t_char = 0

    is_terrain = len(rects_terrain) > 0
    is_char = len(rects_char) > 0
    is_level = False

    if (is_terrain):
        terrain = rects_terrain[0]
        cv2.rectangle(cap_terrain, terrain, (0, 0, 255), 2)

        b_terrain = round(
            (abs(cap_terrain.shape[0] - terrain[1] - terrain[3])) / block_height)
        h_terrain = crop.shape[0] - (terrain[1] + terrain[3])
        x_terrain = terrain[0]
        if (x_terrain > 10):
            last_b_terrain = b_terrain
        else:
            last_b_terrain = 0
            click = 0
        # if (abs(last_x_terrain - x_terrain) > 10):
        #     last_x_terrain = x_terrain
        #     is_moving = True
        # else:
        #     is_moving = False

    # highest_point = 0

    if (is_char):
        add = 0
        for i in rects_char:
            cv2.rectangle(cap_char, i, (255, 0, 0), 1)
            # cv2.rectangle(crop, i, (0, 255, 0), 2)
            h_char += i[3]
            y = crop.shape[0] - i[1] - i[3]
            if (y > t_char):
                t_char = y

            if (i[3] > block_height * 2):
                add += 1
        b_char = len(rects_char) - 1 + add

        # print(rects_char[0])
        # h_top = crop.shape[0] - (rects_char[0][1] - rects_char[0][3])

    diff = b_terrain - abs(b_char)
    is_hole = len(rects_hole) > 0 and b_char < 5

    is_changed = False

    if(is_terrain and is_char):
        is_level = h_char >= h_terrain and b_char > 1

    if (is_hole):
        control.add(5)

    if (diff != last_diff):
        last_diff = diff
        is_changed = True

    # if (is_down and is_changed):
    #     control.up()
    #     is_down = False

    # if(is_level or not is_terrain):
    #     control.up()
    #     is_down = False
    # if (b_char == 0 and diff == 1):
    #     control.add(1)
    # if(not is_level and diff == 1 and is_changed and x_terrain > 0):
    #     # control.up()
    #     control.add(1)
        # is_down = False
    # target = last_b_terrain - click
    # if (target > 0):
    #     control.add(target)
    #     click = last_b_terrain
    if (not is_level and is_changed and diff > 0 and x_terrain > 0):
        control.add(diff)

    # if (not is_level and is_changed and x_terrain > 0 and diff > 0):
    #     if (not is_down):
    #         is_down = True
    #         control.down()

    print(count, ":", b_terrain, b_char, diff,
          h_terrain, h_char, is_level, click, is_changed)
    log = str(b_terrain) + "," + str(b_char) + \
        "," + str(diff) + ',' + str(is_hole) + "," + \
        str(h_terrain) + "," + str(t_char) + "," + \
        str(is_level) + "," + str(is_changed)
    cv2.putText(crop, log, (0, 50), cv2.FONT_HERSHEY_SIMPLEX,
                0.8, color=(0, 0, 0), thickness=2)

    # print(count)
    cv2.imshow('Capture', crop)
    cv2.imshow('Character', thresh_char)
    cv2.imshow('Terrain', cap_terrain)
    cv2.imshow('Hole', cap_hole)
    # cv2.imshow('Pass', cap_passed)
    ratio = 0.5
    if (count > 200):
        count = 1
    res = cv2.resize(crop, dsize=(round(crop.shape[1] * ratio), round(crop.shape[0] * ratio)),
                     interpolation=cv2.INTER_CUBIC)

    cv2.imwrite('output/' + str(count) + '.png', res)

    is_end = b_char + h_char == 0
    count += 1

    if cv2.waitKey(1) == ord('q') or is_end:
        print("end at count " + str(count))
        cv2.destroyAllWindows()
        break
