#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np


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


def from_mapping_file_to_array(file, ROI):
    dt = pd.read_excel(file)
    all_column_names = ["Line "+ str(i) for i in range(ROI.X, ROI.X + ROI.width)]
    dt = dt[all_column_names]
    dt = dt[ROI.Y : ROI.Y  + ROI.height]
    dt = dt.fillna(-1)
    return np.array(dt.values).astype(np.int32)





class MaskDisposition():
    
    def __init__(self, mapping_file, rectangle_of_interest):
        self.ROI = rectangle_of_interest;
        self.disposition = from_mapping_file_to_array(mapping_file, self.ROI)
        # self.fitting_led_index = 
    

def test():        
    rec = Rectangle(0,0,17, 37)
    maskdisp = MaskDisposition("../mapping/mask_mapping.xlsx", rec)
    return maskdisp