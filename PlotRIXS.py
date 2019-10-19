import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import pickle
import RawDataClass as RDC
import ProcessedDataClass as PDC
from Looking_at_RIXS import plotRIXS

scansvert = [10, 11, 12]
base = "RuDimerACN_monoscan_0p6ps_0"

dirxas = "C:/Users/poult/Documents/Research/Beamtimes/SwissFEL_July_2019/Transfered_Data/Processed/RuDimerACN/TFY" \
         "/600fs/"
dirrixs = "C:/Users/poult/Documents/Research/Beamtimes/SwissFEL_July_2019/Transfered_Data/Processed/RuDimerACN" \
          "/RIXS/600fs/roi2/"

RIXS_on_vert, RIXS_off_vert, xasrawdata_vert = plotRIXS(scansvert, base, dirxas, dirrixs, False)

scanshor = [13,10,8]
base = "RuDimerACN_monoscan_10ps_0"

dirxas = "C:/Users/poult/Documents/Research/Beamtimes/SwissFEL_July_2019/Transfered_Data/Processed/RuDimerACN/TFY" \
         "/10ps/"
dirrixs = "C:/Users/poult/Documents/Research/Beamtimes/SwissFEL_July_2019/Transfered_Data/Processed/RuDimerACN" \
          "/RIXS/10ps/"
RIXS_on_hor, RIXS_off_hor, xasrawdata_hor = plotRIXS(scanshor, base, dirxas, dirrixs, False)

X, Y = np.meshgrid(np.linspace(0, RIXS_on_hor.shape[1], RIXS_on_hor.shape[1] + 1), xasrawdata_vert.Energy)
plt.figure()
plt.subplot(2, 1, 1)
plt.pcolor(X, Y, RIXS_on_vert, vmax=0.05)
plt.colorbar()
plt.xlabel('JF pixel')
plt.ylabel('Mono Energy (eV)')
plt.title('DimerACN RIXS pumped-unpumped 10ps')
plt.tight_layout()
#
X, Y = np.meshgrid(np.linspace(0, RIXS_on_hor.shape[1], RIXS_on_hor.shape[1] + 1), xasrawdata_vert.Energy)
plt.figure()
plt.subplot(2, 1, 1)
plt.pcolor(X, Y, RIXS_off_vert, vmax=0.05)
plt.colorbar()
plt.xlabel('JF pixel')
plt.ylabel('Mono Energy (eV)')
plt.title('DimerACN RIXS pumped-unpumped 10ps')
plt.tight_layout()

X, Y = np.meshgrid(np.linspace(0, RIXS_on_hor.shape[1], RIXS_on_hor.shape[1] + 1), xasrawdata_vert.Energy)
plt.figure()
plt.subplot(2, 1, 1)
plt.pcolor(X, Y, RIXS_on_vert-RIXS_off_vert, vmax=0.05)
plt.colorbar()
plt.xlabel('JF pixel')
plt.ylabel('Mono Energy (eV)')
plt.title('DimerACN RIXS pumped-unpumped 10ps')
plt.tight_layout()

X, Y = np.meshgrid(np.linspace(0, RIXS_on_hor.shape[1], RIXS_on_hor.shape[1] + 1), xasrawdata_vert.Energy)
plt.figure()
plt.subplot(2, 1, 1)
plt.pcolor(X, Y, RIXS_on_vert-RIXS_on_hor, vmax=0.05)
plt.colorbar()
plt.xlabel('JF pixel')
plt.ylabel('Mono Energy (eV)')
plt.title('DimerACN RIXS pumped-unpumped 10ps')
plt.tight_layout()

plt.figure()
plt.plot(xasrawdata_hor.Energy,np.sum(RIXS_on_vert-RIXS_off_vert,axis=1))
plt.plot(xasrawdata_hor.Energy,np.sum(RIXS_on_hor-RIXS_off_hor,axis=1))
plt.show()
