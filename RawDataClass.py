#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 20:05:51 2019

@author: ext-poulter_b
"""

class RawData:
    
    _defaults = ("Izero_pump_total",
    "Izero_unpump_total",\
    "Izero2_pump_total",\
    "Izero2_unpump_total",\
    "Izero3_pump_total",\
    "Izero3_unpump_total",\
    "Izero4_pump_total",\
    "Izero4_unpump_total",\
    "pulseIDs_pump",\
    "pulseIDs_unpump",\
    "delay_pump",\
    "delay_SH_pump",\
    "delay_NPP_pump",\
    "Laser_Diode_pump",\
    "Laser_refDiode_pump",\
    "Laser_diag_pump",\
    "PALM_pump",\
    "PALM_unpump",\
    "PALM_eTOF_pump",\
    "PALM_eTOF_unpump",\
    "PALM_drift_pump",\
    "PALM_drift_unpump",\
    "BAM_pump",\
    "BAM_unpump",\
    "waveplate",\
    "DataFluo_pump_total",\
    "DataFluo_unpump_total",\
    "IzeroMedian",\
    "IzeroSTD",\
    "Energy")
        
    _default_value = None
    
    def __init__(self, **kwargs):

        self.__dict__.update(dict.fromkeys(self._defaults, self._default_value))
        self.__dict__.update(kwargs)
        
    def changeValue(self, **kwargs):
        self.__dict__.update(kwargs)
        
    def getKeys(self):
        return self.__dict__.keys()
        
    def makeRIXS(self, cropped_DIR, BS_DIR, save_DIR, name, roi, numstds=4.5, minIzero=0.01, lin_filter=0.025, boot_choice = False, boot_number = 10):
        
        from RIXS import MakeRIXS
        rixsprodata = MakeRIXS.makeRIXS(self, cropped_DIR, BS_DIR, save_DIR, name, roi, numstds, minIzero, lin_filter, boot_choice, boot_number)
        
        return rixsprodata
    