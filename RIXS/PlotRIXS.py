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
    indicies = np.linspace(0,RIXS_map.shape[1],RIXS_map.shape[1]+1)
    indicies = indicies[non_zeros]
    
    return (int(indicies[0]), int(indicies[-1]))



def findvmax(RIXS_map_on, RIXS_map_off):
    
    import math
    
    RIXS_max = np.max((np.max(RIXS_map_on), np.max(RIXS_map_off)))
    
    RIXS_max = math.ceil(RIXS_max*1000)/1000
    
    return RIXS_max




def plotRIXS(pro_data, name):
    
    import matplotlib.pyplot as plt
   
    cmap_alt = makeColorMap('viridis', .5)
    
    min_in, max_in = findJFLimits(pro_data.RIXS_map_pumped)
    RIXS_max = findvmax(pro_data.RIXS_map_pumped, pro_data.RIXS_map_unpumped)
    
    
    plt.figure(figsize = (8,6))    
    X,Y = np.meshgrid(np.linspace(0,max_in-min_in-1,max_in-min_in),pro_data.Energy)
    plt.subplot(2,1,1)
    plt.pcolor(X,Y,pro_data.RIXS_map_pumped[:,min_in: max_in], cmap = cmap_alt, vmax = RIXS_max)
    plt.colorbar()
    plt.xlabel('JF pixel')
    plt.ylabel('Mono Energy (eV)')
    plt.title(str(name) + ' on')
    
    X,Y = np.meshgrid(np.linspace(0,max_in-min_in-1,max_in-min_in),pro_data.Energy)
    plt.subplot(2,1,2)
    plt.pcolor(X,Y,pro_data.RIXS_map_unpumped[:,min_in: max_in], cmap = cmap_alt, vmax = RIXS_max)
    plt.colorbar()
    plt.xlabel('JF pixel')
    plt.ylabel('Mono Energy (eV)')
    plt.title(str(name) + ' off')
    plt.tight_layout()
    
    
    #ax = sns.heatmap(X, Y, pro_data.RIXS_map_pumped)

#plt.figure()
#x = np.linspace(0,RIXS_on_01.shape[1],RIXS_on_01.shape[1])
#plt.plot(x,rixsprodata.RIXS_map_pumped[21,:])
#plt.plot(x,rixsprodata.RIXS_map_unpumped[21,:])
#plt.show()