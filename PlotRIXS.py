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

scans = [7,9,10]
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

RIXS_on, RIXS_off, xasrawdata = plotRIXS(scans, base, dirxas, dirrixs, False)
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
ElossMap_on, loss_on, mono_on = emiss2loss(RIXS_on, calibration, xasrawdata.Energy)
ElossMap_off, loss_off, mono_off = emiss2loss(RIXS_off, calibration, xasrawdata.Energy)

plt.figure()
X, Y = np.meshgrid(xasrawdata.Energy, calibration)
plt.subplot(2, 1, 1)
plt.pcolor(X, Y, RIXS_on, vmax=0.1)
plt.colorbar()
plt.xlabel('Mono Energy (eV)')
plt.ylabel('Emission Energy (eV)')
plt.title('DimerACN RIXS pumped 10ps')
plt.tight_layout()

plt.figure()
X, Y = np.meshgrid(xasrawdata.Energy, loss_on)
plt.subplot(2, 1, 1)
plt.pcolor(X, Y, ElossMap_on, vmax=0.1)
plt.colorbar()
plt.xlabel('Mono Energy (eV)')
plt.ylabel('Energy Loss (eV)')
plt.title('DimerACN RIXS pumped 600fs')
plt.tight_layout()

rixsprodata = PDC.RIXSProData()
rixsprodata.changeValue(Elosspumped=ElossMap_on, Elossunpumped=ElossMap_off, emissionAxis=calibration, lossAxis=loss_on)

sp.savemat('C:/Users/poult/Documents/Research/Beamtimes/SwissFEL_July_2019/Transfered_Data/10psRIXS.mat',
           mdict= {'RIXSpumped':RIXS_on,'RIXSunpumped':RIXS_off,'Elosspumped':ElossMap_on, 'Elossunpumped':ElossMap_off, 'emissionAxis':calibration, 'lossAxis':loss_on,\
                   'mono':xasrawdata.Energy})

