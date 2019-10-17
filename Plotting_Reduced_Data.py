import numpy as np
import os
import sys
import matplotlib.pyplot as plt

DIR = 'C:/Users/poult/Documents/Research/Beamtimes/SwissFEL_July_2019/Transfered_Data/Reduced_Data/Reduced_data/'
DIRther = '/XAS_Cl/600fs/scans_1_4_5_6/'
filename = 'XES_2836.5eV_10psXES_2836.5eV_10psXES_off.npy'
filename2 = 'avgFluo_unpump.npy'
filename3 = 'Energy_eV.npy'

pumped = np.load(DIR + filename)
unpumped = np.load(DIR + DIRther + filename2)
Energy = np.load(DIR + DIRther + filename3)
print(len(Energy))
print(pumped.shape)
plt.plot(Energy, pumped, label='unpumped')
plt.xlabel('Energy, eV')
plt.ylabel('Intensity, a.u.')
plt.legend()
plt.show()






# transient600fs = [x - y for x, y in zip(pumped, unpumped)]
# print(len(transient600fs))
# DIRther = '/XAS_Cl/10ps_/scans_1/'
# filename = 'avgFluo_pump.npy'
# filename2 = 'avgFluo_unpump.npy'
# filename3 = 'Energy_eV.npy'
#
# pumped = np.load(DIR + DIRther + filename)
# unpumped = np.load(DIR + DIRther + filename2)
# Energy2 = np.load(DIR + DIRther + filename3)
#
# plt.plot(Energy2, pumped, label='pumped')
# plt.plot(Energy2, unpumped, label='unpumped')
# plt.xlabel('Energy, eV')
# plt.ylabel('Intensity, a.u.')
# plt.legend()
# plt.show()
#
# transient10ps = [x - y for x, y in zip(pumped, unpumped)]
#
#
# plt.plot(Energy, transient600fs,label='DimerACN')
# plt.plot(Energy2,transient10ps,label='DimerCl')
# plt.xlabel('Energy, eV')
# plt.ylabel('Intensity, a.u.')
# plt.legend()
# plt.show()
