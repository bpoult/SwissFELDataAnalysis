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
name = "2900eV_Rubpy3_pink_Cl3"
loadDir = "/das/work/p17/p17983/SwissFEL19DA/PostExperiment/Ben/Processed/RuBpy3/XES/Calibration/" + name + "/"
saveDir = "/das/work/p17/p17983/SwissFEL19DA/PostExperiment/Ben/Processed/RuBpy3/XES/Calibration/" + name + "/roi2/"
if not os.path.isdir(saveDir):
    os.mkdir(saveDir)
#    
#with open(loadDir + "xasrawdata.pkl", "rb") as f:
#    xasrawdata = pickle.load(f)
    
filename_base = name + '%02d' % scannum[0] + "_step00"
scan_name = name + '%02d' % scannum[0]
DIR = '/das/work/p17/p17983/cropped_data/'+name +'/'
DIRBS = "/sf/alvra/data/p17983/raw/"
#numsteps = len(xasrawdata.Energy)

#images,pulse_ids = \
#    load_JF_data(DIRBS + name+ '/run_000417' + ".JF02T09V02.h5", nshots=None)

new = images.copy()

new[images<2]=0
new[images>6]=0

images_sum=np.sum(new,axis=0)/new.shape[0]
plt.figure()
plt.plot(np.sum(images_sum,axis=0))
#    
#stamp = make_bar_stamp(on_new.shape[1],on_new.shape[0])
#
#images_on[images_on < 0] = 0
#
#images_sum=np.sum(on_new,axis=0)/on_new.shape[0]
#
X, Y = np.meshgrid(np.linspace(0, new.shape[2], new.shape[2] ),\
                   np.linspace(0, new.shape[1], new.shape[1] ))
plt.figure()
plt.subplot(2, 1, 1)
plt.pcolor(X, Y, images_sum, vmax=0.005)
plt.colorbar()
plt.xlabel('JF pixel')
plt.ylabel('Mono Energy (eV)')
plt.title('DimerACN RIXS unpumped 10ps')
plt.tight_layout()

#plt.figure()
#plt.plot(np.sum(images_sum[:,140:155],axis=0))
#
#plt.figure()
#plt.plot(np.sum(XES_on,axis=0))
#plt.plot(stamp*images.sum(axis=0)/images.shape[0])
    
#plt.figure()
#plt.plot(stamp*imagesfinal.sum(axis=0)/imagesfinal.shape[0])
    
    
#imagescop=images.copy()
#imagescop[images<2]=0
#imagescop[images>3]=0
#imagescop[:,0:205,:]=0
#imagescop[:,350:512,:]=0
#imagescop[:,:,0:160]=0
#imagescop[:,:,200:300]=0
#plt.plot(imagescop.sum(axis=0).transpose()/imagescop.shape[0])  


#emphotons = imagescop.sum(axis=0)
#emphotons = emphotons.sum(axis=0)
#emphotons = emphotons.sum(axis=0)
#print(emphotons)
    
    
    