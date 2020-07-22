#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 22:40:56 2019

@author: ext-poulter_b
"""

from common.channels import *
import h5py
import numpy as np


def _get_data(f):
    if "data" in f:
        return f["data"]
    else:
        return f

def load_PumpProbe_events(filename, nshots=None):
    with h5py.File(filename, 'r') as BS_file:

        BS_file = _get_data(BS_file)
        
        pulse_ids = BS_file[channel_BS_pulse_ids][:nshots]
        
        FEL = BS_file[channel_Events][:nshots,48]
        Laser = BS_file[channel_Events][:nshots,18]
        Darkshot = BS_file[channel_Events][:nshots,21]
        
        index_pump = np.logical_and.reduce((FEL, Laser, np.logical_not(Darkshot)))
        index_unpump = np.logical_and.reduce((FEL, Laser, Darkshot))
                
        DataFluo_pump = BS_file[channel_PIPS_fluo][:nshots][index_pump]
        DataFluo_unpump = BS_file[channel_PIPS_fluo][:nshots][index_unpump]
                
        IzeroFEL_pump = BS_file[channel_Izero][:nshots][index_pump]
        IzeroFEL_unpump = BS_file[channel_Izero][:nshots][index_unpump]
        
        Izero2_pump = BS_file[channel_Izero2][:nshots][index_pump]
        Izero2_unpump = BS_file[channel_Izero2][:nshots][index_unpump]
        
        Izero3_pump = BS_file[channel_Izero3][:nshots][index_pump]
        Izero3_unpump = BS_file[channel_Izero3][:nshots][index_unpump]
        
        Izero4_pump = BS_file[channel_Izero4][:nshots][index_pump]
        Izero4_unpump = BS_file[channel_Izero4][:nshots][index_unpump]
        
        pulseIDs_pump = BS_file[channel_BS_pulse_ids][:nshots][index_pump]
        pulseIDs_unpump = BS_file[channel_BS_pulse_ids][:nshots][index_unpump]
        
        delay_pump = BS_file[channel_delay][:nshots][index_pump]
        
        delay_SH_pump = BS_file[channel_delay_SH][:nshots][index_pump]
        
        delay_NPP_pump = BS_file[channel_delay_NPP][:nshots][index_pump]
        
        Laser_Diode_pump = BS_file[channel_LaserDiode][:nshots][index_pump]
        
        Laser_refDiode_pump = BS_file[channel_Laser_refDiode][:nshots][index_pump]
        
        Laser_diag_pump = BS_file[channel_Laser_diag][:nshots][index_pump]
        
        PALM_pump = BS_file[channel_PALM][:nshots][index_pump]
        PALM_unpump = BS_file[channel_PALM][:nshots][index_unpump]
        
        PALM_eTOF_pump = BS_file[channel_PALM_eTOF][:nshots][index_pump]
        PALM_eTOF_unpump = BS_file[channel_PALM_eTOF][:nshots][index_unpump]
        
        PALM_drift_pump = BS_file[channel_PALM_drift][:nshots][index_pump]
        PALM_drift_unpump = BS_file[channel_PALM_drift][:nshots][index_unpump]
        
        BAM_pump = BS_file[channel_BAM][:nshots][index_pump]
        BAM_unpump = BS_file[channel_BAM][:nshots][index_unpump]
        
        waveplate = BS_file[channel_waveplate][:nshots][index_pump]
        
        energy = BS_file[channel_energy][:nshots][index_pump]
        

             
    return DataFluo_pump, DataFluo_unpump, IzeroFEL_pump, IzeroFEL_unpump,\
    Izero2_pump, Izero2_unpump, Izero3_pump,Izero3_unpump,Izero4_pump,Izero4_unpump,\
    pulseIDs_pump,pulseIDs_unpump, delay_pump, delay_SH_pump,delay_NPP_pump,\
    Laser_Diode_pump, Laser_refDiode_pump,Laser_diag_pump, PALM_pump, PALM_unpump,\
    PALM_eTOF_pump,PALM_eTOF_unpump,PALM_drift_pump, PALM_drift_unpump, BAM_pump,\
    BAM_unpump, waveplate, energy