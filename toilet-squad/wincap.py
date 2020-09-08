import win32gui
import win32ui
import win32con
from PIL import ImageGrab
import numpy as np


class WinCap:
    hwnd = 0
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0
    window_rect = None
    w = 0
    h = 0

    ww = 0
    wh = 0

    def __init__(self, window_name):
        self.hwnd = win32gui.FindWindow(None, window_name)

        self.window_rect = window_rect = win32gui.GetWindowRect(self.hwnd)
        self.ww = window_rect[2] - window_rect[0]
        self.wh = window_rect[3] - window_rect[1]

        offset_top = 80
        offset_x = 40

        # self.h = self.wh - offset_top
        # self.w = self.ww - (offset_x * 2)

        self.cropped_x = offset_x
        self.cropped_y = offset_top

        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

    def get_screenshot(self):
        # raw = ImageGrab.grab(self.window_rect)
        # raw = raw.crop((self.cropped_x, self.cropped_top,
        #                 self.w + self.cropped_x, self.h))

        wDC = win32gui.GetWindowDC(None)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.ww, self.wh)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.ww, self.wh), dcObj,
                   (0, 0), win32con.SRCCOPY)

        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.wh, self.ww, 4)

        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        img = img[..., :3]

        img = np.ascontiguousarray(img)

        return img
