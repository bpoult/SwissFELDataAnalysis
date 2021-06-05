#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 22:45:02 2021

@author: ext-poulter_b
"""
import numpy as np
from common.Filter import Filtering
import random


def boot_xas(TFY_on, TFY_off, condPump, condUnPump):
        
    TFY_good_on = np.empty(np.shape(TFY_on))
    TFY_good_off = np.empty(np.shape(TFY_off))
    condFinalPump = np.empty(np.shape(condPump), dtype=bool)
    condFinalUnPump = np.empty(np.shape(condUnPump), dtype=bool)
    
    
    num = condPump.size
    
    for jj in range(num):
        
        index = random.randint(0,num-1)
        TFY_good_on[jj] = TFY_on[index]
        condFinalPump[jj] = condPump[index]

    num = condUnPump.size
    
    for jj in range(num):
        
        index = random.randint(0,num-1)
        TFY_good_off[jj] = TFY_off[index]
        condFinalUnPump[jj] = condUnPump[index]

        
    return TFY_good_on, TFY_good_off, condFinalPump, condFinalUnPump


def get_xas(filename,xasrawdata,ii,numstds=4.5, minIzero=0.01, lin_filter=0.025, boot_choice = False, boot_number = 10):
    condPump, condUnPump, FilterParameters, Izero_pump, Izero_unpump, DataFluo_pump, DataFluo_unpump = Filtering(ii, xasrawdata, numstds, minIzero, lin_filter)
    
    TFY_on = DataFluo_pump/Izero_pump
    TFY_off = DataFluo_unpump/Izero_unpump

    if boot_choice:
        
        for kk in range(boot_number):
            TFY_good_on_kk, TFY_good_off_kk, condFinalPump_kk_TFY, condFinalUnPump_kk_TFY \
            = boot_xas(TFY_on, TFY_off, condPump, condUnPump)
        
            TFY_on_kk = TFY_good_on_kk[condFinalPump_kk_TFY]
            TFY_off_kk = TFY_good_off_kk[condFinalUnPump_kk_TFY]
            
            if kk ==0:           
                TFY_on_array = np.zeros((1000, boot_number))
                TFY_off_array = np.zeros((1000, boot_number))
                TFY_on_array[TFY_on_array==0]=np.nan
                TFY_off_array[TFY_off_array==0]=np.nan
                
            TFY_on_array[0:len(TFY_on_kk),kk] = TFY_on_kk
            TFY_off_array[0:len(TFY_off_kk),kk] = TFY_off_kk
            
            
            TFY_on = np.nanmean(TFY_on_array, axis=1)
            TFY_off = np.nanmean(TFY_off_array, axis=1)
            TFY_on_err = np.nanstd(TFY_on_array, axis=1)
            TFY_off_err = np.nanstd(TFY_off_array, axis=1)
        
    else:
        TFY_on = TFY_on[condPump]
        TFY_off = TFY_off[condUnPump]
    if boot_choice:
        return TFY_on, TFY_off, TFY_on_err, TFY_off_err, FilterParameters
    else:
        return TFY_on, TFY_off, FilterParameters