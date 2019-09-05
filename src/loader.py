#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 21:36:45 2019

@author: bjorn
"""

import numpy as np
import cv2

class ImageLoader():
    
    def __init__(self, height, width):
        self.storage = {}
        self.height = height
        self.width = width
        
    def load(self, name, path):
        img  = cv2.imread(path)
        correct_dim  = (self.height, self.width, 3)
        if img.shape != correct_dim :
            img = cv2.resize(img, correct_dim) 
        img =  cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.storage[name] = img
        
    def get(self, name):
        return self.storage[name]
    
