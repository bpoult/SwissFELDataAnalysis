#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 00:01:16 2021

@author: ext-poulter_b
"""

from common.LoadData import load_data
import pickle
import ProcessedDataClass as PDC
import math
import numpy as np
import time
import matplotlib.pyplot as plt


name_base = "XES_2842.0eV_10ps"

save_DIR = "/das/work/p17/p17983/SwissFEL19DA/PostExperiment/Ben/Processed/JF_incl/XES/10ps/"
name = name_base

roi = 2


with open(save_DIR + name + "/" + "rixsprodata_roi" + str(roi) + ".pkl", "rb") as f:
    pro_data = pickle.load(f)


XES_2d_on = np.mean(pro_data.XES_on_2d_array,0)
XES_2d_off = np.mean(pro_data.XES_off_2d_array,0)
plt.figure()
plt.imshow(XES_2d_on)
max_array = [np.max(XES_2d_off[i,:]) for i in range(0,XES_2d_off.shape[0])]


max_indecies = np.squeeze(np.asarray([np.where(np.isclose(XES_2d_off[i,:],max_array[i])) for i in range(0,XES_2d_off.shape[0])]))

new_array = []
for i in range(0,len(max_indecies)):
    if max_indecies[i].shape[0] > 1:
        new_array.append(0)
        continue
    new_array.append(max_indecies[i])

plt.figure()
plt.plot(range(41,79),new_array[41:79])
plt.plot(range(99,135),new_array[99:135])

x = list(range(41,79)) + list(range(99,135))
y = new_array[41:79] + new_array[99:135]

fit_param_2 = np.polyfit(x,y,2)

fit = []
for i in range(0,XES_2d_off.shape[0]):
#    val = a*test4[i]**2 + b*test4[i] +c
    fit.append(fit_param_2[0]*i**2 + fit_param_2[1]*i +fit_param_2[2])

plt.plot(fit)

shift = np.squeeze(np.int64(fit-np.min(fit)))

#new_map = np.zeros((XES_2d_off.shape[0],XES_2d_off.shape[1]))
for i in range(0,XES_2d_off.shape[0]):
    if i is 0:
        new_map = np.append(XES_2d_off[i,shift[i]:-1],np.zeros(shift[i]+1))
    else:
        new_map = np.vstack((new_map,np.append(XES_2d_off[i,shift[i]:-1],np.zeros(shift[i]+1))))
plt.figure()
plt.imshow(XES_2d_off[40:140,40:100])
plt.figure()
plt.imshow(new_map[40:140,40:100])

