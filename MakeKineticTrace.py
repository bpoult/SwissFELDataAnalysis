#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 19:47:10 2019

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


# Set the scan name and the directories of the scan and its json file
scan_name = "RuDimerACN_timescan_011"

saveDir = "/das/work/p17/p17983/SwissFEL19DA/PostExperiment/Ben/Processed/RuDimerACN/Kinetic_Traces/" + scan_name + "/"
if not os.path.isdir(saveDir):
    os.mkdir(saveDir)

exists = os.path.isfile(saveDir + 'xasrawdata.pkl')
if not exists:
    xasrawdata = LoadData(scan_name,True)
    with open(saveDir + "xasrawdata.pkl", "wb") as f:
        pickle.dump(xasrawdata, f)
        
        
elif exists:
    with open(saveDir + "xasrawdata.pkl", "rb") as f:
        xasrawdata = pickle.load(f)

delay_mm = np.empty(0)
for i in range(0,len(xasrawdata.delay_SH_pump)):
    delay = [x for x in xasrawdata.delay_SH_pump[i] if x>0]
    delay_mm = np.append(delay_mm, np.mean(delay[i]))

time_zero_mm = 156.3276
delay_ps = 1e12*(delay_mm - time_zero_mm)*2*1e-3/(3e8)

delays = np.array(delay_ps)


saveProData = True
loadProData = False

xasprodata = FilterData(xasrawdata,True)

plt.figure()
plt.plot(delays, xasprodata.DataFluo_pump_norm_total,label='Pumped')
plt.plot(delays, xasprodata.DataFluo_unpump_norm_total,label='UnPumped')
plt.xlabel('Time (ps)')
plt.ylabel('absorption')
plt.title(scan_name)
plt.legend()

#plt.figure()
#plt.plot(delays, xasprodata.DataFluo_unpump_norm_total-xasprodata.DataFluo_pump_norm_total,label='UnPump-Pump')


xasprodata.changeValue(delays=delays)

if saveProData is True:
        with open(saveDir + "xasprodata.pkl", "wb") as f:
            pickle.dump(xasprodata, f)
            
if loadProData is True:
    with open(saveDir + "xasprodata.pkl", "rb") as f:
        x = pickle.load(f)