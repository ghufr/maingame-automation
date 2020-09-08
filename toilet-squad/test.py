import cv2
import time

from wincap import WinCap
from control import Control


wincap = WinCap('Platformnya Game Nasional - Google Chrome')

hsv_filter = [(18, 150, 104), (18, 210, 255)]
# hsv_filter_bg = [(175, 81, 111), (180, 101, 125)]
# hsv_filter_knock = [(16, 169, 220), (18, 186, 255)]
hsv_filter_door = [(0, 100, 80), (180, 250, 200)]
hsv_filter_gray_enemy = [(0, 0, 29), (0, 0, 77)]

control = Control()


DELAY = 0.1

whitelist = []
#     (14694, 7),  # W:3
#     (14048, 9),  # W:3
#     (14469, 11),  # W:3
#     (7074, 5),  # W:2

#     (1280, 6),    # Raja:3
#     (14841, 10),  # Raja:4
#     (14719, 8),  # Raja:3
#     (7013, 5),  # Raja:4

#     (2145, 9),  # Rapper:3
#     (3304, 6),  # Rapper:3
#     (11402, 20),  # Rapper:2
#     (7038, 13),  # Rapper:4
#     (20073, 9),  # Rapper:4
#     (9404, 9),  # Pink guy
#     (14958, 8),  # Pink guy:3

#     (16892, 8),  # Sailor Moon:3
#     (9467, 14),  # Sailor Moon: 3
#     (4391, 8),  # Sailor Moon:4
#     (9276, 12),  # W?:3

#     (18907, 28),  # Doraemon:4
#     (18713, 10),  # Doraemon:3
#     (16141, 9),  # Doraemon:3
#     (16467, 13),  # Mario:4

#     (6989, 12),  # Pikachu:3
#     (17801, 20),  # Pikachu:3
#     (14930, 19),  # Pikachu:3
#     (7516, 8),  # Pikachu:2
#     (1500, 6),  # W?:2
#     (6521, 19),  # W?:3
#     (125, 5),  # W?:1
#     (7394, 6),  # W?:1
#     (2885, 7),  # W?:3
#     (6583, 13),  # W?:3
#     (14988, 13),  # W?:3
#     (17972, 21),  # W?:3
#     (15366, 18),  # W?:3
#     (11883, 20),  # Harry Potter
#     (15647, 14),  # Suster:4
#     (16178, 23),  # W?:3
#     (14664, 24),  # W:2
#     (17107, 14),  # Tukang Bakso:1

#     (13157, 19)  # Superman:4
# ]

blacklist = [
    (200, 2),  # Robot:4
    (25, 1),  # Dark Vader:4,
    (100, 3),  # Dark Vader:2,
    (3396, 4),  # Dark Vader:3
    (6025, 2)  # Dark Vader:3
]

# TODO: Detect black and white enemy

# cap_door = cv2.imread('pintu.png', 0)

while (True):
    is_empty = True

    cap = wincap.get_screenshot()
    cap_crop = cap[470: 680, 230: 340]
    cap_hsv = cv2.cvtColor(cap_crop, cv2.COLOR_BGR2HSV)
    cap_gray = cv2.cvtColor(cap_crop, cv2.COLOR_BGR2GRAY)
    cap_gray_blur = cv2.blur(cap_gray, (3, 3))

    thresh = cv2.inRange(cap_hsv, hsv_filter[0], hsv_filter[1])
    thresh = cv2.rectangle(thresh, (0, 117), (34, 210), (0, 0, 0), -1)
    # thresh = cv2.blur(thresh, (7, 7))

    filter_door = cv2.inRange(cap_hsv, hsv_filter_door[0], hsv_filter_door[1])
    # filter_door = cv2.bitwise_and(filter_door, cap_gray)
    # thresh = cv2.GaussianBlur(thresh, (3, 3), 0)
    # thresh_knock = cv2.inRange(
    #     cap_hsv, hsv_filter_knock[0], hsv_filter_knock[1])

    _, thresh_bg = cv2.threshold(
        filter_door, 127, 255, cv2.THRESH_BINARY)

    thresh_bg = thresh_bg[0:180, 30:thresh_bg.shape[1]]

    # print(thresh_bg.shape[1], thresh_bg.shape[0])

    # _, thresh_door = cv2.threshold(
    #     filter_door, 90, 255, cv2.THRESH_BINARY)

    # thresh_join = cv2.bitwise_and(thresh_bg, cap_hsv)

    cv2.imshow('Capture', cap_crop)
    cv2.imshow('Thresh', thresh)
    cv2.imshow('Thresh BG', thresh_bg)
    cv2.imshow('Filter Door', filter_door)

    contours, _ = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours_bg, _ = cv2.findContours(
        thresh_bg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # contours_knock, _ = cv2.findContours(
    #     thresh_knock, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # cv2.absdiff()

    # print(len(contours_bg), end=" ")

    max_area_bg = 0
    total_area_bg = 0
    for cnt in contours_bg:
        _, _, w, h = cv2.boundingRect(cnt)
        area = w * h
        total_area_bg += area
        if (area > max_area_bg):
            max_area_bg = area

    # print(max_area_bg, end=" ")

    win_size = 14400
    is_blank = abs(total_area_bg - win_size) < 4000

    # lvl3 = 10480

    is_empty = len(contours_bg) < 5 or is_blank

    if (len(contours_bg) > 6):
        is_empty = False

    print(total_area_bg, "-", len(contours_bg), end=": ")

    # if (max_area_bg == lvl3):
    #     continue
    # is_empty = True

    # if len(contours_bg) > 0:
    #     areas = [0]
    #     for cnt in contours_bg:
    #         x, y, w, h = cv2.boundingRect(cnt)
    #         area = w * h
    #         if (area > 10000):
    #             areas.append(area)
    #     if (max(areas) > 28000):
    #         is_empty = True
    #     else:
    #         is_empty = False
    #     print(is_empty)

    # if len(contours_bg) > 6:
    #     is_empty = False
    # else:
    #     areas = [0]
    #     for cnt in contours_bg:
    #         x, y, w, h = cv2.boundingRect(cnt)
    #         area = w * h
    #         if (area > 10000):
    #             areas.append(area)
    #     if (max(areas) > 30000):
    #         is_empty = True
    #     else:
    #         is_empty = False

    if len(contours) > 0:
        areas = [0]
        for cnt in contours:
            rect = cv2.boundingRect(cnt)
            rw = rect[2]
            rh = rect[3]
            area = rw * rh
            # if area > 4000:
            areas.append(area)

        max_area = max(areas)
        sum_area = sum(areas)
        print("Sum: ", sum_area, end=" ")
        # print(max_area)
        if (max_area_bg == 17344 and sum_area == 75):
            continue
            # time.sleep(DELAY)
        if (sum_area > 80 and len(areas) > 1):
            # print('Save')
            control.left()
            time.sleep(DELAY)
        elif not is_empty:
            control.right()
            time.sleep(DELAY)

    elif (not is_empty):
        whitelisted = False
        for white in whitelist:
            diff = abs(total_area_bg - white[0])
            if (diff < 2 and len(contours_bg) == white[1]):
                time.sleep(0.05)
                whitelisted = True
                break
        # if (total_area_bg == 13007 and len(contours_bg) == 19):

        # if (total_area_bg == 6648 and len(contours_bg) == 13):
        #     time.sleep(DELAY)
        #     continue

        # if (total_area_bg == 2225 and len(contours_bg) == 9):
        #     time.sleep(DELAY)
        #     continue

        # if (total_area_bg == 6517 and len(contours_bg) == 8):
        #     time.sleep(DELAY)
        #     continue

        # if (total_area_bg == 17056 and len(contours_bg) == 10):
        #     time.sleep(DELAY)
        #     continue
        if not whitelisted:
            control.right()
            time.sleep(DELAY)
    else:
        # if (total_area_bg == 205 and len(contours_bg) == 2):
        #     control.right()
        # if (total_area_bg == 25 and len(contours_bg) == 1):
        #     control.right()
        # if (total_area_bg == 200 and len(contours_bg) == 2):
        #     control.right()
        # if (total_area_bg == 16925 and len(contours_bg) == 6):
        #     control.right()
        # if (total_area_bg == 1675 and len(contours_bg) == 3):
        #     control.right()
        # if (total_area_bg == 14900 and len(contours_bg) == 7):
        #     control.right()

        # # Detective lvl2
        # if (total_area_bg == 13775 and len(contours_bg) == 5):
        # control.right()
        for black in blacklist:
            if (total_area_bg == black[0] and len(contours_bg) == black[1]):
                control.right()
                time.sleep(DELAY)

    control.center()
    # time.sleep(0.2)
    # control.right()
    print()
    # time.sleep(0.1)
    # loop_time += 1

    if (cv2.waitKey(1) == ord('q')):
        cv2.destroyAllWindows()
        break
