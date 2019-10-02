#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 21:07:23 2019

@author: ext-poulter_b
"""
import numpy as np
from matplotlib import pyplot as plt
import ProcessedDataClass as PDC 
    
XASProData = PDC.XASProData()
numstds = 2.8
minIzero = 0.022
lin_filter = 0.08

def FilterData(xasrawdata,PlotOn):

# numstds is the number of standard deviations to take from the median
# minIzero sets the minimum permissable Izero
# lin_filter sets upper and lower bounds for the filter


    DataFluo_pump_norm_total = np.empty(0)
    DataFluo_unpump_norm_total = np.empty(0)
    err_DataFluo_pump_total = np.empty(0)
    err_DataFluo_unpump_total = np.empty(0)
    IzeroFEL_pump_total = np.empty(0)
    IzeroFEL_unpump_total = np.empty(0)
    DataFluo_pump_total = np.empty(0)
    DataFluo_unpump_total = np.empty(0)
    iZero = np.empty(0)
    IzeroFEL_pump_raw_total = np.empty(0)
    IzeroFEL_unpump_raw_total = np.empty(0)
    DataFluo_pump_raw_total = np.empty(0)
    DataFluo_unpump_raw_total = np.empty(0)
    number = len(xasrawdata.DataFluo_pump_total)
    
    IzeroMedian = xasrawdata.IzeroMedian
    IzeroSTD = xasrawdata.IzeroSTD
    Energy = xasrawdata.Energy

    for i in range(number):

        DataFluo_pump = xasrawdata.DataFluo_pump_total[i]
        DataFluo_unpump = xasrawdata.DataFluo_unpump_total[i]
        IzeroFEL_pump = xasrawdata.Izero_pump_total[i]
        IzeroFEL_unpump = xasrawdata.Izero_unpump_total[i]
            
        IzeroFEL_pump_raw_total = np.append(IzeroFEL_pump_raw_total, IzeroFEL_pump)
        IzeroFEL_unpump_raw_total = np.append(IzeroFEL_unpump_raw_total, IzeroFEL_unpump)
        DataFluo_pump_raw_total = np.append(DataFluo_pump_raw_total, DataFluo_pump)
        DataFluo_unpump_raw_total = np.append(DataFluo_unpump_raw_total, DataFluo_unpump)
    
        linFit_pump = np.polyfit(IzeroFEL_pump,DataFluo_pump,1)
        linFit_unpump = np.polyfit(IzeroFEL_unpump,DataFluo_unpump,1)
        
        conditionPumpLinHigh =  DataFluo_pump < IzeroFEL_pump*linFit_pump[0]+linFit_pump[1]+lin_filter
        conditionPumpLinLow =  DataFluo_pump > IzeroFEL_pump*linFit_pump[0]+linFit_pump[1]-lin_filter
        
        conditionUnPumpLinHigh =  DataFluo_unpump < IzeroFEL_unpump*linFit_unpump[0]+linFit_unpump[1]+lin_filter
        conditionUnPumpLinLow =  DataFluo_unpump > IzeroFEL_unpump*linFit_unpump[0]+linFit_unpump[1]-lin_filter
        
        condLin_pump =  conditionPumpLinHigh & conditionPumpLinLow
        condLin_unpump =  conditionUnPumpLinHigh & conditionUnPumpLinLow

        IzeroMedian+numstds*IzeroSTD
        
        conditionPumpMax = IzeroFEL_pump < IzeroMedian+numstds*IzeroSTD
        conditionPumpMin = IzeroFEL_pump > IzeroMedian-numstds*IzeroSTD
        conditionPumpLow = IzeroFEL_pump > minIzero

        conditionUnPumpMax = IzeroFEL_unpump < IzeroMedian+numstds*IzeroSTD
        conditionUnPumpMin = IzeroFEL_unpump > IzeroMedian-numstds*IzeroSTD
        conditionUnPumpLow = IzeroFEL_unpump > minIzero

        condIzeroPump = conditionPumpMax & conditionPumpMin & conditionPumpLow & conditionPumpLinHigh & conditionPumpLinLow
        condIzeroUnPump = conditionUnPumpMax & conditionUnPumpMin & conditionUnPumpLow & conditionUnPumpLinHigh & conditionUnPumpLinLow
            
        IzeroFEL_pumpPro = IzeroFEL_pump[condIzeroPump]
        IzeroFEL_unpumpPro = IzeroFEL_unpump[condIzeroUnPump]
        
        IzeroFEL_pump_total = np.append(IzeroFEL_pump_total, IzeroFEL_pumpPro)
        IzeroFEL_unpump_total = np.append(IzeroFEL_unpump_total, IzeroFEL_unpumpPro)
        
        DataFluo_pumpPro = DataFluo_pump[condIzeroPump]
        DataFluo_unpumpPro = DataFluo_unpump[condIzeroUnPump]
    
    
        DataFluo_pump_total = np.append(DataFluo_pump_total, DataFluo_pumpPro)
        DataFluo_unpump_total = np.append(DataFluo_unpump_total, DataFluo_unpumpPro)
        
        DataFluo_pump_norm = DataFluo_pumpPro/IzeroFEL_pumpPro
        DataFluo_unpump_norm = DataFluo_unpumpPro/IzeroFEL_unpumpPro
        
        DataFluo_pump_norm_total = np.append(DataFluo_pump_norm_total, DataFluo_pump_norm.mean())
        DataFluo_unpump_norm_total = np.append(DataFluo_unpump_norm_total, DataFluo_unpump_norm.mean())
        err_DataFluo_pump_total = np.append(err_DataFluo_pump_total, DataFluo_pump_norm.std()/np.sqrt(DataFluo_pump_norm.size))
        err_DataFluo_unpump_total = np.append(err_DataFluo_unpump_total, DataFluo_unpump_norm.std()/np.sqrt(DataFluo_unpump_norm.size))
        
        iZero = np.append(iZero, np.mean(IzeroFEL_pump_total))
        
        
        condFinalPump = condLin_pump & condIzeroPump
        condFinalUnPump = condLin_unpump & condIzeroUnPump
        
        if i == 25 and PlotOn:   # feel free to elmnate this if statement and following line
            
            plt.scatter(IzeroFEL_pump, DataFluo_pump)
            plt.scatter(IzeroFEL_pumpPro, DataFluo_pumpPro)
            plt.title('Izero, pumped')
            plt.xlabel('I0')
            plt.ylabel('Absorption')
   # Energy[28] = 2840.25
    XASProData.changeValue(Izero_pump_total=IzeroFEL_pump_total,Izero_unpump_total=IzeroFEL_unpump_total\
                           ,DataFluo_pump_total=DataFluo_pump_total,DataFluo_pump_norm_total=DataFluo_pump_norm_total, \
                           DataFluo_unpump_total=DataFluo_unpump_total,DataFluo_unpump_norm_total=DataFluo_unpump_norm_total\
                           ,IzeroMedian=IzeroMedian, IzeroSTD=IzeroSTD, Energy = Energy)
    

        
        
    print("The original number of pumped and unpumped shots is:")
    print(len(xasrawdata.Izero_pump_total[1])*len(xasrawdata.Izero_pump_total),\
          + len(xasrawdata.Izero_unpump_total[1])*len(xasrawdata.Izero_unpump_total))
    print("The filtered number of pumped and unpumped shots is:")
    print(len(XASProData.Izero_pump_total), len(XASProData.Izero_unpump_total))
    
    if PlotOn:
        print('ploton is on')
        plt.figure()
        _, bins, _ = plt.hist(IzeroFEL_pump_raw_total, 100, label = 'unfiltered')
        _ = plt.hist(IzeroFEL_pump_total, bins, rwidth = .5, label = 'filtered')
        plt.title('Izero, pumped')
        plt.legend()

        plt.figure()
        _, bins, _ = plt.hist(IzeroFEL_unpump_raw_total, 100, label = 'unfiltered')
        _ = plt.hist(IzeroFEL_unpump_total, bins, rwidth = .5, label = 'filtered')
        plt.title('Izero, unpumped')
        plt.legend()
        
        plt.figure()
        plt.scatter(IzeroFEL_pump_raw_total, DataFluo_pump_raw_total)
        plt.scatter(IzeroFEL_pump_total, DataFluo_pump_total)
        plt.title('Izero, pumped')
        plt.xlabel('I0')
        plt.ylabel('Absorption')

        plt.figure()
        plt.scatter(IzeroFEL_unpump_raw_total, DataFluo_unpump_raw_total)
        plt.scatter(IzeroFEL_unpump_total, DataFluo_unpump_total)
        plt.title('Izero, unpumped')
        plt.xlabel('I0')
        plt.ylabel('Absorption')
        
    return XASProData


def FilteringStuff(i,xasrawdata):
    
    IzeroMedian = xasrawdata.IzeroMedian
    IzeroSTD = xasrawdata.IzeroSTD
    DataFluo_pump = xasrawdata.DataFluo_pump_total[i]
    DataFluo_unpump = xasrawdata.DataFluo_unpump_total[i]
    IzeroFEL_pump = xasrawdata.Izero_pump_total[i]
    IzeroFEL_unpump = xasrawdata.Izero_unpump_total[i]
    
    linFit_pump = np.polyfit(IzeroFEL_pump,DataFluo_pump,1)
    linFit_unpump = np.polyfit(IzeroFEL_unpump,DataFluo_unpump,1)
        
    conditionPumpLinHigh =  DataFluo_pump < IzeroFEL_pump*linFit_pump[0]+linFit_pump[1]+lin_filter
    conditionPumpLinLow =  DataFluo_pump > IzeroFEL_pump*linFit_pump[0]+linFit_pump[1]-lin_filter
        
    conditionUnPumpLinHigh =  DataFluo_unpump < IzeroFEL_unpump*linFit_unpump[0]+linFit_unpump[1]+lin_filter
    conditionUnPumpLinLow =  DataFluo_unpump > IzeroFEL_unpump*linFit_unpump[0]+linFit_unpump[1]-lin_filter
        
    condLin_pump =  conditionPumpLinHigh & conditionPumpLinLow
    condLin_unpump =  conditionUnPumpLinHigh & conditionUnPumpLinLow

    IzeroMedian+numstds*IzeroSTD
        
    conditionPumpMax = IzeroFEL_pump < IzeroMedian+numstds*IzeroSTD
    conditionPumpMin = IzeroFEL_pump > IzeroMedian-numstds*IzeroSTD
    conditionPumpLow = IzeroFEL_pump > minIzero

    conditionUnPumpMax = IzeroFEL_unpump < IzeroMedian+numstds*IzeroSTD
    conditionUnPumpMin = IzeroFEL_unpump > IzeroMedian-numstds*IzeroSTD
    conditionUnPumpLow = IzeroFEL_unpump > minIzero

    condIzeroPump = conditionPumpMax & conditionPumpMin & conditionPumpLow & conditionPumpLinHigh & conditionPumpLinLow
    condIzeroUnPump = conditionUnPumpMax & conditionUnPumpMin & conditionUnPumpLow & conditionUnPumpLinHigh & conditionUnPumpLinLow
            
    condFinalPump = condLin_pump & condIzeroPump
    condFinalUnPump = condLin_unpump & condIzeroUnPump

    return condFinalPump,condFinalUnPump




