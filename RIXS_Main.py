#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 22:50:03 2020

@author: ext-liekhussc_c
"""

from common.LoadData import load_data
import pickle
import ProcessedDataClass as PDC
import math
import numpy as np
import time
import matplotlib.pyplot as plt

name_base = "RuDimerCl_monoscan_0p6ps_"
#name_base = "RuDimerACN_monoscan_10ps_"
#name_base = "RuDimerACN_monoscan_0p6ps_"
#name_base = "XES_RuDimerCl_2842.0eV_10ps"
#name_base = "RuBpy3_monoscan_"

name_numbers = [1,2,3,4,5,6,7,8,10,11,12]
#name_numbers = [2,3,4,5,8,10,12,13,14,15,16,17,18]
#name_numbers = [16,17,18,20]
#name_numbers = [10,11,14]

# Use these for RIXS
scan_DIR = "/sf/alvra/data/p17983/raw/scan_data/"
info_DIR = "/sf/alvra/data/p17983/res/scan_info/"
cropped_DIR = '/das/work/p17/p17983/cropped_data/scan_data/'
BS_DIR = "/sf/alvra/data/p17983/raw/scan_data/" 

# Use these for XES
#cropped_DIR = '/das/work/p17/p17983/cropped_data/' + name_base + '/'
#BS_DIR = "/sf/alvra/data/p17983/raw/" 
#scan_DIR = "/sf/alvra/data/p17983/raw/"

#save_DIR = "/das/work/p17/p17983/SwissFEL19DA/PostExperiment/Chelsea/Data/RuCl/"
save_DIR = "/das/work/p17/p17983/SwissFEL19DA/PostExperiment/Ben/Processed/Bootstrapped/RIXS/RuDimerCl_600fs/"
#save_DIR = "/das/work/p17/p17983/SwissFEL19DA/PostExperiment/Chelsea/Data/RuACN/"
#save_DIR = "/das/work/p17/p17983/SwissFEL19DA/PostExperiment/Chelsea/Data/RuBpy3/"

input_info = True #set to True if it is energy scan, set to array of file numbers if it is an emission scan
#input_info = list(range(548,619))
roi = 2
#name_numbers = [0];

reload_raw = False
reload_pro = True

#Filter settings
numstds = 4.5
minIzero = 0.01
lin_filter = 0.025

#Boot
boot_choice = True
boot_number = 50

#Combine
combine = False

print('___________________________________________________________')
print('start rawdata')
print('___________________________________________________________')



start_time = time.time()

raw_datas = []

for name_number in name_numbers:

    
    name = name_base + f'{name_number:03}' # RIXS

#    name = name_base #+ f'{name_number:03}' # XES

    
    if reload_raw:
        raw_data = load_data(scan_DIR, info_DIR, name, input_info, save_DIR)
    else:
        with open(save_DIR + name + "/" + "rawdata.pkl", "rb") as f:
            raw_data = pickle.load(f)
            
    raw_datas = raw_datas + [raw_data]
        
    
    
print('___________________________________________________________')
print('start prodata')
print('___________________________________________________________')



pro_data = PDC.RIXSProData()

for name_number, raw_data in zip(name_numbers, raw_datas):
    
    name = name_base + f'{name_number:03}'
#    name = name_base
    if combine:
        if reload_pro:
           pro_data_new = raw_data.makeRIXS(input_info,cropped_DIR, BS_DIR, save_DIR, name, roi, numstds, minIzero, lin_filter, boot_choice, boot_number)
        else:
            with open(save_DIR + name + "/" + "rixsprodata_roi" + str(roi) + ".pkl", "rb") as f:
                pro_data_new = pickle.load(f)
    
        try:
            
            print(pro_data_new.Energy)
    
        except:
            pass
        print(save_DIR + name + "/" + "rixsprodata_roi" + str(roi) + ".pkl")
        print(pro_data.Energy)
            
        pro_data.combine(pro_data_new)
        if boot_choice:
            pro_data.changeValue(RIXS_map_pumped_err = np.sqrt(pro_data.RIXS_map_pumped_err)/len(name_numbers), \
                         RIXS_map_unpumped_err = np.sqrt(pro_data.RIXS_map_unpumped_err)/len(name_numbers))

    else:
        if reload_pro:
           pro_data = raw_data.makeRIXS(input_info, cropped_DIR, BS_DIR, save_DIR, name, roi, numstds, minIzero, lin_filter, boot_choice, boot_number)
        else:
            with open(save_DIR + name + "/" + "rixsprodata_roi" + str(roi) + ".pkl", "rb") as f:
                pro_data = pickle.load(f)



print('___________________________________________________________')
print('start plotting')
print('___________________________________________________________')


strname = [f'{x:03}' for x in name_numbers]

pro_data.plot(name_base + ' ,'.join(strname),[2838,2842],[25,45])

print('end time')

print(time.time()-start_time)