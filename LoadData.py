#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 01:05:13 2019

@author: ext-poulter_b
"""

from alvra_tools.load_data import *
from alvra_tools.channels import *
from load_PumpProbe_events_BIP import load_PumpProbe_events_BIP

def LoadData(scan_name,XAS,XES):
    
    import sys
    sys.path.insert(0, '/das/work/p17/p17983/')
    import numpy as np
    import json
    import os
    import RawDataClass as RDC

    
    

    
    if XAS:
        DIR = "/sf/alvra/data/p17983/raw/scan_data/" + scan_name + "/"
    if XES:
        DIR = "/sf/alvra/data/p17983/raw/" + scan_name + "/"
    DIR_json = "/sf/alvra/data/p17983/res/scan_info/"
    
    xasRawData = RDC.XASRawData()
    print(DIR)
    json_file = DIR_json + scan_name + "_scan_info.json"
    print (json_file)
    if XAS is True:
        with open(json_file) as file:
            data = json.load(file)
            numFiles = len(data['scan_files'])
            looprange = range(0,numFiles)
    if XES is True:
        print("Lower File number bound? (XES)")
        num_XES_lower = int(input())
        print("Upper File number bound? (XES)")
        num_XES_upper = int(input())
        numFiles = num_XES_upper - num_XES_lower
        looprange = range(num_XES_lower,num_XES_upper)
    print ("Processing",numFiles,"files")
    
    IzeroFEL_pump_original_total = []
    IzeroFEL_unpump_original_total = []
    Izero2_pump_total =[]
    Izero2_unpump_total =[]
    Izero3_pump_total =[]
    Izero3_unpump_total =[]
    Izero4_pump_total =[]
    Izero4_unpump_total =[]
    pulseIDs_pump_total =[]
    pulseIDs_unpump_total =[]
    delay_pump_total =[]
    delay_SH_pump_total =[]
    delay_NPP_pump_total =[] 
    Laser_Diode_pump_total =[]
    Laser_refDiode_pump_total =[]
    Laser_diag_pump_total =[]
    PALM_pump_total =[]
    PALM_unpump_total =[]
    PALM_eTOF_pump_total =[]
    PALM_eTOF_unpump_total =[]
    PALM_drift_pump_total =[]
    PALM_drift_unpump_total =[]
    BAM_pump_total = []
    BAM_unpump_total = []
    DataFluo_pump_original_total = []
    DataFluo_unpump_original_total = []
    Energy_eV = np.empty(0)
    waveplate_total = np.empty(0)
    
    for i in looprange:
#for i in range(0,1):
        if XAS is True:
            filename = str(data['scan_files'][i][0])
        if XES is True:
            filename = 'run_000' + '%02d' %i +'.BSREAD.h5'
            print(filename)
        filename = DIR + os.path.basename(filename)
        exists = os.path.isfile(filename)
        if not exists:
            print("No such file")
        elif exists: 
#         print("step",i+1,"of",numFiles,": Processing %s" %(str(data['scan_files'][i][0])))

            (DataFluo_pump, DataFluo_unpump, IzeroFEL_pump, IzeroFEL_unpump,\
             Izero2_pump, Izero2_unpump, Izero3_pump,Izero3_unpump,Izero4_pump,Izero4_unpump,\
             pulseIDs_pump,pulseIDs_unpump, delay_pump, delay_SH_pump,delay_NPP_pump,\
             Laser_Diode_pump, Laser_refDiode_pump,Laser_diag_pump, PALM_pump, PALM_unpump,\
             PALM_eTOF_pump,PALM_eTOF_unpump,PALM_drift_pump, PALM_drift_unpump, BAM_pump,\
             BAM_unpump, waveplate, Energy) = \
            load_PumpProbe_events_BIP(filename)
            
            IzeroFEL_pump_original_total.append(IzeroFEL_pump.T[0])
            IzeroFEL_unpump_original_total.append(IzeroFEL_unpump.T[0])
            
            Izero2_pump_total.append(Izero2_pump.T[0])
            Izero2_unpump_total.append(Izero2_unpump.T[0])
            
            Izero3_pump_total.append(Izero3_pump.T[0])
            Izero3_unpump_total.append(Izero3_unpump.T[0])
            
            Izero4_pump_total.append(Izero4_pump.T[0])
            Izero4_unpump_total.append(Izero4_unpump.T[0])

            
            DataFluo_pump_original_total.append(DataFluo_pump.T[0])
            DataFluo_unpump_original_total.append(DataFluo_unpump.T[0])
            
            pulseIDs_pump_total.append(pulseIDs_pump.T[0])
            pulseIDs_unpump_total.append(pulseIDs_unpump.T[0])
            
            delay_pump_total.append(delay_pump.T[0])
            delay_SH_pump_total.append(delay_SH_pump.T[0])
            delay_NPP_pump_total.append(delay_NPP_pump.T[0])
            Laser_Diode_pump_total.append(Laser_Diode_pump.T[0])
            Laser_refDiode_pump_total.append(Laser_refDiode_pump.T[0])
            Laser_diag_pump_total.append(Laser_diag_pump.T[0])
            
            PALM_pump_total.append(PALM_pump.T[0])
            PALM_unpump_total.append(PALM_unpump.T[0])
            PALM_eTOF_pump_total.append(PALM_eTOF_pump.T[0])
            PALM_eTOF_unpump_total.append(PALM_eTOF_unpump.T[0])
            PALM_drift_pump_total.append(PALM_drift_pump.T[0])
            PALM_drift_unpump_total.append(PALM_drift_unpump.T[0])
            BAM_pump_total.append(BAM_pump.T[0])
            BAM_unpump_total.append(BAM_unpump.T[0])
            
            
            waveplate =[x for x in Energy if (np.abs(x) > 0)]
            waveplate_total = np.append(waveplate_total,np.mean(waveplate))
            Energy = [x for x in Energy if (np.abs(x) > 0)]
            Energy_eV = np.append(Energy_eV, np.mean(Energy))
        
            IzeroMedian = np.median(np.concatenate([IzeroFEL_pump, IzeroFEL_unpump]))
            IzeroSTD = np.std(np.concatenate([IzeroFEL_pump, IzeroFEL_unpump]))
            

#    Energy = [2852.0, 2851.0, 2850.0, 2849.0, 2848.0, 2847.0, 2846.5,\
#                    2846.0, 2845.5 , 2845.0, 2844.75, 2844.5 , 2844.25, 2844.0,\
#                    2843.75, 2843.5 , 2843.25, 2843.0, 2842.75, 2842.5 , 2842.25,\
#                    2842.0, 2841.75, 2841.5 , 2841.25, 2841.0, 2840.75, 2840.5,\
#                    2840.25, 2840.0, 2839.75, 2839.5 , 2839.25, 2839.0, 2838.75,\
#                    2838.5, 2838.25, 2838.0, 2837.75, 2837.5 , 2837.25, 2837.0,\
#                    2836.75, 2836.5 , 2836.25, 2836.0, 2835.75, 2835.5 , 2835.25,\
#                    2835.0, 2834.5 , 2834.0, 2833.0, 2832.0, 2831.0]
    
    xasRawData.changeValue(Izero_pump_total=IzeroFEL_pump_original_total\
                           ,Izero_unpump_total=IzeroFEL_unpump_original_total\
                           ,DataFluo_pump_total=DataFluo_pump_original_total\
                           ,DataFluo_unpump_total=DataFluo_unpump_original_total\
                           ,IzeroMedian=IzeroMedian\
                           ,IzeroSTD=IzeroSTD\
                           ,Energy = Energy_eV,
                           Izero2_pump_total=Izero2_pump_total,\
                           Izero2_unpump_total=Izero2_unpump_total,\
                           Izero3_pump_total=Izero3_pump_total,\
                           Izero3_unpump_total=Izero3_unpump_total,\
                           Izero4_pump_total=Izero4_pump_total,\
                           Izero4_unpump_total=Izero4_unpump_total,\
                           pulseIDs_pump=pulseIDs_pump_total,\
                           pulseIDs_unpump=pulseIDs_unpump_total,\
                           delay_pump=delay_pump_total,\
                           delay_SH_pump=delay_SH_pump_total,\
                           delay_NPP_pump=delay_NPP_pump_total,\
                           Laser_Diode_pump=Laser_Diode_pump_total,\
                           Laser_refDiode_pump=Laser_refDiode_pump_total,\
                           Laser_diag_pump=Laser_diag_pump_total,\
                           PALM_pump=PALM_pump_total,\
                           PALM_unpump=PALM_unpump_total,\
                           PALM_eTOF_pump=PALM_eTOF_pump_total,\
                           PALM_eTOF_unpump=PALM_eTOF_unpump_total,\
                           PALM_drift_pump=PALM_drift_pump_total,\
                           PALM_drift_unpump=PALM_drift_unpump_total,\
                           BAM_pump=BAM_pump_total,\
                           BAM_unpump=BAM_unpump_total,\
                           waveplate=waveplate_total)
    
    return xasRawData
        
        
        