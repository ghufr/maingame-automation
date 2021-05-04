import cv2
import math
import time
import os
import shutil
import time

from wincap import WinCap
from control import Control
from identifier import Identifier

# Platformnya Game Nasional
wincap = WinCap('Tako Dino Run - Google Chrome')
# test = wincap.get_screenshot()
# wincap.save_screenshot('output/test.png')
control = Control(debug=False)

block_height = 46

control.start()

count = 0
last_pos = [0, 0, 0, 0]
last_time = 0
fps = 0

while(True):
    cap = wincap.get_screenshot()
    # out.write(cap)
    cap_hsv = cv2.cvtColor(cap, cv2.COLOR_BGR2HSV)

    # crop = cap_hsv[330:wincap.h - 240, 0:wincap.w]

    cap_w_half = math.floor(cap_hsv.shape[1] / 2)

    # cap_char = crop[0:crop.shape[0], 90:180]
    cap_terrain = cap_hsv[0:cap_hsv.shape[0], 85:cap_hsv.shape[1]]
    # cap_hole = cap_hsv[cap_hsv.shape[0] - 100:cap_hsv.shape[0],
    #                    150: cap_hsv.shape[1]]
    # cap_ = crop[crop.shape[0] - 100:crop.shape[0], 0:40]

    # id_char = Identifier('Character', cap_char, 2000)
    id_terrain = Identifier('Terrain', cap_terrain, 800)
    # id_end = Identifier('End', crop, 2000)
    # id_hole = Identifier('Hole', cap_hole, 1000)

    # thresh_char = id_char.apply_hsv_filter([(0, 0, 0), (30, 255, 255)])
    # thresh_end = id_end.apply_hsv_filter([(0, 0, 63), (29, 215, 200)])

    thresh_terrain = id_terrain.apply_hsv_filter(
        [(142, 0, 70), (180, 255, 255)])
    # thresh_hole = id_hole.apply_hsv_filter([(50, 0, 0), (71, 255, 255)])

    # rects_char = id_char.find_contours()
    rects_terrain = id_terrain.find_contours()
    # rects_hole = id_hole.find_contours()
    # rects_end = id_end.find_contours()

    # bottom = 0
    # h_top = 0
    # h_terrain = 0

    # if (len(rects_end) > 0):
    #     break

    # print(rects_terrain)
    is_terrain = len(rects_terrain) > 0
    # is_char = len(rects_char) > 0
    # is_level = False
    if (is_terrain):
        # print(rects_terrain[0])
        c = 0
        for terrain in rects_terrain:
            jump_duration = 0.2
            speed = round((last_pos[c] - terrain[0]), 2)
            time_to_impact = 0
            height = 0
            terrain_height = terrain[3]
            if (speed > 0):
                time_to_impact = terrain[0] / speed
            last_pos[c] = terrain[0]
            cv2.rectangle(cap_terrain, rects_terrain[0], (255, 0, 0), 1)
            # print(terrain)
            c += 1

            log = "T" + \
                str(c) + ":" + str(terrain[0]) + "|" + \
                str(speed) + "|" + str(time_to_impact)

            cv2.putText(cap_hsv, log, (10, 10 * c), cv2.FONT_HERSHEY_SIMPLEX,
                        0.4, color=(0, 0, 0), thickness=1)

            if (time_to_impact > 0 and time_to_impact < 10 and terrain[0] < 100 and speed < 60):
                control.click()
                last_pos = [0, 0, 0, 0]

        # cv2.rectangle(crop, rects_terrain[0], (0, 0, 255), 2)

        # print(rects_terrain[0])
        # bottom = round(
        #     (abs(crop.shape[0] - rects_terrain[0][1] - rects_terrain[0][3])) / block_height)
        # bottom = (rects_terrain[0][3] + 10) / block_height
        # print(rects_terrain[0])
        # h_terrain = rects_terrain[0][1] + rects_terrain[0][3]

    # if (is_char):
    #     add = 0
    #     for i in rects_char:
    #         cv2.rectangle(cap_char, i, (255, 0, 0), 1)
    #         # cv2.rectangle(crop, i, (0, 255, 0), 2)
    #         # if (i[3] > block_height * 2):
    #         #     add += 1

    #     h_char = len(rects_char) - 1 + add
    #     # print(rects_char[0])
    #     h_top = rects_char[0][1] + rects_char[0][3]

    # if(is_terrain and is_char):
    #     is_level = h_top - h_terrain < 10
    # else:
    #     is_level = False
    # diff = bottom - abs(h_char)
    # is_hole = len(rects_hole) > 0 and h_char < 6

    # if (is_hole):
    # print("Hole")
    # for i in range(10):
    # control.add(5)

        # for i in range(diff):

    # print(bottom, h_char, diff, h_terrain, h_top)

    # if (len(rects_passed) > 0):
    # count += 1

    # print(count)
    cv2.imshow('Capture', cap_hsv)
    # cv2.imshow('Character', thresh_char)
    # cv2.imshow('Terrain', cap_terrain)
    # cv2.imshow('Hole', cap_hole)
    # cv2.imshow('Pass', cap_passed)
    # ratio = 2
    count += 1
    if (count > 300):
        count = 1
    # res = cv2.resize(cap_hsv, dsize=(round(cap_hsv.shape[1] * ratio), round(cap_hsv.shape[0] * ratio)),
    #                  interpolation=cv2.INTER_CUBIC)
    cv2.imwrite('./output/' + str(count) + '.png', cap_hsv)
    fps = round((1./(time.time() - last_time)))
    last_time = time.time()
    print("FPS: " + str(fps))
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
