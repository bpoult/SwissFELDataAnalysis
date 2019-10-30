import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import pickle
import RawDataClass as RDC
import ProcessedDataClass as PDC
from Looking_at_RIXS import plotRIXS

scans = [10, 11, 12]
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

RIXS_on, RIXS_off, xasrawdata = plotRIXS(scans, base, dirxas, dirrixs, False)
RIXS_on = np.ndarray.transpose(RIXS_on)
X, Y = np.meshgrid(xasrawdata.Energy,calibration)
plt.subplot(2, 1, 1)
plt.pcolor(X, Y, RIXS_on, vmax=0.1)
plt.colorbar()
plt.xlabel('Mono Energy (eV)')
plt.ylabel('Emission Energy (eV)')
plt.title('DimerACN RIXS pumped 10ps')
plt.tight_layout()
