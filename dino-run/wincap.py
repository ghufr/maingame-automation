import win32gui
from PIL import ImageGrab
import mss
import mss.tools
import numpy as np
import cv2


class WinCap:
    hwnd = 0
    # cropped_x = 0
    # cropped_y = 0
    # offset_x = 0
    # offset_y = 0
    window_rect = None
    sct = None
    out = None

    def __init__(self, window_name):
        self.hwnd = win32gui.FindWindow(None, window_name)
        self.sct = mss.mss()

        self.window_rect = window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        offset_top = 118
        offset_bottom = 200

        # offset_x = 20

        # self.w = self.w - (offset_x * 2)

        # self.cropped_x = offset_x
        # self.cropped_top = offset_top

    def get_screenshot(self):
        bbox = (80, 770, self.w - 80, self.h - 240)
        raw = self.sct.grab(bbox)
        self.out = np.array(raw)
        # raw = raw.crop((self.cropped_x, self.cropped_top,
        #                 self.w + self.cropped_x, self.h))
        return np.array(raw)

    # def save_screenshot(self, output):
    #     ratio = 0.5
    #     out = self.out[100:self.out.shape[0], 0:self.out.shape[1]]
    #     res = cv2.resize(out, dsize=(round(self.w * ratio), round(self.h * ratio)),
    #                      interpolation=cv2.INTER_CUBIC)
    #     cv2.imwrite(output, res)
        # mss.tools.to_png(res.rgb, res.size, output=output)
