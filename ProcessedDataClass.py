#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 20:39:35 2019

@author: ext-poulter_b
"""

class XASProData:
    
    _defaults = "Izero_pump_total",
    "Izero_unpump_total"\
    ,"DataFluo_pump_total",\
    "DataFluo_unpump_total",\
    "IzeroMedian","IzeroSTD",\
    "Energy"
        
        
    _default_value = None
    
    def __init__(self, **kwargs):

        self.__dict__.update(dict.fromkeys(self._defaults, self._default_value))
        self.__dict__.update(kwargs)
        
    def changeValue(self, **kwargs):
        self.__dict__.update(kwargs)