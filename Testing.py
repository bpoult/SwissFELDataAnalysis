#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 22:18:38 2019

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
from make_bar_stamp import make_bar_stamp
from GetXES import get_xes_pumped
import ProcessedDataClass as PDC 


rixsprodata = PDC.RIXSProData()
scannum = [7]
name = "RuDimerACN_monoscan_0p6ps_0"
scan = "RuDimerACN_monoscan_0p6ps_0"+ '%02d' % scannum[0]
loadDir = "/das/work/p17/p17983/SwissFEL19DA/PostExperiment/Ben/Processed/RuDimerACN/TFY/600fs/" + scan + "/"
saveDir = "/das/work/p17/p17983/SwissFEL19DA/PostExperiment/Ben/Processed/RuDimerACN/RIXS/600fs/" + scan + "/"
if not os.path.isdir(saveDir):
    os.mkdir(saveDir)
    
with open(loadDir + "xasrawdata.pkl", "rb") as f:
    xasrawdata = pickle.load(f)
    

filename_base = name + '%02d' % scannum[0] + "_step00"
scan_name = name + '%02d' % scannum[0]
DIR = '/das/work/p17/p17983/cropped_data/scan_data/' + scan_name + "/"
DIRBS = "/sf/alvra/data/p17983/raw/scan_data/" + scan_name + "/"
numsteps = len(xasrawdata.Energy)

XES_on, XES_off,images,imagesfinal = \
get_xes_pumped(filename_base + '%02d' % (30),xasrawdata,DIR, DIRBS,2,True,1)
    
stamp = make_bar_stamp(XES_on.shape[1],XES_on.shape[0])

testing=images[0:2,:,:].flatten()
    
#plt.plot(stamp*images.sum(axis=0)/images.shape[0])
    
#plt.figure()
#plt.plot(stamp*imagesfinal.sum(axis=0)/imagesfinal.shape[0])
    
    
imagescop=images.copy()
imagescop[images<2]=0
imagescop[images>3]=0
imagescop[:,0:205,:]=0
imagescop[:,350:512,:]=0
imagescop[:,:,0:160]=0
imagescop[:,:,200:300]=0
plt.plot(imagescop.sum(axis=0).transpose()/imagescop.shape[0])  


emphotons = imagescop.sum(axis=0)
emphotons = emphotons.sum(axis=0)
emphotons = emphotons.sum(axis=0)
print(emphotons)
    
    
    