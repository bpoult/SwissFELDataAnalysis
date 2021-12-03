import numpy as np
import scipy.io as sp
import matplotlib.pyplot as plt
import pickle
import RawDataClass as RDC
import ProcessedDataClass as PDC
from Looking_at_RIXS import plotRIXS
from EmissionToLoss import emiss2loss

basename = "XES_RuDimerCl_2837.0eV_10ps"
dirxas = "C:/Users/poult/Documents/Research/Beamtimes/SwissFEL_July_2019/Transfered_Data/Processed/JF_corrected/RuDimerCl/XES/Bootstrapped/10ps/"
dirxes = "C:/Users/poult/Documents/Research/Beamtimes/SwissFEL_July_2019/Transfered_Data/Processed/JF_corrected/RuDimerCl/XES/Bootstrapped/10ps/"
with open(dirxas + basename + "/rawdata.pkl", "rb") as f:
    xasprodata = pickle.load(f)
with open(dirxes + basename + "/rixsprodata_roi2.pkl", "rb") as f:
    xesprodata = pickle.load(f)
with open('JF_Lalpha_Calibration_3.txt') as f:
    w = [float(x) for x in next(f).split()]  # read first line
    calibration = []
    for line in f:  # read rest of lines
        calibration.append([float(x) for x in line.split()])
calibration = np.asarray(calibration)
calibration = calibration.flatten()

XES_on = xesprodata.RIXS_map_pumped
XES_off = xesprodata.RIXS_map_unpumped
error_on = xesprodata.RIXS_map_pumped_err
error_off = xesprodata.RIXS_map_unpumped_err
num_scans = len(xesprodata.RIXS_map_pumped)


# plt.figure()
# plt.plot(calibration[100:250], XES_on)
# plt.plot(calibration[100:250], XES_off)
# plt.figure()
# plt.plot(calibration[100:250],(XES_on-XES_off))

SaveThis = True
if SaveThis is True:

    sp.savemat('C:/Users/poult/Documents/Research/Beamtimes/SwissFEL_July_2019/Transfered_Data/Matlab_Files/Dec-2-2021/RuDimerCl_10ps_XES_2837eV_on.mat',
               mdict= {'E_emi':calibration[100:250],'XES_on':XES_on,'Error_on':error_on})

    sp.savemat('C:/Users/poult/Documents/Research/Beamtimes/SwissFEL_July_2019/Transfered_Data/Matlab_Files/Dec-2-2021/RuDimerCl_10ps_XES_2837eV_off.mat',
               mdict= {'E_emi':calibration[100:250],'XES_off':XES_off,'Error_off':error_off})