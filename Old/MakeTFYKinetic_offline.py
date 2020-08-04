import os
from matplotlib import pyplot as plt
import scipy.io as sp
import numpy as np
from Filter import FilterData
import pickle
import ProcessedDataClass as PDC
import RawDataClass as RDC
from scipy.special import erf
from scipy.optimize import curve_fit
from TimeCorrection import TimeCorrection


def errfunc_sigma(x, a, b, c, d):
    return a + b * erf((c - x) / (np.sqrt(2) * np.abs(d)))  # d is sigma, fwhm = 2.355 * sigma


def errfunc_fwhm(x, a, b, c, d):
    return a + b * erf((c - x) * 2 * np.sqrt(np.log(2)) / (np.abs(d)))  # d is fwhm


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

scans = [3]

scan_name = "RuDimerCl_timescan_0"
# scan_name = "RuDimerACN_monoscan_10ps_0"
# plt.figure()
for i in range(0, len(scans)):
    saveDir = "C:/Users/poult/Documents/Research/Beamtimes/SwissFEL_July_2019/Transfered_Data/Processed/RuDimerACN/Kinetic_Traces" \
              "/" + scan_name + '%02d/' % scans[i]
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
    # ReferenceTime =[-1.80025658e+00, -7.99653952e-01, -2.99685952e-01, -9.96987517e-02,
    #                 2.94848333e-04,  1.00288448e-01,  1.99615424e-01,  3.00275648e-01,
    #                 3.99602624e-01,  4.99596224e-01,  5.99589824e-01,  8.00243648e-01,
    #                 1.10022445e+00,  1.40020525e+00,  1.69951942e+00,  2.20015405e+00,
    #                 3.20009005e+00,  4.20002605e+00,  6.19989805e+00,  1.01996420e+01,
    #                 1.22001807e+01,  1.51999887e+01,  2.01996687e+01]
    # ReferenceTime = [-2.2, -1.2, -0.7, -0.5, -0.4, -0.3, -0.2, -0.1,  0. ,  0.1,  0.2,
    #     0.4,  0.7,  1. ,  1.3,  1.8,  2.8,  3.8,  5.8,  9.8, 19.8]
    # Time = ReferenceTime
    if saveProData is True:
        with open(saveDir + "xasprodata.pkl", "wb") as f:
            time_zero_mm = 156.3276
            xasrawdata = TimeCorrection(xasrawdata,time_zero_mm)
            xasprodata = FilterData(xasrawdata, False,time_zero_mm)

            delay_mm = np.empty(0)
            for ii in range(0, len(xasrawdata.delay_SH_pump)):
                delay = [x for x in xasrawdata.delay_SH_pump[ii] if x > 0]
                delay_mm = np.append(delay_mm, np.mean(delay[ii]))
            delay_ps = 1e12 * (delay_mm - time_zero_mm) * 2 * 1e-3 / (3e8)
            delays = np.array(delay_ps)
            xasprodata.changeValue(delays=delays)

            pickle.dump(xasprodata, f)
    Time = xasprodata.delays
    ReferenceTime = delay_ps.tolist()

    if loadProData is True:
        with open(saveDir + "xasprodata.pkl", "rb") as f:
            xasprodata = pickle.load(f)
    difference = np.subtract(xasprodata.DataFluo_pump_norm_total,xasprodata.DataFluo_unpump_norm_total)
    index = []
    for elements in range(0, len(xasprodata.delays)):
        Element = min(ReferenceTime, key=lambda var: abs(var - xasprodata.delays[elements]))
        index.append(ReferenceTime.index(Element))

    mult = len(Time)
    TFYpump.append([0] * mult)
    TFYunpump.append([0] * mult)
    TotalShotsPumped.append([0] * mult)
    TotalShotsUnpumped.append([0] * mult)
    TFY_Difference.append([0]*mult)
    for variable in range(0, len(index)):
        addVals = index[variable]
        TFYpump[i][addVals] = xasprodata.DataFluo_pump_norm_total[variable]
        TFYunpump[i][addVals] = xasprodata.DataFluo_unpump_norm_total[variable]
        TotalShotsPumped[i][addVals] = xasprodata.shotspostfilterpump[variable]
        TotalShotsUnpumped[i][addVals] = xasprodata.shotspostfilterunpump[variable]
        TFY_Difference[i][addVals] = difference[variable]

    # plt.plot(ReferenceTime,TFY_Difference[i],label=i)
# plt.legend()
Energy = np.asarray(Energy)
TFYpump = np.asarray(TFYpump)
TFYunpump = np.asarray(TFYunpump)
PumpErrHigh = np.asarray(PumpErrHigh)
PumpErrLow = np.asarray(PumpErrLow)
UnPumpErrHigh = np.asarray(UnPumpErrHigh)
UnPumpErrLow = np.asarray(UnPumpErrLow)
TotalShotsPumped = np.asarray(TotalShotsPumped)
TotalShotsUnpumped = np.asarray(TotalShotsUnpumped)
TFY_Difference = np.asarray(TFY_Difference)
# norm1 = np.trapz(TFYunpump[0][10:45])
# norm2 = np.trapz(TFYunpump[1][10:45])
# plt.figure()
# plt.plot(Energy, np.divide(TFYunpump[0],norm1))
# plt.plot(Energy, np.divide(TFYunpump[1],norm2))



# TFYunpump[TFYunpump == 0] = np.nan
# TFYpump[TFYpump == 0] = np.nan
# PumpErrHigh[PumpErrHigh == 0] = np.nan
# PumpErrLow[PumpErrLow == 0] = np.nan
# UnPumpErrHigh[UnPumpErrHigh == 0] = np.nan
# UnPumpErrLow[UnPumpErrLow == 0] = np.nan
# TFY_Difference[TFY_Difference == 0] = np.nan
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
parameters, extras = curve_fit(errfunc_fwhm,xasprodata.delays , TFY_Difference, p0=[-0.03, -0.01, 0, 0.25])

print("Position t0 =", np.round(parameters[2], 5), "ps")
print("Width =", np.abs(np.round(parameters[3], 3)) * 1000, "fs")

plt.figure()
plt.plot(xasprodata.delays, errfunc_fwhm(xasprodata.delays,*parameters),color='red',label='fit')
plt.plot(xasprodata.delays, TFY_Difference,color='blue',label='KineticTrace')
plt.title("fit is: "+ np.str(np.round(parameters[2], 5)) +"ps")
plt.legend()
plt.xlabel('Time (ps)')
plt.ylabel('absorption')

Dir = 'C:/Users/poult/Documents/Research/Beamtimes/SwissFEL_July_2019/Transfered_Data/Processed/RuDimerACN/TFY' \
      '/600fs/'
save = True
XASAveraged = PDC.XASAveraged()
XASAveraged.changeValue(Averaged_Spectrum_unpumped=TFYunpump, Scans_in_average=scans,
                        Shots_Per_Point_unpumped=TotalShotsUnpumped, Energy=Energy)
if save:
    with open(Dir + "Pumped_Averaged_600fs.pkl", "wb") as f:
        pickle.dump(XASAveraged, f)
    sp.savemat('C:/Users/poult/Documents/Research/Beamtimes/SwissFEL_July_2019/Transfered_Data/Dec-06-2019/DimerACN/Kinetic_Trace_2842.0eV.mat',
               mdict={'Kinetic_Trace_C': TFY_Difference, 'TotalShots_pumped_C': TotalShotsPumped,
                      'TotalShots_unpumped_C': TotalShotsUnpumped,'All_Scans_C': full_list,'Times':ReferenceTime})
#
