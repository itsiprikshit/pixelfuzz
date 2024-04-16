#! python3
import time
import pyautogui, sys
import os
from multiprocessing import Process

print('Press Ctrl-C to quit.')

def task():
    os.system("mate-calc")
    # os.system("/usr/bin/gnome-calculator")

process = Process(target=task)
process.start()

pyautogui.FAILSAFE = False

time.sleep(5)

x = 386
y = 85


pyautogui.keyDown('ctrlleft')
pyautogui.press('q')
pyautogui.keyUp('ctrlleft')

print("ended")


exit(0)
# pyautogui.click(386, 85)
# exit(0)

# Calculator height top is y = 114 and bottom is 138 and x is 60
# For gnome calc - 85 is top y for close

for i in range(50):
    for j in range(200):
        xc = x + j
        yc = y + i
        print(f'{xc}, {yc} \n')
        pyautogui.click(x = xc, y = yc)