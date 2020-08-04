#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 23:52:59 2019

@author: ext-poulter_b
"""

import numpy as np
import os
import pickle
from XES.GetXES import get_xes_pumped
import ProcessedDataClass as PDC 


def makeRIXS(rawdata, cropped_DIR, BS_DIR, save_DIR, name, roi):
    
    rixsprodata = PDC.RIXSProData()
    
    BS_DIR = BS_DIR + name + "/"
    cropped_DIR = cropped_DIR + name + "/"
    save_DIR = save_DIR + name + "/"

    filename_base = name + "_step00"

    numsteps = len(rawdata.Energy)

    print('dir')
    print(cropped_DIR)
    print(BS_DIR)

    for ii in range(numsteps):
        print(filename_base + '%02d' % (ii+0))
        XES_on, XES_off,FilterParameters = \
            get_xes_pumped(filename_base + '%02d' % (ii+0), rawdata, cropped_DIR, BS_DIR, roi, True, ii)
        

        if ii == 0:
            rixs_on_01 = XES_on.sum(axis=0)
            rixs_off_01 = XES_off.sum(axis=0)
        else:
            rixs_on_01 = np.vstack((rixs_on_01,XES_on.sum(axis=0)))
            rixs_off_01 = np.vstack((rixs_off_01,XES_off.sum(axis=0)))
        
        
    
    
    rixsprodata.changeValue(RIXS_map_pumped=rixs_on_01, RIXS_map_unpumped = rixs_off_01,
                            FilterParameters = FilterParameters, Energy = rawdata.Energy)
    
    rixsprodata.croppedfile = cropped_DIR
    rixsprodata.bsfile = BS_DIR
    
    if not os.path.isdir(save_DIR):
        os.mkdir(save_DIR)
        
    with open(save_DIR + "rixsprodata_roi" + str(roi) + ".pkl", "wb") as f:
        pickle.dump(rixsprodata, f)

    
    return rixsprodata


