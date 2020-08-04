#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 20:39:35 2019

@author: ext-poulter_b
"""


class XASProData:
    _defaults = ("Izero_pump_total", \
                "Izero_unpump_total", \
                "DataFluo_pump_total", \
                "DataFluo_unpump_total", \
                "IzeroMedian", \
                "IzeroSTD", \
                "Energy", "delays")

    _default_value = None

    def __init__(self, **kwargs):
        self.__dict__.update(dict.fromkeys(self._defaults, self._default_value))
        self.__dict__.update(kwargs)

    def changeValue(self, **kwargs):
        self.__dict__.update(kwargs)
        
    def getKeys(self):
        print(self.__dict__.keys())


class RIXSProData:
    _defaults = ("RIXS_map_pumped", "RIXS_map_unpumped", \
                "FilterParameters", "Energy")

    _default_value = None

    def __init__(self, **kwargs):
        self.__dict__.update(dict.fromkeys(self._defaults, self._default_value))
        self.__dict__.update(kwargs)

    def changeValue(self, **kwargs):
        self.__dict__.update(kwargs)
        
    def getKeys(self):
        print(self.__dict__.keys())
        
    def plot(self, name):
        from RIXS import PlotRIXS
        
        PlotRIXS.plotRIXS(self, name)


class XASAveraged:
    _defaults = ("Averaged_Spectrum_pumped",\
                "Averaged_Spectrum_unpumped",\
                "Scans_in_average",\
                "Shots_Per_Point_pumped",\
                "Shots_Per_Point_unpumped",\
                "Energy",\
                "Difference_Spectrum")

    _default_value = None

    def __init__(self, **kwargs):
        self.__dict__.update(dict.fromkeys(self._defaults, self._default_value))
        self.__dict__.update(kwargs)

    def changeValue(self, **kwargs):
        self.__dict__.update(kwargs)
        
    def getKeys(self):
        print(self.__dict__.keys())