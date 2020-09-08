import win32gui
from PIL import ImageGrab
import numpy as np


class WinCap:
    hwnd = 0
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0
    window_rect = None

    def __init__(self, window_name):
        self.hwnd = win32gui.FindWindow(None, window_name)

        self.window_rect = window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        offset_top = 210
        offset_x = 40

        self.h = self.h - offset_top + 60
        self.w = self.w - (offset_x * 2)

        self.cropped_x = offset_x
        self.cropped_top = offset_top

    def get_screenshot(self):
        raw = ImageGrab.grab(self.window_rect)
        raw = raw.crop((self.cropped_x, self.cropped_top,
                        self.w + self.cropped_x, self.h))
        return np.array(raw)
