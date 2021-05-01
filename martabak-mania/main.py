import cv2
import time


from wincap import WinCap
from identifier import Identifier
from control import Control

# Ayo Gabung Kompetisi
# Martabak Mania
# Platformnya Game Nasional
wincap = WinCap('Ayo Gabung Kompetisi - Google Chrome')
control = Control()


topping_list = [
    Identifier('oreo', [(0, 0, 0), (180, 82, 70)]),
    Identifier('matcha', [(30, 70, 14), (37, 255, 255)]),
    Identifier('strawberry', [(148, 33, 44), (169, 255, 255)]),
    Identifier('keju', [(22, 13, 242), (27, 255, 255)]),
    Identifier('meses', [(13, 92, 33), (16, 182, 113)]),
    Identifier('nuttella', [(6, 141, 32), (10, 193, 172)]),
    Identifier('kacang', [(14, 192, 0), (15, 255, 255)]),
    # Identifier('skacang', [(18, 159, 223), (18, 182, 255)]),
    Identifier('skacang', [(17, 129, 217), (18, 155, 255)]),

]

control.start()
limit = 2940

while (limit > 0):
    cap = wincap.get_screenshot()
    # y1:y2, x1:x2
    crop = cap[330:460, 43:200]

    crop_hsv = cv2.cvtColor(crop, cv2.COLOR_RGB2HSV)
    crop_gray = cv2.cvtColor(crop, cv2.COLOR_RGB2GRAY)

    toppings = [None] * 8

    cs = 24
    h = crop.shape[0]
    w = crop.shape[1]
    rw = int(w / 2) + 1
    rh = int(h / 2)

    topping_position = [
        [(rw + 2, rw + 2 + cs), (10, 10 + cs)],
        [(rw + 40, rw + 40+cs), (34, 34 + cs)],
        [(rw + 45, rw + 45 + cs), (rh, rh + cs)],
        [(rw + 4, rw + 4 + cs), (h-5 - cs, h-5)],
        [(rw - 2 - cs, rw - 2), (h-3 - cs, h-3)],
        [(14, 14 + cs), (68, 68 + cs)],
        [(14, 14 + cs), (40, 40 + cs)],
        [(rw - 2 - cs, rw - 2), (7, 7 + cs)]
    ]

    for top in topping_list:
        top_masked = top.apply_hsv_filter(crop_hsv, crop_gray)

        # crop_1 = top_masked
        # crop_2 = top_masked[34:34 + cs, rw + 31: rw + 31+cs]
        # crop_3 = top_masked[68:68 + cs, rw + 45: rw + 45+cs]
        # crop_4 = top_masked[h-7 - cs:h-7, rw + 2: rw + 2+cs]

        # crop_5 = top_masked[h-7 - cs:h-7, rw - 2 - cs: rw - 2]
        # crop_6 = top_masked[68:68 + cs, 14: 14 + cs]
        # crop_7 = top_masked[34:34 + cs, 9: 9 + cs]
        # crop_8 = top_masked[7:7 + cs, rw - 2 - cs: rw - 2]
        # cv2.imshow(top.label, top_masked)
        index = 0
        # top_loc = []
        for pos in topping_position:
            x1, x2 = pos[0]
            y1, y2 = pos[1]
            pos_masked = top_masked[y1:y2, x1:x2]
            if (top.label == 'kacang'):
                cv2.imshow(top.label + str(index), pos_masked)
            top_rects, _ = top.find(pos_masked)
            if (len(top_rects) > 0):
                # print(len(top_rects), end=" ")
                # top_loc.append(index)
                toppings[index] = top.label
            else:
                cv2.rectangle(crop, (x1, y1), (x2, y2),
                              thickness=2, color=(0, 0, 0))
            index += 1
        # if (len(top_loc) > 0):
        #     print(top.label, top_loc)
    # print(toppings)

    print(toppings)
    print()
    control.butter()
    for top in toppings:
        if top is not None:
            control.pick_topping(top)
            # time.sleep(0.3)
        else:
            control.pick_topping('kacang')

    control.serve()
    limit -= 1
    control.trash()
    time.sleep(2)

    cv2.imshow('Crop', crop)
    if (cv2.waitKey(1) == ord('q')):
        cv2.destroyAllWindows()
        break
