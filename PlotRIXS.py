import numpy as np
import scipy.io as sp
import os
import sys
import matplotlib.pyplot as plt
import pickle
from RawDataClass import RawData as RDC
from ProcessedDataClass import RIXSProData as PDC
from Looking_at_RIXS import plotRIXS
from EmissionToLoss import emiss2loss
ReferenceEnergy = [2852.0, 2851.0, 2850.0, 2849.0, 2848.0, 2847.0, 2846.5, 2846.0, 2845.5, 2845.0, 2844.75, 2844.5,
                       2844.25, 2844.0,
                       2843.75, 2843.5, 2843.25, 2843.0, 2842.75, 2842.5, 2842.25, 2842.0, 2841.75, 2841.5, 2841.25,
                       2841.0, 2840.75, 2840.5,
                       2840.25, 2840.0, 2839.75, 2839.5, 2839.25, 2839.0, 2838.75, 2838.5, 2838.25, 2838.0, 2837.75,
                       2837.5, 2837.25, 2837.0,
                       2836.75, 2836.5, 2836.25, 2836.0, 2835.75, 2835.5, 2835.25, 2835.0, 2834.5, 2834.0, 2833.0,
                       2832.0, 2831.0]
# scans = [3,5,8,10,15,16,17,18]
scans = [6,7,9,10,11,12,15,16,17,18,20]
base = "RuDimerACN_monoscan_0p6ps_0"

dirxas = "C:/Users/poult/Documents/Research/Beamtimes/SwissFEL_July_2019/Transfered_Data/Processed/JF_corrected/600fs/"
dirrixs = "C:/Users/poult/Documents/Research/Beamtimes/SwissFEL_July_2019/Transfered_Data/Processed/JF_corrected/600fs/"

with open('JF_Lalpha_Calibration_2.txt') as f:
    w = [float(x) for x in next(f).split()]  # read first line
    calibration = []
    for line in f:  # read rest of lines
        calibration.append([float(x) for x in line.split()])
calibration = np.asarray(calibration)
calibration = calibration.flatten()
RIXSonAVG, RIXSoffAVG, xasrawdata,xes_on,xes_off = plotRIXS(scans,base,dirxas,dirrixs,False)


# plt.figure()
# X, Y = np.meshgrid(ReferenceEnergy,np.linspace(0, RIXSonAVG.shape[1], RIXSonAVG.shape[1]))
# plt.subplot(1, 1, 1)
# plt.pcolor(X, Y, np.transpose(RIXSonAVG), vmax=0.1)
# plt.colorbar()
# plt.ylabel('JF pixel')
# plt.xlabel('Mono Energy (eV)')
# plt.title('DimerACN RIXS pumped 600fs')
# plt.tight_layout()
#
#
# plt.figure()
# X, Y = np.meshgrid(ReferenceEnergy,np.linspace(0, RIXSoffAVG.shape[1], RIXSoffAVG.shape[1]))
# plt.subplot(1, 1, 1)
# plt.pcolor(X, Y, np.transpose(RIXSoffAVG), vmax=0.1)
# plt.colorbar()
# plt.ylabel('JF pixel')
# plt.xlabel('Mono Energy (eV)')
# plt.title('DimerACN RIXS unpumed 600fs')
# plt.tight_layout()


ElossMap_on, loss_on, mono_on = emiss2loss(np.transpose(RIXSonAVG), calibration[100:250], ReferenceEnergy)
ElossMap_off, loss_off, mono_off = emiss2loss(np.transpose(RIXSoffAVG), calibration[100:250], ReferenceEnergy)


plt.figure()
X, Y = np.meshgrid(ReferenceEnergy, loss_on)
plt.subplot(1, 1, 1)
plt.pcolor(X, Y, ElossMap_on, vmax=0.07)
plt.colorbar()
plt.xlabel('Mono Energy (eV)')
plt.ylabel('Energy Loss (eV)')
plt.title('DimerACN RIXS pumped 600fs')
plt.tight_layout()

plt.figure()
X, Y = np.meshgrid(ReferenceEnergy, loss_on)
plt.subplot(1, 1, 1)
plt.pcolor(X, Y, ElossMap_off, vmax=0.07)
plt.colorbar()
plt.xlabel('Mono Energy (eV)')
plt.ylabel('Energy Loss (eV)')
plt.title('DimerACN RIXS pumped 600fs')
plt.tight_layout()



