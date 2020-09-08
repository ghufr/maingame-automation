import win32gui
import win32ui
import win32con


def get_screenshot(window_name):
    hwnd = win32gui.FindWindow(None, window_name)

    window_rect = win32gui.GetWindowRect(hwnd)
    w = window_rect[2] - window_rect[0]
    h = window_rect[3] - window_rect[1]

    wDC = win32gui.GetWindowDC(None)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (w, h), dcObj,
               (0, 0), win32con.SRCCOPY)

    dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')

    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())


get_screenshot('Road Rush')
