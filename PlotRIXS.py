import numpy as np
import scipy.io as sp
import os
import sys
import matplotlib.pyplot as plt
import pickle
import RawDataClass as RDC
import ProcessedDataClass as PDC
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
scans = [6,7,10,11,12,15,16,18,20]
base = "RuDimerACN_monoscan_0p6ps_0"

dirxas = "C:/Users/poult/Documents/Research/Beamtimes/SwissFEL_July_2019/Transfered_Data/Processed/RuDimerACN/TFY" \
         "/600fs/"
dirrixs = "C:/Users/poult/Documents/Research/Beamtimes/SwissFEL_July_2019/Transfered_Data/Processed/RuDimerACN" \
          "/RIXS/600fs/roi2/"

with open('JF_Lalpha_Calibration.txt') as f:
    w = [float(x) for x in next(f).split()]  # read first line
    calibration = []
    for line in f:  # read rest of lines
        calibration.append([float(x) for x in line.split()])
calibration = np.asarray(calibration)
calibration = calibration.flatten()

# RIXS_on, RIXS_off, xasrawdata,herfd_pumped, herfd_unpumped,herfd_Difference = plotRIXS(scans, base, dirxas, dirrixs, False)
# plt.figure()
# plt.plot(ReferenceEnergy,herfd_pumped,label='Pumped')
# plt.plot(ReferenceEnergy,herfd_unpumped,label='UnPumped')
# plt.legend()

plt.figure()
plt.plot(ReferenceEnergy,herfd_pumped-herfd_unpumped)

RIXS_on = np.ndarray.transpose(RIXS_on)
RIXS_off = np.ndarray.transpose(RIXS_off)

# loss_step = float(calibration[1] - calibration[0])
# loss_min = np.amin(xasrawdata.Energy) - np.amax(calibration)
# loss_max = np.amax(xasrawdata.Energy) - np.amin(calibration)
# loss_step = np.round((np.amax(calibration)-np.amin(calibration))/len(calibration),1)
# loss_min = np.round(np.amin(xasrawdata.Energy)-np.amax(calibration),1)
# loss_max = np.round(np.amax(xasrawdata.Energy)-np.amin(calibration),1)
#
# loss = np.arange(loss_min,loss_max, loss_step)
# loss = np.sort(loss)
# rixsmap2 = np.zeros((len(loss), len(xasrawdata.Energy)))
# for i in np.arange(len(xasrawdata.Energy)):
#     loss0 = xasrawdata.Energy[i] - calibration
#     rixs0 = RIXS_on[:, i]
#     rixsmap2[:, i] = np.interp(loss,loss0,rixs0, left=0, right=0)
ElossMap_on, loss_on, mono_on = emiss2loss(RIXS_on, calibration, ReferenceEnergy)
ElossMap_off, loss_off, mono_off = emiss2loss(RIXS_off, calibration, ReferenceEnergy)

plt.figure()
X, Y = np.meshgrid(ReferenceEnergy, calibration)
plt.subplot(2, 1, 1)
plt.pcolor(X, Y, RIXS_on, vmax=0.1)
plt.colorbar()
plt.xlabel('Mono Energy (eV)')
plt.ylabel('Emission Energy (eV)')
plt.title('DimerACN RIXS pumped 10ps')
plt.tight_layout()

plt.figure()
X, Y = np.meshgrid(ReferenceEnergy, loss_on)
plt.subplot(2, 1, 1)
plt.pcolor(X, Y, ElossMap_on, vmax=0.1)
plt.colorbar()
plt.xlabel('Mono Energy (eV)')
plt.ylabel('Energy Loss (eV)')
plt.title('DimerACN RIXS pumped 600fs')
plt.tight_layout()

SaveThis = True
if SaveThis is True:
    rixsprodata = PDC.RIXSProData()
    rixsprodata.changeValue(Elosspumped=ElossMap_on, Elossunpumped=ElossMap_off, emissionAxis=calibration, lossAxis=loss_on)

    sp.savemat('C:/Users/poult/Documents/Research/Beamtimes/SwissFEL_July_2019/Transfered_Data/Feb-10-2020/RuDimerACN.mat',
               mdict= {'RIXSpumped_600fs':RIXS_on,'RIXS':RIXS_off,'Elosspumped_600fs':ElossMap_on,
                       'Elossunpumped_600fs':ElossMap_off, 'emission':calibration, 'lossAxis_600fs':loss_on,
                       'x':ReferenceEnergy})

