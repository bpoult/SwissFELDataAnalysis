#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 23:52:59 2019

@author: ext-poulter_b
"""
import sys
sys.path.append("..")
import numpy as np
import os
from matplotlib import pyplot as plt
import pickle
from XES.GetXES import get_xes_pumped
import common.ProcessedDataClass as PDC 


RUN_FROM_SCRATCH = True
ROI = 2

rixsprodata = PDC.RIXSProData()

scannum = [16]
NAME = "RuDimerACN_monoscan_0p6ps_0"
scan = NAME + '%02d' % scannum[0]
LOADDIR = "/das/work/p17/p17983/SwissFEL19DA/PostExperiment/Chelsea/Data/RuDimerACN/" + scan + "/"
SAVEDIR = "/das/work/p17/p17983/SwissFEL19DA/PostExperiment/Chelsea/Data/RuDimerACN/" + scan + "roi2/"

if not os.path.isdir(SAVEDIR):
    os.mkdir(SAVEDIR)
    
with open(LOADDIR + "rawdata.pkl", "rb") as f:
    rawdata = pickle.load(f)

exists = os.path.isfile(SAVEDIR + 'rixsprodata.pkl')
if (not exists or RUN_FROM_SCRATCH):

    for jj in range(len(scannum)):
        fileNAME_base = NAME + '%02d' % scannum[jj] + "_step00"
        scan_NAME = NAME + '%02d' % scannum[jj]
        DIR = '/das/work/p17/p17983/cropped_data/scan_data/' + scan_NAME + "/"
        DIRBS = "/sf/alvra/data/p17983/raw/scan_data/" + scan_NAME + "/"
        numsteps = len(rawdata.Energy)

        for ii in range(numsteps):
            XES_on, XES_off,FilterParameters = \
                get_xes_pumped(fileNAME_base + '%02d' % (ii+0),rawdata,DIR,DIRBS,ROI,True,ii)
            

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
        rixsprodata.changeValue(RIXS_map_pumped=RIXS_on_01, RIXS_map_unpumped = RIXS_off_01,
                                FilterParameters=FilterParameters)
        with open(SAVEDIR + "rixsprodata.pkl", "wb") as f:
            pickle.dump(rixsprodata, f)
elif exists:
    with open(SAVEDIR + "rixsprodata.pkl", "rb") as f:
        rixsprodata = pickle.load(f)

RIXSpumped = np.asarray(rixsprodata.RIXS_map_pumped, dtype=np.float32)
RIXSunpumped = np.asarray(rixsprodata.RIXS_map_unpumped, dtype=np.float32)

X,Y = np.meshgrid(np.linspace(0,RIXSpumped.shape[1],RIXSpumped.shape[1]+1),rawdata.Energy)
plt.subplot(2,1,1)
plt.pcolor(X,Y,rixsprodata.RIXS_map_pumped, vmax = 0.1)
plt.colorbar()
plt.xlabel('JF pixel')
plt.ylabel('Mono Energy (eV)')
plt.title('scannum ' + str(scannum) + ' on')
plt.tight_layout()

X,Y = np.meshgrid(np.linspace(0,RIXSunpumped.shape[1],RIXSunpumped.shape[1]+1),rawdata.Energy)
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






