import os
from matplotlib import pyplot as plt
import scipy.io as sp
import numpy as np
from Filter import FilterData
import pickle
import ProcessedDataClass as PDC
import RawDataClass as RDC

# Set the scan name and the directories of the scan and its json file
Energy = []
TFYpump = []
TFYunpump = []
PumpErrHigh = []
PumpErrLow = []
UnPumpErrHigh = []
UnPumpErrLow = []
TotalShotsPumped = []
TotalShotsUnpumped = []

scans = [6,7,9,10,11,12,14,15,16,18,19,20]

scan_name = "RuDimerACN_monoscan_0p6ps_0"
for i in range(0, len(scans)):
    saveDir = "C:/Users/poult/Documents/Research/Beamtimes/SwissFEL_July_2019/Transfered_Data/Processed/RuDimerACN/TFY" \
              "/600fs/" + scan_name + '%02d/' % scans[i]
    if not os.path.isdir(saveDir):
        os.mkdir(saveDir)

    exists = os.path.isfile(saveDir + 'xasrawdata.pkl')
    if not exists:
        print('The File Does Not Exist.')
    elif exists:
        with open(saveDir + "xasrawdata.pkl", "rb") as f:
            xasrawdata = pickle.load(f)

    saveProData = False
    loadProData = False
    xasprodata = FilterData(xasrawdata, False)
    ReferenceEnergy = [2852.0, 2851.0, 2850.0, 2849.0, 2848.0, 2847.0, 2846.5, 2846.0, 2845.5, 2845.0, 2844.75, 2844.5,
                       2844.25, 2844.0,
                       2843.75, 2843.5, 2843.25, 2843.0, 2842.75, 2842.5, 2842.25, 2842.0, 2841.75, 2841.5, 2841.25,
                       2841.0, 2840.75, 2840.5,
                       2840.25, 2840.0, 2839.75, 2839.5, 2839.25, 2839.0, 2838.75, 2838.5, 2838.25, 2838.0, 2837.75,
                       2837.5, 2837.25, 2837.0,
                       2836.75, 2836.5, 2836.25, 2836.0, 2835.75, 2835.5, 2835.25, 2835.0, 2834.5, 2834.0, 2833.0,
                       2832.0, 2831.0]
    Energy = ReferenceEnergy
    if saveProData is True:
        with open(saveDir + "xasprodata.pkl", "wb") as f:
            pickle.dump(xasprodata, f)

    if loadProData is True:
        with open(saveDir + "xasprodata.pkl", "rb") as f:
            x = pickle.load(f)

    err_pump_high = xasprodata.DataFluo_pump_norm_total + xasprodata.error_pump
    err_pump_low = xasprodata.DataFluo_pump_norm_total - xasprodata.error_pump
    err_unpump_high = xasprodata.DataFluo_unpump_norm_total + xasprodata.error_unpump
    err_unpump_low = xasprodata.DataFluo_unpump_norm_total - xasprodata.error_unpump
    index = []
    for elements in range(0,len(xasrawdata.Energy)):
        Element = min(ReferenceEnergy, key=lambda var: abs(var - xasrawdata.Energy[elements]))
        index.append(ReferenceEnergy.index(Element))

    TFYpump.append([0] * 55)
    TFYunpump.append([0] * 55)
    PumpErrHigh.append([0] * 55)
    PumpErrLow.append([0] * 55)
    UnPumpErrHigh.append([0] * 55)
    UnPumpErrLow.append([0] * 55)
    TotalShotsPumped.append([0]*55)
    TotalShotsUnpumped.append([0]*55)
    for variable in range(0,len(index)):
        addVals = index[variable]
        TFYpump[i][addVals] = xasprodata.DataFluo_pump_norm_total[variable]
        TFYunpump[i][addVals] = xasprodata.DataFluo_unpump_norm_total[variable]
        PumpErrHigh[i][addVals] = err_pump_high[variable]
        PumpErrLow[i][addVals] = err_pump_low[variable]
        UnPumpErrHigh[i][addVals] = err_unpump_high[variable]
        UnPumpErrLow[i][addVals] = err_unpump_low[variable]
        TotalShotsPumped[i][addVals] = xasprodata.shotspostfilterpump[variable]
        TotalShotsUnpumped[i][addVals] = xasprodata.shotspostfilterunpump[variable]

Energy = np.asarray(Energy)
TFYpump = np.asarray(TFYpump)
TFYunpump = np.asarray(TFYunpump)
PumpErrHigh = np.asarray(PumpErrHigh)
PumpErrLow = np.asarray(PumpErrLow)
UnPumpErrHigh = np.asarray(UnPumpErrHigh)
UnPumpErrLow = np.asarray(UnPumpErrLow)
TotalShotsPumped = np.asarray(TotalShotsPumped)
TotalShotsUnpumped = np.asarray(TotalShotsUnpumped)


TFYunpump[TFYunpump == 0] = np.nan
TFYpump[TFYpump == 0] = np.nan
PumpErrHigh[PumpErrHigh == 0] = np.nan
PumpErrLow[PumpErrLow == 0] = np.nan
UnPumpErrHigh[UnPumpErrHigh == 0] = np.nan
UnPumpErrLow[UnPumpErrLow == 0] = np.nan
avgs = TFYunpump.shape[0]

TFYpump = np.nanmean(TFYpump, axis=0)
TFYunpump = np.nanmean(TFYunpump, axis=0)
PumpErrHigh = np.nanmean(PumpErrHigh, axis=0)
PumpErrLow = np.nanmean(PumpErrLow, axis=0)
UnPumpErrHigh = np.nanmean(UnPumpErrHigh, axis=0)
UnPumpErrLow = np.nanmean(UnPumpErrLow, axis=0)
TotalShotsPumped = np.sum(TotalShotsPumped, axis=0)
TotalShotsUnpumped = np.sum(TotalShotsUnpumped, axis=0)


plt.figure()
plt.plot(Energy, TFYpump, color='blue', label='Pumped')
plt.fill_between(Energy, PumpErrHigh, PumpErrLow, alpha=0.3, color='blue')
plt.plot(Energy, TFYunpump, color='orange', label='UnPumped')
plt.fill_between(Energy, UnPumpErrHigh, UnPumpErrLow, alpha=0.3, color='orange')
plt.xlabel('energy (eV)')
plt.ylabel('absorption')
plt.title('XAS')
plt.legend()

plt.figure()
plt.plot(Energy, np.divide(TFYpump - TFYunpump, TFYunpump))
plt.xlabel('energy (eV)')
plt.ylabel('absorption')
