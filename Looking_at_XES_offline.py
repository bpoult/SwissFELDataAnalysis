import numpy as np
import scipy.io as sp
import matplotlib.pyplot as plt
import pickle
import RawDataClass as RDC
import ProcessedDataClass as PDC
from Looking_at_RIXS import plotRIXS
from EmissionToLoss import emiss2loss

basename = "XES_2842.0eV_10ps"
dirxas = "C:/Users/poult/Documents/Research/Beamtimes/SwissFEL_July_2019/Transfered_Data/Processed/RuDimerACN/XES" \
         "/10ps/"
dirxes = "C:/Users/poult/Documents/Research/Beamtimes/SwissFEL_July_2019/Transfered_Data/Processed/RuDimerACN" \
         "/XES/10ps/"
with open(dirxas + basename + "/xasprodata.pkl", "rb") as f:
    xasprodata = pickle.load(f)
with open(dirxas + basename + "/xasrawdata.pkl", "rb") as f:
    xasrawdata = pickle.load(f)
with open(dirxes + basename + "/roi2/xesprodata.pkl", "rb") as f:
    xesprodata = pickle.load(f)
with open('JF_Lalpha_Calibration.txt') as f:
    w = [float(x) for x in next(f).split()]  # read first line
    calibration = []
    for line in f:  # read rest of lines
        calibration.append([float(x) for x in line.split()])
calibration = np.asarray(calibration)
calibration = calibration.flatten()

XES_on = np.mean(xesprodata.RIXS_map_pumped, axis=0)
XES_off = np.mean(xesprodata.RIXS_map_unpumped, axis=0)
std_on = np.std(xesprodata.RIXS_map_pumped, axis=0)
std_off = np.std(xesprodata.RIXS_map_unpumped, axis=0)
error_on = std_on/len(xesprodata.RIXS_map_pumped)
error_off = std_off/len(xesprodata.RIXS_map_unpumped)
XES_Difference = np.nanmean(xesprodata.XES_Difference, axis=0)
XES_Difference[np.isnan(XES_Difference)] = 0
num_scans = len(xesprodata.RIXS_map_pumped)


plt.figure()
plt.plot(calibration, XES_on)
plt.plot(calibration, XES_off)
plt.figure()
plt.plot(XES_on-XES_off)
