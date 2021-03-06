#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 20:05:51 2019

@author: ext-poulter_b
"""

class XASRawData:
    
    _defaults = "Izero_pump_total",
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
    "Energy"
        
    _default_value = None
    
    def __init__(self, **kwargs):

        self.__dict__.update(dict.fromkeys(self._defaults, self._default_value))
        self.__dict__.update(kwargs)
        
    def changeValue(self, **kwargs):
        self.__dict__.update(kwargs)