#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from neopixel import *
import argparse
import pandas as pd
import numpy as np

BLACK = Color(0,0,0)
RED = Color(255,0,0)
GREEN = Color(0,255,0)
BLUE = Color(0,0,255)

class Rectangle():
    def __init__(self, origin_x, origin_y, width, height):
        self.X = origin_x
        self.Y = origin_y
        self.width = width
        self.height = height
        
    def __str__(self):
        name = "X: " + str(self.X) + "\n"
        name += "Y: " + str(self.Y) + "\n"
        name += "widht: " + str(self.width) + "\n"
        name += "height: " + str(self.height) + "\n"
        return name


def from_mapping_file_to_led_array(file, ROI):
    dt = pd.read_excel(file)
    all_column_names = ["Line "+ str(i) for i in range(ROI.X, ROI.X + ROI.width)]
    dt = dt[all_column_names]
    dt = dt[ROI.Y : ROI.Y  + ROI.height]
    dt = dt.fillna(-1)
    return np.array(dt.values).astype(np.int32)


class MaskDisposition():
    
    def __init__(self, mapping_file, rectangle_of_interest):
        self.ROI = rectangle_of_interest;
        self.disposition = from_mapping_file_to_led_array(mapping_file, self.ROI)
        self.led_number = np.sum(self.disposition != -1)

class LedStrip():
    
    def __init__(self, mask_disposition, brightness):
        self.height = mask_disposition.ROI.height
        self.width = mask_disposition.ROI.width
        self.disposition = mask_disposition.disposition
        self.led_count = mask_disposition.led_number # Number of LED pixels.
        raspi_pin = 18 # GPIO pin connected to the pixels (18 uses PWM!).
        led_freq_hz = 800000  # LED signal frequency in hertz (usually 800khz)
        led_dma = 10      # DMA channel to use for generating signal (try 10)
        led_brightness = int(brightness * 255.0)      # Set to 0 for darkest and 255 for brightest
        led_invert = False   # True to invert the signal (when using NPN transistor level shift)
        led_channel = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
        self.strip = Adafruit_NeoPixel(self.led_count, raspi_pin, led_freq_hz, led_dma, led_invert, led_brightness, led_channel)
        self.strip.begin()
        
    def display_image(formatted_img):
        for i in range(self.height):
            for j in range(self.width):
                position = self.disposition[i,j]
                if position != -1:
                    rgb = formatted_img[i,j]
                    self.strip.setPixelColor(position, Color(rgb[0],rgb[1],rgb[2]))
        self.show()
        

    def clear(col = BLACK):
        for i in range(self.led_count):
            self.strip.setPixelColor(i, col)
        self.show()
    
    def show():
        self.strip.show()
    
def main_func(led_strip):
    led_strip.clear(RED)
    time.sleep(1000.0)
    led_strip.clear(GREEN)
    time.sleep(1000.0)
    led_strip.clear(BLUE)
    time.sleep(1000.0)
    
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
    
    print ('Initialization...')
    
    rec = Rectangle(0,0,17, 37)
    maskdisp = MaskDisposition("../mapping/mask_mapping.xlsx", rec)
    strip = LedStrip(maskdisp, 1.0)
    
    print ('Done.')
    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        strip.clear()
        print ('Entering main loop...')
        while True:
            main_func(strip)

    except KeyboardInterrupt:
        if args.clear:
            strip.clear()

