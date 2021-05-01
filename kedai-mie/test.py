import cv2
import numpy as np
import time

from wincap import WinCap

from identifier import Identifier
from control import Control

# Kedai Mie Indonesia
# Platformnya Game Nasional
# Ayo Gabung Kompetisi
wincap = WinCap('Platformnya Game Nasional - Google Chrome')
control = Control()

topping_list = [
    Identifier('Sawi', [(48, 36, 0), (72, 255, 255)], 42, 24),
    Identifier('Telur', [(14, 191, 0), (21, 255, 226)], 22, 22),
    Identifier('Bakso', [(0, 0, 121), (17, 72, 226)], 24, 24),
    Identifier('Sosis', [(4, 56, 146), (9, 255, 249)], 40, 20),
    Identifier('Kornet', [(8, 57, 0), (14, 202, 255)], 21, 28),
    Identifier('Udang', [(14, 24, 231), (19, 180, 255)], 32, 32),
]

drink_list = [
    Identifier('Esteh', [(8, 52, 161), (13, 255, 243)], 23, 39),
    Identifier('Esjeruk', [(15, 169, 0), (23, 255, 255)], 20, 30)
]

snack_list = [
    Identifier('Tahu', [(15, 99, 115), (26, 193, 225)], 30, 34),
    Identifier('Tempe', [(20, 90, 136), (41, 184, 250)], 30, 34),
    Identifier('Bakwan', [(6, 111, 0), (25, 196, 223)], 30, 34),
]

stove_status = Identifier(
    'Stove Status', [(48, 36, 0), (72, 255, 255)], 30, 30)
serving_status = Identifier(
    'Serving Status', [(48, 36, 0), (72, 255, 255)], 36, 34)


def convert_color(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return img_hsv, img_gray


def find_addons(img, items):
    result = []
    max_area = 0

    for item in items:
        img_hsv, img_gray = convert_color(img)
        img_masked = item.apply_hsv_filter(img_hsv, img_gray)
        img_rects, img_sizes = item.find(img_masked)

        if (len(img_rects) > 0):
            result.append(item.label)
    return result


tick = 0
while (True):
    cap = wincap.get_screenshot()
    cap_crop = cap[285:385, 45:230]
    cap_crop_stove = cap[590:680, 365:410]
    cap_crop_top = cap_crop[0:38, 50:140]
    cap_crop_left = cap_crop[0:60, 0:60]
    cap_crop_right = cap_crop[0:80, 150:200]
    cap_crop_center = cap_crop[10:85, 30: 146]

    cap_crop_hsv = cv2.cvtColor(cap_crop, cv2.COLOR_RGB2HSV)
    cap_crop_gray = cv2.cvtColor(cap_crop, cv2.COLOR_RGB2GRAY)
    cap_crop_gray_blur = cv2.GaussianBlur(cap_crop_gray, (5, 5), 0)

    additionals = []
    toppings = []
    drink = ''
    snack = ''
    plate = 1
    is_noodle_ready = False
    is_served = False

    _, bthresh = cv2.threshold(cap_crop_gray, 127, 255, cv2.THRESH_BINARY)

    bthresh_blur = cv2.GaussianBlur(bthresh, (7, 7), 0)
    canny = cv2.Canny(bthresh_blur, 100, 300, apertureSize=3)
    circles = cv2.HoughCircles(bthresh_blur, cv2.HOUGH_GRADIENT, 1,
                               bthresh_blur.shape[0]/64, param1=100, param2=24, minRadius=54, maxRadius=82)

    # 0 = Mangkok
    # 1 = Bungkus
    # print(circles)
    if circles is not None:
        plate = 0
    else:
        plate = 1

    center_hsv, center_gray = convert_color(cap_crop_center)
    for top in topping_list:
        top_masked = top.apply_hsv_filter(center_hsv, center_gray)
        if (top.label == 'Kornet'):
            top_masked = top_masked[10:100, 0:50]

        if (top.label == 'Sosis'):
            top_masked = top_masked[0:35, 35:80]
        if (top.label == 'Telur'):
            top_masked = top_masked[20:55, 40:75]
            cv2.imshow('T', top_masked)

        if (top.label == 'Bakso'):
            top_masked = top_masked[0:70, 70: 100]
        top_rects, _ = top.find(top_masked)
        if (len(top_rects) > 0):
            toppings.append(top.label)

    top_hsv, top_gray = convert_color(cap_crop_top)

    serve_masked = serving_status.apply_hsv_filter(top_hsv, top_gray)
    serve_rects, _ = serving_status.find(serve_masked)

    # print(len(serve_rects))
    if (len(serve_rects) > 0):
        # serve_masked = serving_status.draw_rectangles(
        #     serve_masked, serve_rects)
        is_served = True

    if (len(toppings) > 0):
        # time.sleep(2)

        stove_hsv, stove_gray = convert_color(cap_crop_stove)
        stove_masked = stove_status.apply_hsv_filter(stove_hsv, stove_gray)
        stove_rect, _ = stove_status.find(stove_masked)
        # print(len(stove_rect))
        # cv2.imshow('Stove status', stove_masked)
        # print(len(stove_rect))
        if (len(stove_rect) > 0):
            control.pick_plate(plate)
            control.pick_noodle()
            time.sleep(0.05)
            control.pick_toppings(toppings)
            control.serve()
            control.trash()
            tick = 0

    if not is_served:
        control.pick_noodle()

        # Check drinks
        drink = find_addons(cap_crop_right, drink_list)
        # Check snack
        snack = find_addons(cap_crop_left, snack_list)

        if (len(drink) > 0):
            additionals.extend(drink)

        if (len(snack) > 0):
            additionals.extend(["Tahu", "Tempe", "Bakwan"])

        control.pick_addons(additionals)
        time.sleep(0.3)

    print(is_served, plate, toppings, additionals, tick)
    tick += 1

    cv2.imshow('Cap Crop', cap_crop)
    # cv2.imshow('Cap Crop Stove', cap_crop_stove)
    # cv2.imshow('Canny', circles)

    # cv2.imwrite('test.png', cap_crop)

    # time.sleep(0.2)
    # break

    if (tick > 50):
        control.play_again()
        control.play()
        control.start()

    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
