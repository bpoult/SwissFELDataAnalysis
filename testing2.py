import numpy as np
import scipy.io as sp
from EmissionToLoss import emiss2loss
from scipy.io import loadmat
import matplotlib.pyplot as plt

directory = 'C:/Users/poult/Documents/Research/Beamtimes/SSRL June 2019/RIXSLalphaL3/'
Ru_Dimer_Solid = loadmat(directory + 'RuDimerACN.mat')
f = open(directory + 'Eaxis.txt','r')
y = f.readlines()
y = list(map(str.strip,y))
for i in range(0,len(y)):
    y[i] = float(y[i])
y = np.asarray(y)

RIXS = Ru_Dimer_Solid['RIXS']
x = Ru_Dimer_Solid['x'].flatten()


LossMap, loss,mono = emiss2loss(RIXS,y,x)

plt.figure()
X, Y = np.meshgrid(mono, loss)
plt.subplot(2, 1, 1)
plt.pcolor(X, Y, LossMap, vmax=0.1)
plt.colorbar()
plt.xlabel('Mono Energy (eV)')
plt.ylabel('Energy Loss (eV)')
plt.title('DimerACN RIXS pumped 600fs')
plt.tight_layout()

SaveThis = True
if SaveThis is True:

    sp.savemat('C:/Users/poult/Documents/Research/Beamtimes/SSRL June 2019/E-Transfer Axis/RuDimerACN_powder.mat',
               mdict= {'map':LossMap,'energyT':loss,'mono':mono})