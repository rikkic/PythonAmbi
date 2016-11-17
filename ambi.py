from __future__ import print_function
import ImageGrab
import cv2
import numpy as np
import time
import serial
from collections import deque

def smoothing(pixel, oldpixel, loop):
    difference = tuple(np.subtract(pixel, oldpixel))
    difference = tuple([int(x / transition) for x in difference])
    newpixel = tuple(np.subtract(pixel, difference))
    #if debug:
    #    print("Screen: %s" % (pixel,))
    #    print("Old   : %s" % (oldpixel,))
    #    print("Diff  : %s" % (difference,))
    #    print("New   : %s" % (newpixel,))
    #if loop % transition == 0:
    if 1:
        loop = 0
        pixel = newpixel
    return pixel

ser = serial.Serial('COM3', 57600)
time.sleep(1)

image = ImageGrab.grab()
x_size, y_size = image.size

x_int = 16
x_lower = (x_size % x_int) / 2
x_upper = x_size - ((x_size % x_int) / 2)
x_step = int(x_size / x_int)

y_int = 7
y_lower = (y_size % y_int) / 2
y_upper = y_size - ((y_size % y_int) / 2)
y_step = int(y_size / y_int)

time.clock()
print("Intialised ambilight")
LEDS = x_int + 2 * y_int
oldpixels = deque(maxlen=(LEDS))
for x in range(0,LEDS):
    oldpixels.append((0,0,0))
transition = 2
debug = False
loop = 0

while 1:
    image = ImageGrab.grab()
    pixelstring = ""
    # NOTE: its img[y: y + h, x: x + w]
    for y in range(y_lower, y_upper, y_step): #Left
        pixel = smoothing(image.getpixel((50, y)), oldpixels.pop(), loop)
        pixelstring += "%03d%03d%03d" % (pixel[0], pixel[1], pixel[2])
        oldpixels.appendleft(pixel)
        #testimage[int(y/10):int((y+y_step)/10), 0:20] = (left[2], left[1], left[0])
    for x in range(x_lower, x_upper, x_step): # Up
        #pixel = image.getpixel((x, 200))
        pixel = smoothing(image.getpixel((x, 200)), oldpixels.pop(), loop)
        pixelstring += "%03d%03d%03d" % (pixel[0], pixel[1], pixel[2])
        oldpixels.appendleft(pixel)
        #testimage[0:20, int(x / 10):int((x + x_step) / 10)] = (top[2], top[1], top[0])
    for y in range(y_lower, y_upper, y_step): # Right
        #pixel = image.getpixel((1870, y))
        pixel = smoothing(image.getpixel((1870, y)), oldpixels.pop(), loop)
        pixelstring += "%03d%03d%03d" % (pixel[0], pixel[1], pixel[2])
        oldpixels.appendleft(pixel)
        #testimage[int(y / 10):int((y + y_step) / 10), 172:192] = (right[2], right[1], right[0])
    ser.write(pixelstring + ";")
    loop+=1
    #time.sleep(1)