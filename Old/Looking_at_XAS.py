import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import pickle
import RawDataClass as RDC
import ProcessedDataClass as PDC

scans = [7,9]
XASon = []
XASoff = []
for i in range(0, len(scans)):
    basename = "RuDimerACN_monoscan_0p6ps_0" + '%02d/' % scans[i]
    dirxas = "C:/Users/poult/Documents/Research/Beamtimes/SwissFEL_July_2019/Transfered_Data/Processed/RuDimerACN/TFY" \
             "/600fs/"
    dirrixs = "C:/Users/poult/Documents/Research/Beamtimes/SwissFEL_July_2019/Transfered_Data/Processed/RuDimerACN" \
              "/RIXS/600fs/"
    with open(dirxas + basename + "xasprodata.pkl", "rb") as f:
        xasprodata = pickle.load(f)
    XASon.append(xasprodata.DataFluo_pump_norm_total)
    XASoff.append(xasprodata.DataFluo_unpump_norm_total)

XASon = np.asarray(XASon)
XASoff = np.asarray(XASoff)

XASonTot = np.zeros(55)
XASoffTot = np.zeros(55)
for i in range(0, len(XASoff)):
    XASonTot = XASon[i] + XASonTot
    XASoffTot = XASoff[i] + XASoffTot

XASonAVG = XASonTot / len(XASon)
XASoffAVG = XASoffTot / len(XASoff)

plt.figure()
plt.plot(xasprodata.Energy, XASonAVG,label='Pumped')
plt.plot(xasprodata.Energy, XASoffAVG,label='UnPumped')
plt.xlabel('energy (eV)')
plt.ylabel('absorption')
plt.title('RuDimerACN, 600fs, XAS')
plt.legend()

plt.figure()
plt.plot(xasprodata.Energy, XASoffAVG-XASonAVG ,label='Unpumped - Pumped')
plt.xlabel('energy (eV)')
plt.ylabel('absorption')
plt.title('RuDimerACN, 600fs, XAS Difference')
plt.legend()