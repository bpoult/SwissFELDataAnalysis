#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 23:52:59 2019

@author: ext-poulter_b
"""
import numpy as np
from .load_JF import load_JF_cropped_data_pump
from .make_bar_stamp import make_bar_stamp
from common.Filter import Filtering

def get_xes_pumped(filename,xasrawdata, DIR, DIRBS, roi, ynstamp,ii):
    image_threshold = 2
    hot_pixel = 6
    
    # change the second number to: 50/2 for 1 shot on 1 shot off
    #                            : 50/3 for 2 shots on 1 shot off
    images_off, images_on, pulse_ids_off, pulse_ids_on = \
        load_JF_cropped_data_pump(DIR + filename + ".JF02T09V02crop.h5", roi, 50, 50/2, nshots=None)
    
    condFinalPump, condFinalUnPump,FilterParameters = Filtering(ii,xasrawdata)

    images_good_on = images_on
    images_good_off = images_off

    images_good_on = images_good_on[condFinalPump]
    images_good_off = images_good_off[condFinalUnPump]

    images_thr_on = images_good_on.copy()
    images_thr_on[images_good_on < image_threshold] = 0
    images_thr_on[images_good_on > hot_pixel] = 0
    images_thr_on[np.isnan(images_thr_on)] = 0
    
    images_thr_off = images_good_off.copy()
    images_thr_off[images_good_off < image_threshold] = 0
    images_thr_off[images_good_off > hot_pixel] = 0
    images_thr_off[np.isnan(images_thr_off)] = 0
    
    XES_on = images_thr_on.sum(axis=0)/images_thr_on.shape[0]
    XES_off = images_thr_off.sum(axis=0)/images_thr_off.shape[0]
    
    XES_on[np.isnan(XES_on)] = 0
    XES_off[np.isnan(XES_off)] = 0
    
    stamp = make_bar_stamp(XES_on.shape[1],XES_on.shape[0])
    
    if ynstamp:

        XES_on = XES_on * stamp
        XES_off = XES_off * stamp
            
    return XES_on, XES_off, FilterParameters