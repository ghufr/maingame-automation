import cv2
import numpy as np
# from time import time
import time

from identifier import Identifier
from wincap import WinCap
from control import Control


# Init Object
idn_star = Identifier(
    'Star', [(16, 85, 0), (33, 255, 255)], 30, 30)

idn_player = Identifier(
    'Player', [(0, 0, 0), (0, 0, 255)], 36, 90)

idn_obs_1 = Identifier(
    'Log', [(4, 106, 0), (14, 255, 255)], 70, 40)

idn_obs_2 = Identifier(
    'Hole', [(2, 0, 0), (24, 74, 48)], 40, 40)

idn_obs_3 = Identifier(
    'Stone', [(0, 0, 0), (0, 0, 224)], 60, 40)

obstacles = [
    idn_obs_1,
    idn_obs_2,
    idn_obs_3
]

cap = WinCap('Road Rush - Google Chrome')
control = Control(cap.ww, cap.wh, debug=False)


def identify_lane(x, w):
    a_third = int(w / 3)  # 172

    # print(x)
    thresh = 100
    if (x < a_third):
        return 0
    if (a_third < x < a_third * 2):
        return 1
    if (x > a_third * 2):
        return 2


possible_moves = [
    ['R'],
    ['L', 'R'],
    ['L'],
]

loop_time = time.time()

while (True):
    img = cap.get_screenshot()

    print('FPS {}'.format(1 / (time.time() - loop_time)))
    loop_time = time.time()

    w = img.shape[1]
    h = img.shape[0]

    img_bgr = img[int(h * 0.3):h - 80, 60:w - 60]

    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    player_masked = idn_player.apply_hsv_filter(img_hsv, img_gray)
    player_rectangles = idn_player.find(player_masked)
    img_bgr = idn_player.draw_rectangles(
        img_bgr, player_rectangles, (0, 255, 255))

    player_lane = 1
    player_pos = (0, 0)
    if (len(player_rectangles) == 1):
        # TODO: Check position
        x, y, rw, rh = player_rectangles[0]
        player_pos = (x + int(0.5 * rw), y)
        img_bgr = cv2.circle(img_bgr, player_pos, 2, (0, 255, 0), 2)
        player_lane = identify_lane(player_pos[0], w)
        possible_move = possible_moves[player_lane]

    obs_list = []

    for obs in obstacles:
        obs_masked = obs.apply_hsv_filter(img_hsv, img_gray)
        rectangles = obs.find(obs_masked)
        # img_bgr = obs.draw_rectangles(img_bgr, rectangles, (0, 0, 255))
        obs_lane = 0
        if (len(rectangles) > 0):

            x, y, rw, rh = rectangles[0]
            pos = (x + int(0.5 * rw), y + rh)
            # img_bgr = cv2.circle(img_bgr, pos, 2, (0, 255, 0), 2)
            obs_lane = identify_lane(x + int(0.5 * rw), w)
            diff = abs(obs_lane - player_lane)
            distance_from_player = player_pos[1] - (y + rh)
            # print(diff)
            if diff == 0:
                # print(distance_from_player)
                if 0 < distance_from_player < 120:
                    control.turn(possible_move[0])
                    time.sleep(0.1)

            # if diff == 2:
            #     print(distance_from_player)
            #     pass
            # DO something
            # obs_list.push()
            # TODO: Check obs position
    # cv2.imshow('Image', img_bgr)

    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
