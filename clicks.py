import pyautogui
import time
import random
import sys
import os
from multiprocessing import Process
import math
import subprocess
import chardet

def sfc32(a, b, c, d):
    a &= 0xFFFFFFFF
    b &= 0xFFFFFFFF
    c &= 0xFFFFFFFF
    d &= 0xFFFFFFFF
    def rng():
        nonlocal a, b, c, d
        t = (a + b) & 0xFFFFFFFF
        a = b ^ (b >> 9)
        b = (c + (c << 3)) & 0xFFFFFFFF
        c = ((c << 21) | (c >> 11)) & 0xFFFFFFFF
        d = (d + 1) & 0xFFFFFFFF
        t = (t + d) & 0xFFFFFFFF
        c = (c + t) & 0xFFFFFFFF
        return t / 4294967296
    return rng

def xfnv1a(string):
    h = 2166136261
    for char in string:
        h ^= ord(char)
        h = (h * 16777619) & 0xFFFFFFFF
    def seed_scramble():
        nonlocal h
        h += h << 13
        h ^= h >> 7
        h += h << 3
        h ^= h >> 17
        h += h << 5
        return h & 0xFFFFFFFF
    return seed_scramble

def generateRandomNumber(seedstring):
    num = xfnv1a(seedstring)
    return sfc32(num(), num(), num(), num())

def getScreenResolution():
    resolution_command = "xdpyinfo | grep dimensions | awk '{ print $2 }'"
    resol_value = subprocess.check_output(resolution_command, shell=True)
    resol_value = resol_value.decode('utf-8')
    resol_value_split = resol_value.split('x')
    print("The output is : "+resol_value_split[0])
    return int(resol_value_split[0])

seed = ""
with open('./out/.cur_input', 'r', encoding='iso-8859-1') as f:
	seed = f.read()

random_number = generateRandomNumber(seed)

for i in range(10):
	val = random_number()
	#print(val)
	x_val = 63 + 390 * val
	y_val = 360 + 230 * val
	pyautogui.click(math.floor(x_val),math.floor(y_val))

pyautogui.click(386,100)

#full window
#x_val = 51 + 412 * random_number
# #y_val = 78 + 541 * random_number
# window_coords = getWindowCoords()
# resolution = getScreenResolution()
#x_val = 63 + 390 * random_number
#y_val = 360 + 230 * random_number
# start_x = window_coords[0]
# start_y = window_coords[1]
# width = window_coords[2]
# height = window_coords[3]
# x_val = start_x-10 + width*random_number
# y_val = start_y-10 + height*random_number
#time.sleep(2)
# print(x_val)
# print(y_val)
# pyautogui.click(math.floor(x_val),math.floor(y_val))
# time.sleep(2)
#pyautogui.click(386,100)

