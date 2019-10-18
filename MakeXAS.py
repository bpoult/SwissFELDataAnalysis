import sys
sys.path.insert(0, '/das/work/p17/p17983/SwissFEL19DA/PostExperiment/Ben/jfut/')
import jungfrau_utils as jf
sys.path.insert(0, '/das/work/p17/p17983/')
import numpy as np
import json
import os
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from alvra_tools.load_data import *
from alvra_tools.channels import *
from alvra_tools.utils import errfunc_sigma, errfunc_fwhm
from LoadData import LoadData
from Filter import FilterData
import pickle


# Set the scan name and the directories of the scan and its json file
scan_name = "XES_2842.0eV_600fs"

saveDir = "/das/work/p17/p17983/SwissFEL19DA/PostExperiment/Ben/Processed/RuDimerACN/XES/600fs/" + scan_name + "/"
if not os.path.isdir(saveDir):
    os.mkdir(saveDir)

exists = os.path.isfile(saveDir + 'xasrawdata.pkl')
if not exists:
    xasrawdata = LoadData(scan_name,False,True)
    with open(saveDir + "xasrawdata.pkl", "wb") as f:
        pickle.dump(xasrawdata, f)
        
        
elif exists:
    with open(saveDir + "xasrawdata.pkl", "rb") as f:
        xasrawdata = pickle.load(f)


saveProData = True
loadProData = False

xasprodata = FilterData(xasrawdata,True)

err_pump_high = xasprodata.DataFluo_pump_norm_total + xasprodata.error_pump
err_pump_low = xasprodata.DataFluo_pump_norm_total - xasprodata.error_pump
err_unpump_high = xasprodata.DataFluo_unpump_norm_total + xasprodata.error_unpump
err_unpump_low = xasprodata.DataFluo_unpump_norm_total - xasprodata.error_unpump

plt.figure()
plt.plot(xasprodata.Energy, xasprodata.DataFluo_pump_norm_total,color = 'blue',label='Pumped')
plt.fill_between(xasprodata.Energy,err_pump_high,err_pump_low,alpha = 0.3, color = 'blue')
plt.plot(xasprodata.Energy, xasprodata.DataFluo_unpump_norm_total,color = 'orange',label='UnPumped')
plt.fill_between(xasprodata.Energy,err_unpump_high,err_unpump_low,alpha = 0.3, color = 'orange')
plt.xlabel('energy (eV)')
plt.ylabel('absorption')
plt.title('XAS_'+ scan_name)
plt.legend()


if saveProData is True:
        with open(saveDir + "xasprodata.pkl", "wb") as f:
            pickle.dump(xasprodata, f)
            
if loadProData is True:
    with open(saveDir + "xasprodata.pkl", "rb") as f:
        x = pickle.load(f)