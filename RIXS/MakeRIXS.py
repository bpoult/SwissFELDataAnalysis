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


def makeRIXS(rawdata,input_info, cropped_DIR, BS_DIR, save_DIR, name, roi, numstds=4.5, minIzero=0.01, lin_filter=0.025, boot_choice = False, boot_number = 10):
    
    rixsprodata = PDC.RIXSProData()
    
    BS_DIR = BS_DIR + name + "/"
    save_DIR = save_DIR + name + "/"

    filename_base = name + "_step00"
#    filename_base = 'run_000'

    if input_info is True:
        numsteps = len(rawdata.Energy)
        cropped_DIR = cropped_DIR + name + '/'

    else:
        numsteps = len(input_info)

    print('dir')
    print(cropped_DIR)
    print(BS_DIR)

    for ii in range(numsteps):
        if input_info is True:
            print(filename_base + '%02d' % (ii))
            print(cropped_DIR)
            if boot_choice:
                        XES_on, XES_off, XES_on_err, XES_off_err, TFY_on, TFY_off, FilterParameters = \
                            get_xes_pumped(filename_base + '%02d' % (ii), rawdata, cropped_DIR, BS_DIR, roi, True, ii, numstds, minIzero, lin_filter, boot_choice, boot_number)
                        
            else:
                XES_on, XES_off, TFY_on, TFY_off, FilterParameters = \
                    get_xes_pumped(filename_base + '%02d' % (ii), rawdata, cropped_DIR, BS_DIR, roi, True, ii, numstds, minIzero, lin_filter, boot_choice)

        else:
            print(filename_base + '%02d' % (input_info[ii+0]))

            if boot_choice:
                XES_on, XES_off, XES_on_err, XES_off_err, TFY_on, TFY_off, FilterParameters = \
                    get_xes_pumped(filename_base + '%02d' % (input_info[ii+0]), rawdata, cropped_DIR, BS_DIR, roi, True, ii, numstds, minIzero, lin_filter, boot_choice, boot_number)
                
            else:
                XES_on, XES_off, TFY_on, TFY_off, FilterParameters = \
                    get_xes_pumped(filename_base + '%02d' % (input_info[ii+0]), rawdata, cropped_DIR, BS_DIR, roi, True, ii, numstds, minIzero, lin_filter, boot_choice)


        if ii == 0:
            rixs_on = XES_on
            rixs_off = XES_off
            
            if boot_choice:
                rixs_on_err = XES_on_err
                rixs_off_err = XES_off_err
        else:
            rixs_on = np.vstack((rixs_on, XES_on))
            rixs_off = np.vstack((rixs_off, XES_off))
            
            if boot_choice:
                rixs_on_err = np.vstack((rixs_on_err, XES_on_err))
                rixs_off_err = np.vstack((rixs_off_err, XES_off_err))
        
    if boot_choice:
        rixsprodata.changeValue(RIXS_map_pumped = rixs_on, RIXS_map_unpumped = rixs_off, FilterParameters = FilterParameters, \
                            Energy = np.round(rawdata.Energy,1), RIXS_map_pumped_err = rixs_on_err, RIXS_map_unpumped_err = rixs_off_err, TFY_on = TFY_on, TFY_off = TFY_off)
        
    else:
        rixsprodata.changeValue(RIXS_map_pumped = rixs_on, RIXS_map_unpumped = rixs_off, FilterParameters = FilterParameters, Energy = np.round(rawdata.Energy,1), \
                                TFY_on = TFY_on, TFY_off = TFY_off)
    
    rixsprodata.croppedfile = cropped_DIR
    rixsprodata.bsfile = BS_DIR
    
    if not os.path.isdir(save_DIR):
        os.mkdir(save_DIR)
        
    with open(save_DIR + "rixsprodata_roi" + str(roi) + ".pkl", "wb") as f:
        pickle.dump(rixsprodata, f)

    
    return rixsprodata



    