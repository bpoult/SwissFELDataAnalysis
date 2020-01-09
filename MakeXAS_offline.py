import os
from matplotlib import pyplot as plt
import scipy.io as sp
import numpy as np
from Filter import FilterData
import pickle
import ProcessedDataClass as PDC
import RawDataClass as RDC
from TimeCorrection import ps_to_mm

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
TFY_Difference = []

scans = [6, 7, 9, 10, 11, 12, 14, 16, 17, 18, 20]
time_zero_mm_original = 156.3276
# scan_name = "RuDimerCl_monoscan_0p6ps_0"
scan_name = "RuDimerACN_monoscan_0p6ps_0"
plt.figure()
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

    saveProData = True
    loadProData = False
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
            x = scans[i]
            if x == 6 or x == 7:
                time_zero_mm = time_zero_mm_original + ps_to_mm(0.17995)
            if x == 9:
                time_zero_mm = time_zero_mm_original + ps_to_mm(-0.2083)
            if x == 10 or x == 11 or x == 12 or x == 14:
                time_zero_mm = time_zero_mm_original + ps_to_mm(-0.34772)
            if x == 16 or x == 17 or x == 18 or x == 20:
                time_zero_mm = time_zero_mm_original + ps_to_mm(-0.02141)
            xasprodata = FilterData(xasrawdata, False,time_zero_mm)
            pickle.dump(xasprodata, f)

    if loadProData is True:
        with open(saveDir + "xasprodata.pkl", "rb") as f:
            xasprodata = pickle.load(f)
    difference = np.divide(np.subtract(xasprodata.DataFluo_pump_norm_total,xasprodata.DataFluo_unpump_norm_total),
                           xasprodata.DataFluo_unpump_norm_total)
    index = []
    for elements in range(0, len(xasrawdata.Energy)):
        Element = min(ReferenceEnergy, key=lambda var: abs(var - xasrawdata.Energy[elements]))
        index.append(ReferenceEnergy.index(Element))



    TFYpump.append([0] * 55)
    TFYunpump.append([0] * 55)
    PumpErrHigh.append([0] * 55)
    PumpErrLow.append([0] * 55)
    UnPumpErrHigh.append([0] * 55)
    UnPumpErrLow.append([0] * 55)
    TotalShotsPumped.append([0] * 55)
    TotalShotsUnpumped.append([0] * 55)
    TFY_Difference.append([0]*55)
    for variable in range(0, len(index)):
        addVals = index[variable]
        TFYpump[i][addVals] = xasprodata.DataFluo_pump_norm_total[variable]
        TFYunpump[i][addVals] = xasprodata.DataFluo_unpump_norm_total[variable]
        TotalShotsPumped[i][addVals] = xasprodata.shotspostfilterpump[variable]
        TotalShotsUnpumped[i][addVals] = xasprodata.shotspostfilterunpump[variable]
        TFY_Difference[i][addVals] = difference[variable]
    plt.plot(Energy,TFYunpump[i])
Energy = np.asarray(Energy)
TFYpump = np.asarray(TFYpump)
TFYunpump = np.asarray(TFYunpump)
TotalShotsPumped = np.asarray(TotalShotsPumped)
TotalShotsUnpumped = np.asarray(TotalShotsUnpumped)
TFY_Difference = np.asarray(TFY_Difference)

# norm1 = np.trapz(TFYunpump[0][10:45])
# norm2 = np.trapz(TFYunpump[1][10:45])
# plt.figure()
# plt.plot(Energy, np.divide(TFYunpump[0],norm1))
# plt.plot(Energy, np.divide(TFYunpump[1],norm2))



TFYunpump[TFYunpump == 0] = np.nan
TFYpump[TFYpump == 0] = np.nan
TFY_Difference[TFY_Difference == 0] = np.nan
avgs = TFYunpump.shape[0]
full_list = TFY_Difference.copy()
TFYpump = np.nanmean(TFYpump, axis=0)
TFYunpump = np.nanmean(TFYunpump, axis=0)
PumpErrHigh = np.nanmean(PumpErrHigh, axis=0)
PumpErrLow = np.nanmean(PumpErrLow, axis=0)
UnPumpErrHigh = np.nanmean(UnPumpErrHigh, axis=0)
UnPumpErrLow = np.nanmean(UnPumpErrLow, axis=0)
TotalShotsPumped = np.sum(TotalShotsPumped, axis=0)
TotalShotsUnpumped = np.sum(TotalShotsUnpumped, axis=0)
TFY_Difference = np.nanmean(TFY_Difference,axis=0)

# plt.figure()
# plt.plot(Energy, TFYpump, color='blue', label='Pumped')
# plt.fill_between(Energy, PumpErrHigh, PumpErrLow, alpha=0.3, color='blue')
# plt.plot(Energy, TFYunpump, color='orange', label='UnPumped')
# plt.fill_between(Energy, UnPumpErrHigh, UnPumpErrLow, alpha=0.3, color='orange')
# plt.xlabel('energy (eV)')
# plt.ylabel('absorption')
# plt.title('XAS')
# plt.legend()

plt.figure()
plt.plot(Energy, TFY_Difference)
plt.xlabel('energy (eV)')
plt.ylabel('absorption')



Dir = 'C:/Users/poult/Documents/Research/Beamtimes/SwissFEL_July_2019/Transfered_Data/Processed/RuDimerACN/TFY' \
      '/600fs/'
save = False
XASAveraged = PDC.XASAveraged()
XASAveraged.changeValue(Averaged_Spectrum_unpumped=TFYunpump, Scans_in_average=scans,
                        Shots_Per_Point_unpumped=TotalShotsUnpumped, Energy=Energy)
if save:
    with open(Dir + "Pumped_Averaged_600fs.pkl", "wb") as f:
        pickle.dump(XASAveraged, f)
    sp.savemat('C:/Users/poult/Documents/Research/Beamtimes/SwissFEL_July_2019/Transfered_Data/Dec-05-2019/DimerCl/600fs_DifferenceSpectra_All.mat',
               mdict={'Difference_600fs_All': TFY_Difference, 'TotalShots_600fs_All_pumped': TotalShotsPumped,
                      'TotalShots_600fs_All_unpumped': TotalShotsUnpumped,'Energy': Energy,'All_Scans_600fs_All': full_list})
#
