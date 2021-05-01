import cv2
import math
import time
import os
import shutil

from wincap import WinCap
from identifier import Identifier
from control import Control


wincap = WinCap('Cocos Creator | Jumpin-Cube - Google Chrome')
control = Control()

block = Identifier()


tick = 0
shutil.rmtree("./out/", True)
os.mkdir("./out")
os.chdir("./out")

control.start()
control.start()

time.sleep(1)


while(True):
    cap = wincap.get_screenshot()

    cap_h_half = math.floor(cap.shape[0] * 0.6)
    cap_w_half = math.floor(cap.shape[1] * 0.5)

    block_size = 24
    offset_left = 0
    gap = 20
    if (tick < 20):
        gap = 60 - (tick * 2)
    block_size_half = math.floor(block_size / 2)
    y1 = cap_h_half + block_size
    y2 = cap_h_half + (block_size * 2)

    x11 = cap_w_half - block_size_half
    x21 = cap_w_half + block_size_half

    x12 = cap_w_half + gap + block_size_half
    x22 = x12 + block_size

    x13 = x22 + gap
    x23 = x13 + block_size

    cap_crop_start = cap[y1:y2, x11:x21]
    cap_crop_mid = cap[y1:y2, x12:x22]
    cap_crop_end = cap[y1:y2, x13:x23]

    is_block_mid = block.detect(cap_crop_mid)
    is_block_start = block.detect(cap_crop_start)
    is_block_end = block.detect(cap_crop_end)

    is_gameover = block.is_gameover(cap)

    if not is_gameover:
        tick += 1
        print(tick, end=" - ")
        cv2.rectangle(cap, (x11, y1), (x21, y2),
                      (255, 0, 0), 1)  # Blue - START
        cv2.rectangle(cap, (x12, y1), (x22, y2), (0, 255, 0), 1)  # Green - MID
        cv2.rectangle(cap, (x13, y1), (x23, y2), (0, 0, 255), 1)  # Red - END

        if is_block_start and is_block_mid:
            if is_block_end:
                control.long()
                time.sleep(0.065)
            else:
                control.short()
                cv2.imwrite(str(tick) + ".png", cap)
                time.sleep(0.045)
        elif is_block_end:
            control.long()
            cv2.imwrite(str(tick) + ".png", cap)
            time.sleep(0.065)
        else:
            control.short()
            cv2.imwrite(str(tick) + ".png", cap)
            time.sleep(0.045)

        print("\n")
    else:
        cv2.destroyAllWindows()
        break

    cv2.imshow('Cap Mid', cap_crop_mid)
    cv2.imshow('Cap Start', cap_crop_start)
    cv2.imshow('Cap', cap)

    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
