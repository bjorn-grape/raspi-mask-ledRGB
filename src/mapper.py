#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd


class Rectangle():
    def __init__(self, origin_x, origin_y, width, height):
        self.X = origin_x
        self.Y = origin_y
        self.width = width
        self.height = height


def from_mapping_file_to_array(file, ROI):
    dt = pd.read_excel(file)
    all_column_names = [ "Line "+ i for i in range(ROI.origin_x, ROI.origin_x + ROI.width)]
    dt = dt[all_column_names]
    dt = dt[ROI.origin_y :ROI.origin_y  + ROI.height]
    
    return dt
    


class MaskDisposition():
    
    def __init__(self, mapping_file, rectangle_of_interest):
        self.ROI = rectangle_of_interest;
        self.disposition = from_mapping_file_to_array(mapping_file, self.ROI)
        
