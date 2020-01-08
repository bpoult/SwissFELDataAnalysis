#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 21:07:23 2019

@author: ext-poulter_b
"""
import numpy as np
from matplotlib import pyplot as plt
from TimeCorrection import TimeCorrection
import ProcessedDataClass as PDC

XASProData = PDC.XASProData()
numstds = 4
minIzero = 0.015
lin_filter = 0.03


def FilterData(xasrawdata, PlotOn, CorrectTime):
    # numstds is the number of standard deviations to take from the median
    # minIzero sets the minimum permissable Izero
    # lin_filter sets upper and lower bounds for the filter
    if CorrectTime is True:
        time_zero_mm = 156.2826
        xasrawdata = TimeCorrection(xasrawdata,time_zero_mm)

    FilterParameters = ['numstds:' + str(numstds) + ' minIzero:' + str(minIzero) + ' lin_filter:' + str(lin_filter)]
    DataFluo_pump_norm_total = np.empty(0)
    DataFluo_unpump_norm_total = np.empty(0)
    IzeroFEL_pump_total = np.empty(0)
    IzeroFEL_unpump_total = np.empty(0)
    DataFluo_pump_total = np.empty(0)
    DataFluo_unpump_total = np.empty(0)
    iZero = np.empty(0)
    IzeroFEL_pump_raw_total = np.empty(0)
    IzeroFEL_unpump_raw_total = np.empty(0)
    DataFluo_pump_raw_total = np.empty(0)
    DataFluo_unpump_raw_total = np.empty(0)
    Fluo_pump_std = np.empty(0)
    Fluo_unpump_std = np.empty(0)
    PulseID_pump_total = np.empty(0)
    PulseID_unpump_total = np.empty(0)
    time_delay_ps_total = np.empty(0)
    number = len(xasrawdata.DataFluo_pump_total)

    IzeroMedian = xasrawdata.IzeroMedian
    IzeroSTD = xasrawdata.IzeroSTD
    Energy = xasrawdata.Energy
    shotsprefilterpump = [0] * number
    shotspostfilterpump = [0] * number
    shotsprefilterunpump = [0] * number
    shotspostfilterunpump = [0] * number
    for i in range(number):

        DataFluo_pump = xasrawdata.DataFluo_pump_total[i]
        DataFluo_unpump = xasrawdata.DataFluo_unpump_total[i]
        IzeroFEL_pump = xasrawdata.Izero_pump_total[i]
        IzeroFEL_unpump = xasrawdata.Izero_unpump_total[i]
        PulseID_pump = xasrawdata.pulseIDs_pump[i]
        PulseID_unpump = xasrawdata.pulseIDs_unpump[i]
        time_delay_ps = xasrawdata.Tcorrected_pump[i]

        IzeroFEL_pump_raw_total = np.append(IzeroFEL_pump_raw_total, IzeroFEL_pump)
        IzeroFEL_unpump_raw_total = np.append(IzeroFEL_unpump_raw_total, IzeroFEL_unpump)
        DataFluo_pump_raw_total = np.append(DataFluo_pump_raw_total, DataFluo_pump)
        DataFluo_unpump_raw_total = np.append(DataFluo_unpump_raw_total, DataFluo_unpump)

        linFit_pump = np.polyfit(IzeroFEL_pump, DataFluo_pump, 1)
        linFit_unpump = np.polyfit(IzeroFEL_unpump, DataFluo_unpump, 1)

        conditionPumpLinHigh = DataFluo_pump < IzeroFEL_pump * linFit_pump[0] + linFit_pump[1] + lin_filter
        conditionPumpLinLow = DataFluo_pump > IzeroFEL_pump * linFit_pump[0] + linFit_pump[1] - lin_filter

        conditionUnPumpLinHigh = DataFluo_unpump < IzeroFEL_unpump * linFit_unpump[0] + linFit_unpump[1] + lin_filter
        conditionUnPumpLinLow = DataFluo_unpump > IzeroFEL_unpump * linFit_unpump[0] + linFit_unpump[1] - lin_filter

        IzeroMedian + numstds * IzeroSTD

        conditionPumpMax = IzeroFEL_pump < IzeroMedian + numstds * IzeroSTD
        conditionPumpMin = IzeroFEL_pump > IzeroMedian - numstds * IzeroSTD
        conditionPumpLow = IzeroFEL_pump > minIzero

        conditionUnPumpMax = IzeroFEL_unpump < IzeroMedian + numstds * IzeroSTD
        conditionUnPumpMin = IzeroFEL_unpump > IzeroMedian - numstds * IzeroSTD
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

        PulseID_pumpPro = PulseID_pump[condIzeroPump]
        PulseID_unpumpPro = PulseID_unpump[condIzeroUnPump]
        PulseID_pump_total = np.append(PulseID_pump_total,PulseID_pumpPro)
        PulseID_unpump_total = np.append(PulseID_unpump_total,PulseID_unpumpPro)

        time_delay_psPro = time_delay_ps[condIzeroPump]
        time_delay_ps_total = np.append(time_delay_ps_total,time_delay_psPro)

        DataFluo_pump_norm = DataFluo_pumpPro / IzeroFEL_pumpPro
        DataFluo_unpump_norm = DataFluo_unpumpPro / IzeroFEL_unpumpPro
        Fluo_pump_std = np.append(Fluo_pump_std,np.std(DataFluo_pump_norm))
        Fluo_unpump_std = np.append(Fluo_unpump_std,np.std(DataFluo_unpump_norm))
        DataFluo_pump_norm_total = np.append(DataFluo_pump_norm_total, DataFluo_pump_norm.mean())
        DataFluo_unpump_norm_total = np.append(DataFluo_unpump_norm_total, DataFluo_unpump_norm.mean())


        iZero = np.append(iZero, np.mean(IzeroFEL_pump_total))

        if i == 12 and PlotOn:  # feel free to elmnate this if statement and following line

            plt.scatter(IzeroFEL_pump, DataFluo_pump)
            plt.scatter(IzeroFEL_pumpPro, DataFluo_pumpPro)
            plt.title('Izero, pumped')
            plt.xlabel('I0')
            plt.ylabel('Absorption')
        # Energy[28] = 2840.25
        shotsprefilterpump[i] = len(DataFluo_pump)
        shotspostfilterpump[i] = len(DataFluo_pumpPro)
        shotsprefilterunpump[i] = len(DataFluo_unpump)
        shotspostfilterunpump[i] = len(DataFluo_unpumpPro)

    XASProData.changeValue(Izero_pump_total=IzeroFEL_pump_total, Izero_unpump_total=IzeroFEL_unpump_total
                           , DataFluo_pump_total=DataFluo_pump_total, DataFluo_pump_norm_total=DataFluo_pump_norm_total,
                           DataFluo_unpump_total=DataFluo_unpump_total, DataFluo_unpump_norm_total=DataFluo_unpump_norm_total,
                           IzeroMedian=IzeroMedian, IzeroSTD=IzeroSTD, Energy=Energy, FilterParameters=FilterParameters,
                           shotsprefilterpump=shotsprefilterpump, shotspostfilterpump=shotspostfilterpump,
                           shotsprefilterunpump=shotsprefilterunpump, shotspostfilterunpump=shotspostfilterunpump,
                           Fluo_pump_std=Fluo_pump_std,Fluo_unpump_std=Fluo_unpump_std, PulseID_pump_total=PulseID_pump_total,
                           PulseID_unpump_total=PulseID_unpump_total,time_delay_ps_total=time_delay_ps_total)

    print("The original number of pumped and unpumped shots is:")
    print(len(xasrawdata.Izero_pump_total[1]) * len(xasrawdata.Izero_pump_total), \
          + len(xasrawdata.Izero_unpump_total[1]) * len(xasrawdata.Izero_unpump_total))
    print("The filtered number of pumped and unpumped shots is:")
    print(len(XASProData.Izero_pump_total), len(XASProData.Izero_unpump_total))

    if PlotOn:
        print('ploton is on')
        plt.figure()
        _, bins, _ = plt.hist(IzeroFEL_pump_raw_total, 100, label='unfiltered')
        _ = plt.hist(IzeroFEL_pump_total, bins, rwidth=.5, label='filtered')
        plt.title('Izero, pumped')
        plt.legend()

        plt.figure()
        _, bins, _ = plt.hist(IzeroFEL_unpump_raw_total, 100, label='unfiltered')
        _ = plt.hist(IzeroFEL_unpump_total, bins, rwidth=.5, label='filtered')
        plt.title('Izero, unpumped')
        plt.legend()

        plt.figure()
        plt.scatter(IzeroFEL_pump_raw_total, DataFluo_pump_raw_total)
        plt.scatter(IzeroFEL_pump_total, DataFluo_pump_total, alpha=0.05)
        plt.title('Izero, pumped')
        plt.xlabel('I0')
        plt.ylabel('Absorption')

        plt.figure()
        plt.scatter(IzeroFEL_unpump_raw_total, DataFluo_unpump_raw_total)
        plt.scatter(IzeroFEL_unpump_total, DataFluo_unpump_total, alpha=0.05)
        plt.title('Izero, unpumped')
        plt.xlabel('I0')
        plt.ylabel('Absorption')

    return XASProData


def FilteringStuff(i, xasrawdata):
    FilterParameters = ['numstds:' + str(numstds) + ' minIzero:' + str(minIzero) + ' lin_filter:' + str(lin_filter)]
    IzeroMedian = xasrawdata.IzeroMedian
    IzeroSTD = xasrawdata.IzeroSTD
    DataFluo_pump = xasrawdata.DataFluo_pump_total[i]
    DataFluo_unpump = xasrawdata.DataFluo_unpump_total[i]
    IzeroFEL_pump = xasrawdata.Izero_pump_total[i]
    IzeroFEL_unpump = xasrawdata.Izero_unpump_total[i]

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

    condIzeroPump = conditionPumpMax & conditionPumpMin & conditionPumpLow & conditionPumpLinHigh & conditionPumpLinLow
    condIzeroUnPump = conditionUnPumpMax & conditionUnPumpMin & conditionUnPumpLow & conditionUnPumpLinHigh & conditionUnPumpLinLow

    condFinalPump = condLin_pump & condIzeroPump
    condFinalUnPump = condLin_unpump & condIzeroUnPump

    return condFinalPump, condFinalUnPump, FilterParameters
