import numpy as np
import pickle
from TimeCorrection import TimeCorrection
from matplotlib import pyplot as plt
from Filter import FilterData
from scipy.special import erf
from scipy.optimize import curve_fit
from TimeCorrection import ps_to_mm






dirxas = "C:/Users/poult/Documents/Research/Beamtimes/SwissFEL_July_2019/Transfered_Data/Processed/RuDimerACN/TFY" \
         "/600fs/"
dirrixs = "C:/Users/poult/Documents/Research/Beamtimes/SwissFEL_July_2019/Transfered_Data/Processed/RuDimerACN" \
          "/RIXS/600fs/roi2/"
scans = [6, 7, 9, 10, 11, 12, 14, 16, 17, 18, 20]
base = "RuDimerACN_monoscan_0p6ps_0"
RIXSon = []
RIXSoff = []
allTimes = []
test = []
biglist = []
time_zero_mm_original = 156.3276
time_zero_mm = 156.3276
for i in range(0, len(scans)):
    basename = base + '%02d/' % scans[i]
    with open(dirxas + basename + "xasrawdata.pkl", "rb") as f:
        xasrawdata = pickle.load(f)
    x = scans[i]
    if x == 6 or x == 7:
        time_zero_mm = time_zero_mm_original + ps_to_mm(0.17995)
    if x == 9:
        time_zero_mm = time_zero_mm_original + ps_to_mm(-0.2083)
    if x == 10 or x == 11 or x == 12 or x == 14:
        time_zero_mm = time_zero_mm_original + ps_to_mm(-0.34772)
    if x == 16 or x == 17 or x == 18 or x == 20:
        time_zero_mm = time_zero_mm_original + ps_to_mm(-0.02141)

    print(time_zero_mm)
    xasprodata = FilterData(xasrawdata, False, time_zero_mm)
    # plt.figure()
    # plt.title(scans[i])
    # plt.xlabel("time (ps)")
    # plt.ylabel("number of shots")
    # plt.hist(xasprodata.time_delay_ps_total[xasprodata.time_delay_ps_total>0],100,color='red')

    biglist= np.append(biglist, xasprodata.time_delay_ps_total)
plt.figure()
plt.title("All Scans Combined")
plt.xlabel('time (ps)')
plt.ylabel('number of shots')
plt.hist(biglist[biglist>0], 1000,color='blue')
print(len(biglist))
print(len(biglist[biglist>0]))


# Now fit with error funciton (defined above)


