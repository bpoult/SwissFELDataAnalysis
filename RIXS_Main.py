#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 22:50:03 2020

@author: ext-liekhussc_c
"""

from common.LoadData import load_data
import pickle

name = "RuBpy3_monoscan_012"
scan_DIR = "/sf/alvra/data/p17983/raw/scan_data/"
info_DIR = "/sf/alvra/data/p17983/res/scan_info/"
save_DIR = "/das/work/p17/p17983/SwissFEL19DA/PostExperiment/Chelsea/Data/RuBpy3/"
input_info = True #set to True if it is energy scan, set to array of file numbers if it is an emission scan
cropped_DIR = '/das/work/p17/p17983/cropped_data/scan_data/'
BS_DIR = "/sf/alvra/data/p17983/raw/scan_data/"
roi = 2

reload_raw = False
reload_pro = False

if reload_raw:
    raw_data = load_data(scan_DIR, info_DIR, name, input_info, save_DIR)
else:
    with open(save_DIR + name + "/" + "rawdata.pkl", "rb") as f:
        raw_data = pickle.load(f)
    
    
    
print('___________________________________________________________')
print('start prodata')
print('___________________________________________________________')





if reload_pro:
    pro_data = raw_data.makeRIXS(cropped_DIR, BS_DIR, save_DIR, name, roi)
else:
    with open(save_DIR + name + "/" + "rixsprodata_roi" + str(roi) + ".pkl", "rb") as f:
        pro_data = pickle.load(f)

pro_data.plot(name)