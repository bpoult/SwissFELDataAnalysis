# This is a copy of the First XAS python notebook.

import sys
sys.path.insert(0, '/das/work/p17/p17983/')

import numpy as np
import json
import os
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

from alvra_tools.load_data import *
from alvra_tools.channels import *
from alvra_tools.utils import errfunc_sigma, errfunc_fwhm

ploton = True

scan_name = "RuBpy3_monoscan_001"
scan_name = "Ru_foil_monoscan_003"

scan_name = "RuBpy3_monoscan_014"
# sf/alvra/data/p17983/raw/scan_data/Ru_foil_monoscan_001/
DIR = "/sf/alvra/data/p17983/raw/scan_data/" + scan_name + "/"
# DIR_json = "/das/work/p17/p17983/Example_data/res/scan_info/"
DIR_json = "/sf/alvra/data/p17983/res/scan_info/"

numstds = 3
minIzero = 0.025
lin_filter = 0.1

json_file = DIR_json + scan_name + "_scan_info.json"
print (json_file)

with open(json_file) as file:
    data = json.load(file)
numFiles = len(data['scan_files'])

print ("Processing",numFiles,"files")

DataFluo_pump_norm_total = np.empty(0)
DataFluo_unpump_norm_total = np.empty(0)
err_DataFluo_pump_total = np.empty(0)
err_DataFluo_unpump_total = np.empty(0)

IzeroFEL_pump_original_total = np.empty(0)
IzeroFEL_pump_total = np.empty(0)
IzeroFEL_unpump_original_total = np.empty(0)
IzeroFEL_unpump_total = np.empty(0)

DataFluo_pump_original_total = np.empty(0)
DataFluo_pump_total = np.empty(0)
DataFluo_unpump_original_total = np.empty(0)
DataFluo_unpump_total = np.empty(0)

noise_preFilter_pump = np.empty(0)
noise_noLinFilt_pump = np.empy(0)
noise_withLin_pump = np.empty(0)

Energy_eV = np.empty(0)
iZero = np.empty(0)

for i in range(0,numFiles):
#for i in range(0,1):
    filename = str(data['scan_files'][i][0])
    filename = DIR + os.path.basename(filename)
    exists = os.path.isfile(filename)
    if not exists:
        print("No such file")
    elif exists and i!=39: #Do we need this 39?
#         print("step",i+1,"of",numFiles,": Processing %s" %(str(data['scan_files'][i][0])))
        
        (DataFluo_pump, DataFluo_unpump, IzeroFEL_pump, IzeroFEL_unpump, Energy, _, _) = \
            load_PumpProbe_events(filename, channel_energy)

        IzeroFEL_pump_original = IzeroFEL_pump.copy()
        IzeroFEL_unpump_original = IzeroFEL_unpump.copy()
        
        IzeroFEL_pump_original_total = np.append(IzeroFEL_pump_original_total, IzeroFEL_pump_original)
        IzeroFEL_unpump_original_total = np.append(IzeroFEL_unpump_original_total, IzeroFEL_unpump_original)
        
        DataFluo_pump_original_total = np.append(DataFluo_pump_original_total, DataFluo_pump)
        DataFluo_unpump_original_total = np.append(DataFluo_unpump_original_total, DataFluo_unpump)
        
        IzeroMedian = np.median(np.concatenate([IzeroFEL_pump, IzeroFEL_unpump]))
        IzeroSTD = np.std(np.concatenate([IzeroFEL_pump, IzeroFEL_unpump]))
        

#         print(IzeroFEL_pump.T[0])
        
        
#         print(linFit_pump)
#         print(i)
        

        
    
        if i == 25:
            DataFluo_pump_temp = DataFluo_pump
            IzeroFEL_pump_temp = IzeroFEL_pump
        
        
        #apply filter to points which are not linear
        linFit_pump = np.polyfit(IzeroFEL_pump.T[0],DataFluo_pump.T[0],1)
        linFit_unpump = np.polyfit(IzeroFEL_unpump.T[0],DataFluo_unpump.T[0],1)
        
        conditionPumpLinHigh =  DataFluo_pump < IzeroFEL_pump*linFit_pump[0]+linFit_pump[1]+lin_filter
        conditionPumpLinLow =  DataFluo_pump > IzeroFEL_pump*linFit_pump[0]+linFit_pump[1]-lin_filter
        
        conditionUnPumpLinHigh =  DataFluo_unpump < IzeroFEL_unpump*linFit_unpump[0]+linFit_unpump[1]+lin_filter
        conditionUnPumpLinLow =  DataFluo_unpump > IzeroFEL_unpump*linFit_unpump[0]+linFit_unpump[1]-lin_filter
        
        IzeroMedian+numstds*IzeroSTD
        
        conditionPumpMax = IzeroFEL_pump < IzeroMedian+numstds*IzeroSTD
        conditionPumpMin = IzeroFEL_pump > IzeroMedian-numstds*IzeroSTD
        conditionPumpLow = IzeroFEL_pump > minIzero

        conditionUnPumpMax = IzeroFEL_unpump < IzeroMedian+numstds*IzeroSTD
        conditionUnPumpMin = IzeroFEL_unpump > IzeroMedian-numstds*IzeroSTD
        conditionUnPumpLow = IzeroFEL_unpump > minIzero

        condIzeroPump = conditionPumpMax & conditionPumpMin & conditionPumpLow & conditionPumpLinHigh & conditionPumpLinLow
        condIzeroUnPump = conditionUnPumpMax & conditionUnPumpMin & conditionUnPumpLow & conditionUnPumpLinHigh & conditionUnPumpLinLow
        
        IzeroFEL_pump = IzeroFEL_pump[condIzeroPump]
        IzeroFEL_unpump = IzeroFEL_unpump[condIzeroUnPump]
        
        IzeroFEL_pump_total = np.append(IzeroFEL_pump_total, IzeroFEL_pump)
        IzeroFEL_unpump_total = np.append(IzeroFEL_unpump_total, IzeroFEL_unpump)
        
        DataFluo_pump = DataFluo_pump[condIzeroPump]
        DataFluo_unpump = DataFluo_unpump[condIzeroUnPump]
        
        
        
        
        
        if i == 25:   # feel free to elmnate this if statement and following line
            
            plt.figure()
            plt.scatter(IzeroFEL_pump_temp, DataFluo_pump_temp)
            plt.scatter(IzeroFEL_pump, DataFluo_pump)
            plt.title('Izero, pumped')
            plt.xlabel('I0')
            plt.ylabel('Absorption')
            print(DataFluo_pump_total.shape)
        
        
        
#         DataFluo_pump = DataFluo_pump[condIzeroPump]
#         DataFluo_unpump = DataFluo_unpump[condIzeroUnPump]
        
        DataFluo_pump_total = np.append(DataFluo_pump_total, DataFluo_pump)
        DataFluo_unpump_total = np.append(DataFluo_unpump_total, DataFluo_unpump)
        
        DataFluo_pump_norm = DataFluo_pump/IzeroFEL_pump
        DataFluo_unpump_norm = DataFluo_unpump/IzeroFEL_unpump
        
        DataFluo_pump_norm_total = np.append(DataFluo_pump_norm_total, DataFluo_pump_norm.mean())
        DataFluo_unpump_norm_total = np.append(DataFluo_unpump_norm_total, DataFluo_unpump_norm.mean())
        err_DataFluo_pump_total = np.append(err_DataFluo_pump_total, DataFluo_pump_norm.std()/np.sqrt(DataFluo_pump_norm.size))
        err_DataFluo_unpump_total = np.append(err_DataFluo_unpump_total, DataFluo_unpump_norm.std()/np.sqrt(DataFluo_unpump_norm.size))
        
        Energy = [x for x in Energy if (np.abs(x) > 0)]
        Energy_eV = np.append(Energy_eV, np.mean(Energy))
        iZero = np.append(iZero, np.mean(IzeroFEL_pump_total))
        
        
print("The original number of pumped and unpumped shots is:")
print(IzeroFEL_pump_original_total.shape, IzeroFEL_unpump_original_total.shape)
print("The filtered number of pumped and unpumped shots is:")
print(IzeroFEL_pump_total.shape, IzeroFEL_unpump_total.shape)

plt.figure()
_, bins, _ = plt.hist(IzeroFEL_pump_original_total, 100, label = 'unfiltered')
_ = plt.hist(IzeroFEL_pump_total, bins, rwidth = .5, label = 'filtered')
plt.title('Izero, pumped')
plt.legend()

plt.figure()
_, bins, _ = plt.hist(IzeroFEL_unpump_original_total, 100, label = 'unfiltered')
_ = plt.hist(IzeroFEL_unpump_total, bins, rwidth = .5, label = 'filtered')
plt.title('Izero, unpumped')
plt.legend()



plt.figure()
plt.scatter(IzeroFEL_pump_original_total, DataFluo_pump_original_total)
plt.scatter(IzeroFEL_pump_total, DataFluo_pump_total)
plt.title('Izero, pumped')
plt.xlabel('I0')
plt.ylabel('Absorption')
print(DataFluo_pump_total.shape)

plt.figure()
plt.scatter(IzeroFEL_pump_original_total, DataFluo_pump_original_total)
plt.scatter(IzeroFEL_pump_total, DataFluo_pump_total)
plt.title('Izero, pumped')
plt.xlabel('I0')
plt.ylabel('Absorption')
print(DataFluo_pump_total.shape)

plt.figure()
plt.plot(np.array(Energy_eV), DataFluo_pump_norm_total,label='Pumped')
# plt.plot(np.array(Energy_eV), DataFluo_unpump_norm_total,label='UnPumped')
plt.plot(np.array(Energy_eV), np.array(iZero)*50,label="I_zero_Arb")
plt.xlabel('energy (eV)')
plt.ylabel('absorption')
plt.title('XAS_'+ scan_name)
plt.legend()

print(DataFluo_pump_norm_total.shape)



print(np.array(Energy_eV))

print(DataFluo_pump_norm_total)
DataFluo_pump_norm_total