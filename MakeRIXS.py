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
scannum = [1]
name = "RuDimerCl_monoscan_0"
scan = "RuDimerCl_monoscan_0"+ '%02d' % scannum[0]
loadDir = "/das/work/p17/p17983/SwissFEL19DA/PostExperiment/Ben/Processed/RuDimerACN/Kinetic_Traces" + scan + "/"
saveDir = "/das/work/p17/p17983/SwissFEL19DA/PostExperiment/Ben/Processed/RuDimerACN/Kinetic_Traces/Emission" + scan + "/"
if not os.path.isdir(saveDir):
    os.mkdir(saveDir)
    
with open(loadDir + "xasrawdata.pkl", "rb") as f:
    xasrawdata = pickle.load(f)

exists = os.path.isfile(saveDir + 'rixsprodata.pkl')
if not exists:

    for jj in range(len(scannum)):
        filename_base = name + '%02d' % scannum[jj] + "_step00"
        scan_name = name + '%02d' % scannum[jj]
        DIR = '/das/work/p17/p17983/cropped_data/scan_data/' + scan_name + "/"
        DIRBS = "/sf/alvra/data/p17983/raw/scan_data/" + scan_name + "/"
        numsteps = len(xasrawdata.Energy)

        for ii in range(numsteps):
            XES_on, XES_off = \
                get_xes_pumped(filename_base + '%02d' % (ii+0),xasrawdata,DIR, DIRBS,2,True,ii)
            

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
        with open(saveDir + "rixsprodata.pkl", "wb") as f:
            pickle.dump(rixsprodata, f)
elif exists:
    with open(saveDir + "rixsprodata.pkl", "rb") as f:
        rixsprodata = pickle.load(f)

RIXSpumped = np.asarray(rixsprodata.RIXS_map_pumped, dtype=np.float32)
RIXSunpumped = np.asarray(rixsprodata.RIXS_map_unpumped, dtype=np.float32)

X,Y = np.meshgrid(np.linspace(0,RIXSpumped.shape[1],RIXSpumped.shape[1]+1),xasrawdata.Energy)
plt.subplot(2,1,1)
plt.pcolor(X,Y,rixsprodata.RIXS_map_pumped, vmax = 0.1)
plt.colorbar()
plt.xlabel('JF pixel')
plt.ylabel('Mono Energy (eV)')
plt.title('scannum ' + str(scannum) + ' on')
plt.tight_layout()

X,Y = np.meshgrid(np.linspace(0,RIXSunpumped.shape[1],RIXSunpumped.shape[1]+1),xasrawdata.Energy)
plt.figure()
plt.subplot(2,1,1)
plt.pcolor(X,Y,rixsprodata.RIXS_map_unpumped, vmax = 0.1)
plt.colorbar()
plt.xlabel('JF pixel')
plt.ylabel('Mono Energy (eV)')
plt.title('scannum ' + str(scannum) + ' off')
plt.tight_layout()

#plt.figure()
#x = np.linspace(0,RIXS_on_01.shape[1],RIXS_on_01.shape[1])
#plt.plot(x,rixsprodata.RIXS_map_pumped[21,:])
#plt.plot(x,rixsprodata.RIXS_map_unpumped[21,:])
#plt.show()






