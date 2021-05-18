#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 22:24:10 2020

@author: ext-liekhussc_c
"""

import numpy as np

def makeColorMap(start_map, percent_at_sat):
    
    from matplotlib import cm
    from matplotlib.colors import ListedColormap
   
    number_colors = int(1000*percent_at_sat)
    
    start_colors = cm.get_cmap(start_map, number_colors)
    start_colors = start_colors(np.linspace(0,1,number_colors))
    
    sat_color = np.tile(start_colors[-1], (1000-number_colors,1))
    
    new_colors = np.vstack((start_colors, sat_color))
    
    return ListedColormap(new_colors)


def findJFLimits(RIXS_map):
    
    
    energy_sum = np.sum(RIXS_map,0)
    non_zeros = energy_sum > 0
    indicies = np.linspace(0,RIXS_map.shape[0],RIXS_map.shape[1]+1)
    indicies = indicies[non_zeros]
    
    return (int(indicies[0]), int(indicies[-1]))



def findvmax(RIXS_map_on, RIXS_map_off):
    
    import math
    
    RIXS_max = np.max((np.max(RIXS_map_on), np.max(RIXS_map_off)))
    
    RIXS_max = math.ceil(RIXS_max*1000)/1000
    
    return RIXS_max




def plotRIXS(pro_data, name, energy_cut, JF_cut):
    
    import matplotlib.pyplot as plt
   
    cmap_alt = makeColorMap('viridis', .4)
    
    min_in, max_in = findJFLimits(pro_data.RIXS_map_pumped)
    RIXS_max = findvmax(pro_data.RIXS_map_pumped, pro_data.RIXS_map_unpumped)
    
    
    JF_pixel = np.linspace(0,max_in-min_in-1,max_in-min_in)
    
    plt.figure(figsize = (8,6))    
    X,Y = np.meshgrid(JF_pixel,pro_data.Energy)
    
    RIXS_on = pro_data.RIXS_map_pumped[:,min_in: max_in]
    RIXS_off = pro_data.RIXS_map_unpumped[:,min_in: max_in]
    
    if "RIXS_map_pumped_err" in pro_data.getKeys():
        RIXS_on_err = pro_data.RIXS_map_pumped_err[:,min_in:max_in]
        RIXS_off_err = pro_data.RIXS_map_unpumped_err[:,min_in:max_in]
    
    plt.subplot(2,1,1)
    plt.pcolor(X,Y,RIXS_on, cmap = cmap_alt, vmax = RIXS_max)
    plt.colorbar()
    plt.xlabel('JF pixel')
    plt.ylabel('Mono Energy (eV)')
    plt.title(str(name) + ' on')
    
    plt.subplot(2,1,2)
    plt.pcolor(X,Y,RIXS_off, cmap = cmap_alt, vmax = RIXS_max)
    plt.colorbar()
    plt.xlabel('JF pixel')
    plt.ylabel('Mono Energy (eV)')
    plt.title(str(name) + ' off')
    plt.tight_layout()
    
    
    
    
    energy_slice_cond = (pro_data.Energy > energy_cut[0]) & (pro_data.Energy < energy_cut[1])
    pixel_slice_cond = (JF_pixel > JF_cut[0]) & (JF_pixel < JF_cut[1])
    
    energy_slice_on = np.mean(RIXS_on[energy_slice_cond, :], 0)
    energy_slice_off = np.mean(RIXS_off[energy_slice_cond, :], 0)
    
    pixel_slice_on = np.mean(RIXS_on[:, pixel_slice_cond], 1)
    pixel_slice_off = np.mean(RIXS_off[:, pixel_slice_cond], 1)
    
    if "RIXS_map_pumped_err" in pro_data.getKeys():
        
        energy_slice_on_err = RIXS_on_err[energy_slice_cond, :]
        energy_slice_off_err = RIXS_off_err[energy_slice_cond, :]
        pixel_slice_on_err = RIXS_on_err[:, pixel_slice_cond]
        pixel_slice_off_err = RIXS_off_err[:, pixel_slice_cond]
        
        
        energy_slice_on_err = np.sqrt(np.sum(energy_slice_on_err**2, 0))/len(energy_slice_on_err)
        energy_slice_off_err = np.sqrt(np.sum(energy_slice_off_err**2, 0))/len(energy_slice_off_err)
        pixel_slice_on_err = np.sqrt(np.sum(pixel_slice_on_err**2, 1))/len(pixel_slice_on_err[1,:])
        pixel_slice_off_err = np.sqrt(np.sum(pixel_slice_off_err**2, 1))/len(pixel_slice_off_err[1,:])


    plt.figure()
    
    if "RIXS_map_pumped_err" in pro_data.getKeys():
        plt.errorbar(pro_data.Energy, pixel_slice_on, pixel_slice_on_err, label = 'on')
        plt.errorbar(pro_data.Energy, pixel_slice_off, pixel_slice_off_err, label = 'off')
    
    else:
        plt.plot(pro_data.Energy, pixel_slice_on, label = 'on')
        plt.plot(pro_data.Energy, pixel_slice_off, label = 'off')
        
    plt.xlabel('Mono Energy (eV)')
    plt.title(str(name) + ', pixel range ' + str(JF_cut[0]) + ' to ' + str(JF_cut[1]))
    plt.legend()

    
    plt.figure()
    
    if "RIXS_map_pumped_err" in pro_data.getKeys():
        plt.errorbar(JF_pixel, energy_slice_on, energy_slice_on_err, label = 'on')
        plt.errorbar(JF_pixel, energy_slice_off, energy_slice_off_err, label = 'on')
    
    else:
        plt.plot(JF_pixel, energy_slice_on, label = 'on')
        plt.plot(JF_pixel, energy_slice_off, label = 'off')

    plt.xlabel('JF pixel')
    plt.title(str(name) + ', energy range ' + str(energy_cut[0]) + ' to ' + str(energy_cut[1]))
    plt.legend()
    
    
    """
    plt.figure()
    plt.plot(pro_data.Energy, pro_data.TFY_on, label = 'on')
    plt.plot(pro_data.Energy, pro_data.TFY_off, label = 'off')
    plt.title('TFY')
    """
    
    
    
    
    
    
    
    