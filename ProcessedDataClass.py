#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 20:39:35 2019

@author: ext-poulter_b
"""



class RIXSProData:
    _defaults = ("RIXS_map_pumped", "RIXS_map_unpumped", \
                "FilterParameters", "Energy", "TFY_on", "TFY_off")

    _default_value = None

    def __init__(self, **kwargs):
        self.__dict__.update(dict.fromkeys(self._defaults, self._default_value))
        self.__dict__.update(kwargs)

    def changeValue(self, **kwargs):
        self.__dict__.update(kwargs)
        
    def getKeys(self):
        return self.__dict__.keys()
        
    def plot(self, name, energy_cut, JF_cut):
        from RIXS import PlotRIXS
        
        PlotRIXS.plotRIXS(self, name, energy_cut, JF_cut)
        
    def combine(self, prodata):
        
        if (self.RIXS_map_pumped is None):
            print('none detected')
            
            self.RIXS_map_pumped = prodata.RIXS_map_pumped
            self.RIXS_map_unpumped = prodata.RIXS_map_unpumped
            self.FilterParameters = prodata.FilterParameters
            self.Energy = prodata.Energy
            #self.TFY_on = prodata.TFY_on
            #self.TFY_off = prodata.TFY_off
            
            if 'RIXS_map_pumped_err' in list(prodata.getKeys()):
                self.RIXS_map_pumped_err = prodata.RIXS_map_pumped_err**2
                self.RIXS_map_unpumped_err = prodata.RIXS_map_unpumped_err**2
            
        else:
            print('good to go')
            print(self.RIXS_map_pumped.shape)
            print(prodata.RIXS_map_pumped.shape)
            self.RIXS_map_pumped = self.RIXS_map_pumped + prodata.RIXS_map_pumped
            self.RIXS_map_unpumped = self.RIXS_map_unpumped + prodata.RIXS_map_unpumped
            #self.TFY_on = self.TFY_on + prodata.TFY_on
            #self.TFY_off = self.TFY_off + prodata.TFY_off
            
            if 'RIXS_map_pumped_err' in list(self.getKeys()):
                self.RIXS_map_pumped_err = self.RIXS_map_pumped_err + prodata.RIXS_map_pumped_err**2
                self.RIXS_map_unpumped_err = self.RIXS_map_unpumped_err + prodata.RIXS_map_unpumped_err**2
            
            if not(self.FilterParameters == prodata.FilterParameters):
                print('You are attempting to combine processed data with different filter parameters')
                
            if not((self.Energy == prodata.Energy).all()):
                print('You are attempting to combine processed data with different monoenergy scans')




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
        return self.__dict__.keys()
    
    
    
    

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
        return self.__dict__.keys()