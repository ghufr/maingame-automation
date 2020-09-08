import cv2
from PIL import ImageGrab
import numpy as np
from matplotlib import pyplot as plt
import pyautogui
import time

from wincap import WinCap

from vision import Vision
from hsvfilter import HsvFilter

wincap = WinCap('Kedai Mie Indonesia - Google Chrome')
# toolbar_h = 200


# def capture(left, top, right, bottom):
#     # Take screenshot
#     window_rect = win32gui.GetWindowRect(hwnd)
#     screenshot = ImageGrab.grab(window_rect)

#     w = window_rect[2] - window_rect[0]
#     h = window_rect[3] - window_rect[1]

#     crop_top = h * top
#     crop_right = w - (w * right)
#     crop_bottom = h - (h * bottom)

#     # print(screenshot.size)
#     screenshot = screenshot.crop((left, crop_top, crop_right, crop_bottom))
#     # n_h = int(screenshot.size[0] * 3)
#     # n_w = int(screenshot.size[1] * 3)
#     # screenshot = screenshot.resize((n_h, n_w))
#     return screenshot


def resize(img, scale):

    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)

    # dsize
    dsize = (width, height)

    # resize image
    output = cv2.resize(img, dsize, interpolation=cv2.INTER_CUBIC)

    return output


# vision_bakso = Vision('assets/bakso.png')
vision_sawi = Vision('assets/norm/processed/sawi.png')
vision_telur = Vision('assets/norm/processed/telur.png')

vision_tempe = Vision('assets/tempe.png')
vision_tahu = Vision('assets/tahu-1.png')
vision_bakwan = Vision('assets/bakwan-1.png')
vision_esteh = Vision('assets/esteh-2.png')
vision_esjeruk = Vision('assets/esteh-2.png')

vision_sosis = Vision('assets/sosis-2.png')
vision_udang = Vision('assets/tahu-1.png')
vision_kornet = Vision('assets/tahu-1.png')

visions = [
    {
        'vision': Vision('assets/norm/processed/bakso.png'),
        'label': 'Bakso',
        'confidence': 0.6,
        'hsv_filter': HsvFilter(97, 0, 100, 116, 81, 226, 0, 0, 0, 0)
    },
    {
        'vision': Vision('assets/norm/processed/sawi-alt.png'),
        'label': 'Sawi',
        'confidence': 0.67,
        'hsv_filter': HsvFilter(42, 45, 89, 89, 255, 255, 0, 0, 0, 0)
    },
    {
        'vision': Vision('assets/norm/processed/telur.png'),
        'label': 'Telur',
        'confidence': 0.8,
        'hsv_filter': HsvFilter(89, 0, 95, 123, 227, 248, 0, 0, 0, 0)
    }
]


vision_telur.init_control_gui()

while (True):
    orders = []

    screenshot_bgr = wincap.get_screenshot()
    screenshot_rgb = cv2.cvtColor(screenshot_bgr, cv2.COLOR_BGR2RGB)
    screenshot_gray = cv2.cvtColor(screenshot_bgr, cv2.COLOR_BGR2GRAY)
    screenshot_hsv = cv2.cvtColor(screenshot_bgr, cv2.COLOR_BGR2HSV)

    # Telur (orange)
    # hsv_filter = HsvFilter(89, 0, 95, 123, 227, 248, 0, 0, 0, 0)

    # Sawi (green)
    # hsv_filter = HsvFilter(42, 45, 89, 89, 255, 255, 0, 0, 0 ,0)

    # Sosis, Kornet (Red)
    # hsv_filter = HsvFilter(106, 59, 91, 121, 255, 255, 0, 0, 0 ,0)

    # Bakso (Gray)
    # hsv_filter = HsvFilter(97, 0, 100, 116, 81, 226, 0, 0, 0 ,0)

    # Udang (Yellow)
    # hsv_filter = HsvFilter(98, 21, 214, 110, 221, 225, 0, 0, 0, 0)

    # Tempe (Yellow)
    # hsv_filter = HsvFilter(79, 92, 124, 98, 163, 255, 0, 0, 0, 0)

    # Bakwan (Yellow)
    # hsv_filter = HsvFilter(96, 122, 149, 112, 203, 255, 0 , 0, 0, 0)

    # Check Icon (green)
    # hsv_filter = HsvFilter(32, 122, 149, 87, 203, 255, 0 , 0, 0, 0)

    # Bowl content (yellow)
    # hsv_filter = HsvFilter(54, 20, 115, 114, 255, 255, 0 , 0, 0, 0)

    # Bowl contour (white)
    # hsv_filter = HsvFilter(0, 0, 0, 31, 32, 255, 0, 0, 0, 0)

    # Esteh
    # hsv_filter = HsvFilter(101, 0, 147, 179, 255, 255, 0 , 0, 0, 0)

    # processed_image = cv2.GaussianBlur(screenshot_hsv, (5, 5), 0)
    # processed_image = vision_sawi.apply_hsv_filter(
    #     screenshot_hsv, HsvFilter(42, 45, 89, 89, 255, 255, 0, 0, 0, 0))
    order_image = resize(screenshot_bgr[240:380, 50:250], 2)
    table_image = screenshot_bgr[670:800, 140:320]
    stove_image = screenshot_bgr[580:640, 390:435]

    order_image_gray = cv2.cvtColor(order_image, cv2.COLOR_BGR2GRAY)
    order_image_gray = cv2.GaussianBlur(order_image_gray, (5, 5), 0)

    # _, thresh = cv2.threshold(order_image_gray, 127, 255, 0)
    # contours, hierarchy = cv2.findContours(
    #     thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # cv2.drawContours(order_image, contours, -1, (0, 255, 0), 1)
    for obj in visions:
        processed_image = obj['vision'].apply_hsv_filter(
            cv2.cvtColor(order_image, cv2.COLOR_BGR2HSV))
        vision = obj['vision'].find(order_image_gray, obj['confidence'])
        # vision_image = obj['vision'].draw_rectangles(
        #     processed_image, rectangles)
        cv2.imshow(obj['label'], cv2.cvtColor(vision, cv2.COLOR_BGR2RGB))

    # rectangles = vision_sawi.find(order_image_gray, 0.7)

    # vision_image = vision_sawi.draw_rectangles(
    #     order_image, rectangles)

    cv2.imshow("Screenshot", screenshot_rgb)
    # cv2.imshow("Vision", cv2.cvtColor(vision_image, cv2.COLOR_BGR2RGB))
    # cv2.imshow("Table", table_image)
    # cv2.imshow("Stove", stove_image)

    # screenshot = resize(np.array(capture(70, 0.3, 0.48, 0.55)), 300)
    # screenshot_rgb = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
    # screenshot_hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)

    # screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    # screenshot_gray_blur = cv2.GaussianBlur(screenshot_gray, (5, 5), 0)

    # screenshot_table = np.array(capture(120, 0.7, 0.3, 0.15))

    # # Mangkok or Bungkus?
    # template_bungkus = cv2.imread(
    #     'assets/test-snap.png', cv2.IMREAD_GRAYSCALE)

    # tresh = cv2.threshold(screenshot_gray_blur, 127,
    #                       255, cv2.THRESH_BINARY)[1]

    # tresh = cv2.matchTemplate(tresh, template_bungkus,
    #                           cv2.TM_CCOEFF_NORMED)
    # max_val = cv2.minMaxLoc(tresh)[1]

    # if (max_val > 0.67):
    #     # pyautogui.moveTo(420, 930)
    #     # pyautogui.leftClick(420, 930)
    #     is_wadah_selected = True

    #     print('Pilih Bungkus')
    # else:
    #     # pyautogui.moveTo(310, 930)
    #     # pyautogui.leftClick(310, 930)
    #     is_wadah_selected = True

    #     print('Pilih Mangkok')

    # # Masak Mie
    # print("Masak Mie")
    # # pyautogui.leftClick(420, 650)
    # is_mie_ready = True

    # # Mie Ready State

    # # Matching Isian

    # templates = [
    #     {
    #         'template': template_telur,
    #         'label': 'Telur',
    #         'color': (255, 0, 0),
    #         'confidence': 0.6,
    #         'coor': (290, 690),
    #         'filter': [(50, 100, 0), (60, 255, 255)],
    #         'size': [100, 100]
    #     },
    #     {
    #         'template': template_sawi,
    #         'label': 'Sawi',
    #         'color': (0, 255, 0),
    #         'confidence': 0.6,
    #         'coor': (205, 690)
    #     },
    #     {
    #         'template': template_bakso,
    #         'label': 'Bakso',
    #         'color': (0, 0, 255),
    #         'confidence': 0.56,
    #         'coor': (120, 690)
    #     },
    #     {
    #         'template': template_tempe,
    #         'label': 'Tempe',
    #         'color': (0, 255, 255),
    #         'confidence': 0.6,
    #         'coor': (450, 540)
    #     },
    #     {
    #         'template': template_tahu,
    #         'label': 'Tahu',
    #         'color': (0, 255, 0),
    #         'confidence': 0.6,
    #         'coor': (330, 540)
    #     },
    #     {
    #         'template': template_esteh,
    #         'label': 'Esteh',
    #         'color': (255, 255, 255),
    #         'confidence': 0.8,
    #         'coor': (400, 540),
    #         'filter': [(0, 200, 0), (50, 255, 255)]
    #     },
    #     {
    #         'template': template_bakwan,
    #         'label': 'Bakwan',
    #         'color': (255, 255, 255),
    #         'confidence': 0.78,
    #         'coor': (400, 540)
    #     },
    #     {
    #         'template': template_sosis,
    #         'label': 'Sosis',
    #         'color': (0, 0, 255),
    #         'confidence': 0.72,
    #         'coor': (290, 620)
    #     }
    # ]

    # for curr in templates:
    #     w, h = curr['template'].shape[::-1]

    #     # if (curr['size']):
    #     #     w = curr['size'][0]
    #     #     h = curr['size'][0]

    #     result = cv2.matchTemplate(screenshot_gray_blur,
    #                                curr['template'], cv2.TM_CCOEFF_NORMED)

    #     if 'filter' in curr:
    #         # screenshot_hsv = cv2.GaussianBlur(screenshot_hsv, (5, 5), 0)
    #         tresh = cv2.inRange(
    #             screenshot_hsv, curr['filter'][0], curr['filter'][1])

    #         # gray = cv2.cvtColor(screenshot_hsv, cv2.COLOR_HSV2GRAY)
    #         result = cv2.matchTemplate(tresh,
    #                                    curr['template'], cv2.TM_CCOEFF_NORMED)

    #     # loc = np.where(result >= curr['confidence'])

    #     _, max_val, _, max_loc = cv2.minMaxLoc(result)

    #     if (max_val >= curr['confidence']):
    #         orders.append(curr['label'])
    #         cv2.rectangle(screenshot_hsv, max_loc,
    #                       (max_loc[0] + w, max_loc[1] + h), curr['color'], 1)
    #         # pyautogui.leftClick(curr['coor'][0], curr['coor'][1])

    #     # for pt in zip(*loc[::-1]):
    #     #     cv2.rectangle(screenshot_rgb, pt,
    #     #                   (pt[0] + w, pt[1] + h), curr['color'], 1)
    #     cv2.imshow(curr['label'], tresh)

    # print(orders)
    # cv2.imshow("Screen", screenshot_hsv)
    # cv2.imshow('Table', screenshot_table)

    # print("Serve")
    # pyautogui.leftClick(222, 813)

    # Done State

    # pyautogui.leftClick(70, 950)

    if (cv2.waitKey(25) == ord('q')):
        cv2.destroyAllWindows()
        break
