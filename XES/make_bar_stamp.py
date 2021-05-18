#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 00:06:00 2019

@author: ext-poulter_b
"""
import numpy as np

def make_bar_stamp(dimension_x, dimension_y):

    X,Y = np.meshgrid(np.linspace(0,dimension_x-1,dimension_x),np.linspace(0,dimension_y-1,dimension_y))

    Z = np.zeros([dimension_y,dimension_x])+1

    condition = np.logical_and(Y<260, Y>260)
    Z[condition] = 0
    
    Z[Y>320] = 0
    Z[Y < 180] = 0

    condition = np.logical_not(np.logical_and(X<200, X>130))
    Z[condition] = 0
    
    return Z