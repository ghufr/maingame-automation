import pyautogui
count = 50
max = 450
pyautogui.PAUSE = 0.005
while(True):
    count += 20
    pyautogui.click(count, 500)
    if (count >= max):
        count = 50
