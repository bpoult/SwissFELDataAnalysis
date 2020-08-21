#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 21:07:23 2019

@author: ext-poulter_b
"""
import numpy as np




def Filtering(ii, rawdata, numstds=4.5, minIzero=0.01, lin_filter=0.025, minTime=0.3, maxTime=12):
    FilterParameters = ['numstds:' + str(numstds) + ' minIzero:' + str(minIzero) + ' lin_filter:' + str(lin_filter)]
    IzeroMedian = rawdata.IzeroMedian
    IzeroSTD = rawdata.IzeroSTD
    DataFluo_pump = rawdata.DataFluo_pump_total[ii]
    DataFluo_unpump = rawdata.DataFluo_unpump_total[ii]
    IzeroFEL_pump = rawdata.Izero_pump_total[ii]
    IzeroFEL_unpump = rawdata.Izero_unpump_total[ii]
    #time_delay_ps = rawdata.Tcorrected_pump[ii]
    
    linFit_pump = np.polyfit(IzeroFEL_pump, DataFluo_pump, 1)
    linFit_unpump = np.polyfit(IzeroFEL_unpump, DataFluo_unpump, 1)

    conditionPumpLinHigh = DataFluo_pump < IzeroFEL_pump * linFit_pump[0] + linFit_pump[1] + lin_filter
    conditionPumpLinLow = DataFluo_pump > IzeroFEL_pump * linFit_pump[0] + linFit_pump[1] - lin_filter

    conditionUnPumpLinHigh = DataFluo_unpump < IzeroFEL_unpump * linFit_unpump[0] + linFit_unpump[1] + lin_filter
    conditionUnPumpLinLow = DataFluo_unpump > IzeroFEL_unpump * linFit_unpump[0] + linFit_unpump[1] - lin_filter

    condLin_pump = conditionPumpLinHigh & conditionPumpLinLow
    condLin_unpump = conditionUnPumpLinHigh & conditionUnPumpLinLow

    IzeroMedian + numstds * IzeroSTD

    conditionPumpMax = IzeroFEL_pump < IzeroMedian + numstds * IzeroSTD
    conditionPumpMin = IzeroFEL_pump > IzeroMedian - numstds * IzeroSTD
    conditionPumpLow = IzeroFEL_pump > minIzero


    conditionUnPumpMax = IzeroFEL_unpump < IzeroMedian + numstds * IzeroSTD
    conditionUnPumpMin = IzeroFEL_unpump > IzeroMedian - numstds * IzeroSTD
    conditionUnPumpLow = IzeroFEL_unpump > minIzero
    #conditionTimePumpLow = time_delay_ps > minTime
    #conditionTimePumpHigh = time_delay_ps < maxTime


    condIzeroPump = conditionPumpMax & conditionPumpMin & conditionPumpLow & conditionPumpLinHigh & conditionPumpLinLow
    condIzeroUnPump = conditionUnPumpMax & conditionUnPumpMin & conditionUnPumpLow & conditionUnPumpLinHigh & conditionUnPumpLinLow

    condFinalPump = condLin_pump & condIzeroPump
    condFinalUnPump = condLin_unpump & condIzeroUnPump

    return condFinalPump, condFinalUnPump, FilterParameters, IzeroFEL_pump, IzeroFEL_unpump

def JF_PIPS_filter(images_on,images_off,rawdata,i, JF_PIPS_lin_filter=0.8):
    JF_PIPS_parameters = ['JF_PIPS_LinParam: '+ str(JF_PIPS_lin_filter)]
    DataFluo_pump = rawdata.DataFluo_pump_total[i]
    DataFluo_unpump = rawdata.DataFluo_unpump_total[i]
    JF_pumped = np.sum(np.sum(images_on,axis=2),axis=1)
    JF_unpumped = np.sum(np.sum(images_off,axis=2),axis=1)

    linFit_pump = np.polyfit(JF_pumped, DataFluo_pump, 1)
    linFit_unpump = np.polyfit(JF_unpumped, DataFluo_unpump, 1)
    
    cond_JF_PIPS_pump_high = DataFluo_pump < JF_pumped * linFit_pump[0] + linFit_pump[1] + JF_PIPS_lin_filter
    cond_JF_PIPS_pump_low = DataFluo_pump > JF_pumped * linFit_pump[0] + linFit_pump[1] - JF_PIPS_lin_filter
    
    cond_JF_PIPS_unpump_high = DataFluo_unpump < JF_unpumped * linFit_unpump[0] + linFit_unpump[1] + JF_PIPS_lin_filter
    cond_JF_PIPS_unpump_low = DataFluo_unpump > JF_unpumped * linFit_unpump[0] + linFit_unpump[1] - JF_PIPS_lin_filter

    cond_JF_PIPS_pumped = cond_JF_PIPS_pump_high & cond_JF_PIPS_pump_low
    cond_JF_PIPS_unpumped = cond_JF_PIPS_unpump_high & cond_JF_PIPS_unpump_low
    
    
    
    return cond_JF_PIPS_pumped, cond_JF_PIPS_unpumped, JF_PIPS_parameters
