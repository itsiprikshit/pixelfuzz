import pyautogui
import time
import random
import os
from multiprocessing import Process

def task():
    os.system("/usr/bin/gnome-calculator")

# process = Process(target=task)
# process.start()

#close calculator
time.sleep(3)

f = open("./guinter.txt", "a")

f.write(f"{pyautogui.size()}\n")
f.write(f"{pyautogui.position()}\n")
f.close()

pyautogui.click(160, 434)
time.sleep(2)
pyautogui.click(386, 100)

i = 1

f = open("./guinter.txt", "a")

while  i < 5:
    f.write(f"{i}\n")
    i = i + 1

f.close()
