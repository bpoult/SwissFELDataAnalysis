#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 23:52:59 2019

@author: ext-poulter_b
"""
import numpy as np
from .load_JF import load_JF_cropped_wids
from .make_bar_stamp import make_bar_stamp
from common.Filter import Filtering
import random


def boot_xes(images_on, images_off, condPump, condUnPump):
        
    images_good_on = np.empty(np.shape(images_on))
    images_good_off = np.empty(np.shape(images_off))
    condFinalPump = np.empty(np.shape(condPump), dtype=bool)
    condFinalUnPump = np.empty(np.shape(condUnPump), dtype=bool)
    
    
    num = condPump.size
    
    for jj in range(num):
        
        index = random.randint(0,num-1)
        images_good_on[jj,:,:] = images_on[index,:,:]
        condFinalPump[jj] = condPump[index]

    num = condUnPump.size
    
    for jj in range(num):
        
        index = random.randint(0,num-1)
        images_good_off[jj,:,:] = images_off[index,:,:]
        condFinalUnPump[jj] = condUnPump[index]

        
    return images_good_on, images_good_off, condFinalPump, condFinalUnPump


def apply_filter(images_good_on, images_good_off, condFinalPump, condFinalUnPump, ynstamp,boot_choice):
    
    images_good_on = images_good_on[condFinalPump]
    images_good_off = images_good_off[condFinalUnPump]
    
    image_threshold = 2
    hot_pixel = 6

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
    XES_on_2d = XES_on[175:350,100:250]
    XES_off_2d = XES_off[175:350,100:250]
    
    shift = [28, 28, 27, 27, 26, 25, 25, 24, 24, 23, 22, 22, 21, 21, 20, 20, 19,
       19, 18, 18, 17, 17, 16, 16, 15, 15, 14, 14, 13, 13, 12, 12, 12, 11,
       11, 10, 10, 10,  9,  9,  8,  8,  8,  7,  7,  7,  6,  6,  6,  6,  5,
        5,  5,  4,  4,  4,  4,  3,  3,  3,  3,  3,  2,  2,  2,  2,  2,  1,
        1,  1,  1,  1,  1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,
        2,  3,  3,  3,  3,  4,  4,  4,  4,  5,  5,  5,  5,  6,  6,  6,  7,
        7,  7,  8,  8,  8,  9,  9,  9, 10, 10, 11, 11, 11, 12, 12, 13, 13,
       13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18, 19, 19, 20, 20, 21, 21,
       22, 23, 23, 24, 24]
    # This is from the bend correction script. Using RuDimerACN XES_2842.0eV_10ps for the fit
    
    for i in range(0,XES_off_2d.shape[0]):
        if i is 0:
            new_map_on = np.append(XES_on_2d[i,shift[i]:-1],np.zeros(shift[i]+1))
            new_map_off = np.append(XES_off_2d[i,shift[i]:-1],np.zeros(shift[i]+1))

        else:
            new_map_on = np.vstack((new_map_on,np.append(XES_on_2d[i,shift[i]:-1],np.zeros(shift[i]+1))))
            new_map_off = np.vstack((new_map_off,np.append(XES_off_2d[i,shift[i]:-1],np.zeros(shift[i]+1))))
    XES_on_2d = new_map_on
    XES_off_2d = new_map_off
    
    XES_on = XES_on_2d.sum(axis=0)
    XES_off = XES_off_2d.sum(axis=0)
    return XES_on, XES_off, XES_on_2d, XES_off_2d


def get_xes_pumped(filename, xasrawdata, DIR, DIRBS, roi, ynstamp, ii, numstds=4.5, minIzero=0.01, lin_filter=0.025, boot_choice = False, boot_number = 10):
    print(DIR + filename + ".JF02T09V02crop.h5")
    images_on, images_off = \
        load_JF_cropped_wids(DIR + filename + ".JF02T09V02crop.h5", roi, xasrawdata.pulseIDs_pump[ii])
    
    condPump, condUnPump, FilterParameters, Izero_pump, Izero_unpump, DataFluo_pump, DataFluo_unpump = Filtering(ii, xasrawdata, numstds, minIzero, lin_filter)
    
    TFY_on = np.mean(DataFluo_pump[condPump]/Izero_pump[condPump],0)
    TFY_off = np.mean(DataFluo_unpump[condUnPump]/Izero_unpump[condUnPump],0)

    
    if boot_choice:
        
        for kk in range(boot_number):
            
            images_good_on_kk, images_good_off_kk, condFinalPump_kk, condFinalUnPump_kk \
            = boot_xes(images_on, images_off, condPump, condUnPump)
            
            XES_on_kk, XES_off_kk,XES_on_2d_kk, XES_off_2d_kk = apply_filter(images_good_on_kk, images_good_off_kk, condFinalPump_kk, condFinalUnPump_kk, ynstamp,boot_choice)
            

            
            if kk == 0:
                XES_on_array = np.empty((XES_on_kk.shape[0], boot_number))
                XES_off_array = np.empty((XES_off_kk.shape[0], boot_number))
                XES_on_2d_array = np.empty((XES_on_2d_kk.shape[0],XES_on_2d_kk.shape[1], boot_number))
                XES_off_2d_array = np.empty((XES_off_2d_kk.shape[0],XES_off_2d_kk.shape[1], boot_number))

            
            XES_on_array[:,kk] = XES_on_kk
            XES_off_array[:,kk] = XES_off_kk
            XES_on_2d_array[:,:,kk] = XES_on_2d_kk
            XES_off_2d_array[:,:,kk] = XES_off_2d_kk

            
        XES_on = np.mean(XES_on_array, axis=1)
        XES_off = np.mean(XES_off_array, axis=1)
        
        XES_on_2d = np.mean(XES_on_2d_array,axis=2)
        XES_off_2d = np.mean(XES_off_2d_array,axis=2)

        XES_on_err = np.std(XES_on_array, axis=1)
        XES_off_err = np.std(XES_off_array, axis=1)
        
        
    else:
        
        images_good_on = images_on
        images_good_off = images_off
        condFinalPump = condPump
        condFinalUnPump = condUnPump

        XES_on, XES_off, XES_on_2d, XES_off_2d = apply_filter(images_good_on, images_good_off, condFinalPump, condFinalUnPump, ynstamp,boot_choice)
    
    if boot_choice:
        
        return XES_on, XES_off, XES_on_err, XES_off_err,XES_on_2d,XES_off_2d, TFY_on, TFY_off, FilterParameters,
        
    else:
        
        return XES_on, XES_off, TFY_on, TFY_off, FilterParameters, XES_on_2d, XES_off_2d


