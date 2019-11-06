#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 23:52:59 2019

@author: ext-poulter_b
"""
import sys
sys.path.insert(0, '/das/work/p17/p17983/SwissFEL19DA/PostExperiment/Ben/jfut/')
import jungfrau_utils as jf
sys.path.insert(0, '/das/work/p17/p17983/')
import numpy as np
import json
import os
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from alvra_tools.load_data import *
from alvra_tools.channels import *
from alvra_tools.utils import errfunc_sigma, errfunc_fwhm
from LoadData import LoadData
from Filter import FilterData
import pickle
from GetXES import get_xes_pumped
import ProcessedDataClass as PDC 

rixsprodata = PDC.RIXSProData()

name = "XES_2842pink_Lbeta2_10ps"
loadDir = "/das/work/p17/p17983/SwissFEL19DA/PostExperiment/Ben/Processed/RuDimerACN/XES/10ps/" + name + "/"
saveDir = "/das/work/p17/p17983/SwissFEL19DA/PostExperiment/Ben/Processed/RuDimerACN/XES/10ps/" + name + "/roi1/"
if not os.path.isdir(saveDir):
    os.mkdir(saveDir)
    
with open(loadDir + "xasrawdata.pkl", "rb") as f:
    xasrawdata = pickle.load(f)

exists = os.path.isfile(saveDir + 'xesprodata.pkl')
if not exists:
    print('What are the lower and upper bounds of the XES scans?')
    scannum_low = int(input())
    scannum_high = int(input())
    scannum = range(scannum_low,scannum_high)
    DIR = '/das/work/p17/p17983/cropped_data/' + name + "/"
    DIRBS = "/sf/alvra/data/p17983/raw/" + name + "/"
    numsteps = len(xasrawdata.Energy)
    jj = 0
    for ii in range(numsteps):
        filename_base = 'run_000' + '%02d' % scannum[ii]
        XES_on, XES_off = \
        get_xes_pumped(filename_base,xasrawdata,DIR, DIRBS,1,False,ii)
    


        if ii == 0 & jj == 0:
            rixs_on_01 = XES_on.sum(axis=0)
            rixs_off_01 = XES_off.sum(axis=0)
        else:
            rixs_on_01 = np.vstack((rixs_on_01,XES_on.sum(axis=0)))
            rixs_off_01 = np.vstack((rixs_off_01,XES_off.sum(axis=0)))
            
            
        
    if jj == 0:
        RIXS_on_01 = rixs_on_01
        RIXS_off_01 = rixs_off_01
        
    else:
        
        RIXS_on_01 = RIXS_on_01 + rixs_on_01
        RIXS_off_01 = RIXS_off_01 + rixs_off_01

    save = True
    if save is True:
        rixsprodata.changeValue(RIXS_map_pumped=RIXS_on_01, RIXS_map_unpumped = RIXS_off_01)
        with open(saveDir + "xesprodata.pkl", "wb") as f:
            pickle.dump(rixsprodata, f)
elif exists:
    with open(saveDir + "xesprodata.pkl", "rb") as f:
        rixsprodata = pickle.load(f)

RIXSpumped = np.asarray(rixsprodata.RIXS_map_pumped, dtype=np.float32)
RIXSunpumped = np.asarray(rixsprodata.RIXS_map_unpumped, dtype=np.float32)


XES_on = np.sum(RIXSpumped,axis=0)
XES_off = np.sum(RIXSunpumped,axis=0)
integral_on = np.trapz(XES_on)
integral_off = np.trapz(XES_off)

print(integral_on)
print(integral_off)

XES_on = XES_on.copy()
XES_off = XES_off.copy()*integral_on/integral_off

plt.figure()
plt.plot(XES_on)

plt.figure()
plt.plot(XES_off)

plt.figure()
plt.plot(XES_on-XES_off)



#plt.figure()
#x = np.linspace(0,RIXS_on_01.shape[1],RIXS_on_01.shape[1])
#plt.plot(x,rixsprodata.RIXS_map_pumped[21,:])
#plt.plot(x,rixsprodata.RIXS_map_unpumped[21,:])
#plt.show()






