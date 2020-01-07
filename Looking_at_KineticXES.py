import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import pickle

import scipy.io as sp

import RawDataClass as RDC
import ProcessedDataClass as PDC
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

scans = [20]
XESon = []
XESoff = []
tfy_on = []
tfy_off = []
delay_array = []
for i in range(0, len(scans)):
    basename = "RuDimerACN_timescan_0" + '%02d/' % scans[i]
    dirxas = "C:/Users/poult/Documents/Research/Beamtimes/SwissFEL_July_2019/Transfered_Data/Processed/RuDimerACN" \
             "/Kinetic_Traces/"
    dirxes = "C:/Users/poult/Documents/Research/Beamtimes/SwissFEL_July_2019/Transfered_Data/Processed/RuDimerACN" \
             "/Kinetic_Traces/Emission/ "
    with open(dirxas + basename + "xasrawdata.pkl", "rb") as f:
        xasrawdata = pickle.load(f)
    with open(dirxas + basename + "xasprodata.pkl", "rb") as f:
        xasprodata = pickle.load(f)
    with open(dirxes + basename + "XES_kinetic.pkl", "rb") as f:
        XES_kinetic = pickle.load(f)
    XESon.append(XES_kinetic.RIXS_map_pumped)
    XESoff.append(XES_kinetic.RIXS_map_unpumped)
    tfy_on.append(xasprodata.DataFluo_pump_norm_total)
    tfy_off.append(xasprodata.DataFluo_unpump_norm_total)
    delay_array.append(xasprodata.delays)

tfy_on = np.asarray(tfy_on)
tfy_off = np.asarray(tfy_off)
XESon = np.asarray(XESon)
XESoff = np.asarray(XESoff)

tfy_on_tot = np.zeros(len(xasprodata.delays))
tfy_off_tot = np.zeros(len(xasprodata.delays))
XESonTot = np.zeros((len(xasprodata.delays), 300))
XESoffTot = np.zeros((len(xasprodata.delays), 300))
for i in range(0, len(XESoff)):
    XESonTot = XESon[i] + XESonTot
    XESoffTot = XESoff[i] + XESoffTot
    tfy_on_tot = tfy_on[i] + tfy_on_tot
    tfy_off_tot = tfy_off[i] + tfy_off_tot


XESonAVG = XESonTot / len(XESon)
XESoffAVG = XESoffTot / len(XESoff)
tfy_on_avg = tfy_on_tot / len(tfy_on)
tfy_off_avg = tfy_off_tot / len(tfy_off)

XES_trace_off = []
XES_trace_on = []
for i in range(0,XESoffAVG.shape[0]):
    XES_trace_off.append(np.trapz(XESoffAVG[i,155:175]))
    XES_trace_on.append(np.trapz(XESonAVG[i,155:175]))
XES_trace_off = np.asarray(XES_trace_off)
XES_trace_on = np.asarray(XES_trace_on)

normconstants_off = []
normconstants_on = []
normconstants_on.append(np.divide(XES_trace_on,tfy_on_avg))
normconstants_off.append(np.divide(XES_trace_off,tfy_off_avg))
normconstants_on = np.asarray(normconstants_on).flatten()
normconstants_off = np.asarray(normconstants_off).flatten()

XESonAVG_new=[]
XESoffAVG_new=[]

for i in range(0,XESoffAVG.shape[0]):
    XESonAVG_new.append(np.multiply(XESonAVG[i,:],normconstants_on[i]))
    XESoffAVG_new.append(np.multiply(XESoffAVG[i,:],normconstants_off[i]))

XESonAVG_new = np.asarray(XESonAVG_new)
XESoffAVG_new = np.asarray(XESoffAVG_new)



# plt.figure()
# plt.plot(normconstants_on,label='on')
# plt.plot(normconstants_off,label = 'off')
# plt.show()

# X, Y = np.meshgrid(np.linspace(0, XESonAVG.shape[1], XESonAVG.shape[1] + 1), xasprodata.delays)
# plt.subplot(2, 1, 1)
# plt.pcolor(X, Y, XESonAVG, vmax=0.5)
# plt.colorbar()
# plt.xlabel('JF pixel')
# plt.ylabel('Time (ps)')
# plt.title('DimerACN XES pumped')
# plt.tight_layout()
#
#
# X, Y = np.meshgrid(np.linspace(0, XESoffAVG.shape[1], XESoffAVG.shape[1] + 1), xasprodata.delays)
# plt.figure()
# plt.subplot(2, 1, 1)
# plt.pcolor(X, Y, XESoffAVG, vmax=0.5)
# plt.colorbar()
# plt.xlabel('JF pixel')
# plt.ylabel('Time (ps)')
# plt.title('DimerACN XES unpumped')
# plt.tight_layout()
#
#
# X, Y = np.meshgrid(np.linspace(0, XESoffAVG.shape[1], XESoffAVG.shape[1] + 1), xasprodata.delays)
# plt.figure()
# plt.subplot(2, 1, 1)
# plt.pcolor(X, Y, (XESonAVG-XESoffAVG), vmax=0.1)
# plt.colorbar()
# plt.xlabel('JF pixel')
# plt.ylabel('Time (ps)')
# plt.title('DimerACN XES unpumped')
# plt.tight_layout()



#plt.figure()
#plt.plot(xasprodata.delays,tfy_on_avg)
#plt.plot(xasprodata.delays,tfy_off_avg)
#plt.plot(xasprodata.delays,(tfy_on_avg-tfy_off_avg)+6)
#plt.xlabel('JF pixel')
#plt.ylabel('Time (ps)')
#plt.legend(('pumped','unpumped','normalized difference'))
#plt.title('DimerACN TFY Kinetic Trace, 2840.3 eV Incident Energy')
#plt.show()
#
#
#plt.figure()
#on = []
#off = []
#diff = []
#for i in range(0,len(xasprodata.delays)):
#    # plt.plot(XESonAVG[i,125:200]-XESoffAVG[i,125:200])
#    on.append(np.trapz(XESonAVG[i, 155:175]))
#    off.append(np.trapz(XESoffAVG[i, 155:175]))
#    diff.append(np.trapz(XESonAVG[i,155:175])-np.sum(XESoffAVG[i,125:200]))
#diff=np.asarray(diff)
#plt.figure()
#plt.plot(xasprodata.delays,on)
#plt.plot(xasprodata.delays,off)
#plt.plot(xasprodata.delays,diff+3.2)
#plt.legend(('pumped','unpumped','normalized difference'))
#plt.xlabel('JF pixel')
#plt.ylabel('Time (ps)')
#plt.title('DimerACN XES Kinetic Trace, 2840.3 eV Incident Energy')
#plt.show()
plt.figure()
plt.plot(xasprodata.delays,tfy_on_avg)
plt.plot(xasprodata.delays,tfy_off_avg)
plt.plot(xasprodata.delays,(tfy_on_avg-tfy_off_avg)+6)
plt.xlabel('JF pixel')
plt.ylabel('Time (ps)')
plt.legend(('pumped','unpumped','normalized difference'))
plt.title('DimerACN TFY Kinetic Trace, 2840.3 eV Incident Energy')
plt.show()
#
#
# # plt.figure()
# on = []
# off = []
# diff = []
# for i in range(0,len(xasprodata.delays)):
#     # plt.plot(XESonAVG[i,125:200]-XESoffAVG[i,125:200])
#     on.append(np.trapz(XESonAVG[i, 155:175]))
#     off.append(np.trapz(XESoffAVG[i, 155:175]))
#     diff.append(np.trapz(XESonAVG[i,155:175])-np.sum(XESoffAVG[i,125:200]))
# diff=np.asarray(diff)
# plt.figure()
# # plt.plot(xasprodata.delays,on)
# # plt.plot(xasprodata.delays,off)
# plt.plot(xasprodata.delays,(diff/off)+3.2)
# plt.legend(('pumped','unpumped','normalized difference'))
# plt.xlabel('JF pixel')
# plt.ylabel('Time (ps)')
# plt.title('DimerACN XES Kinetic Trace, 2840.3 eV Incident Energy')
# plt.show()

# X, Y = np.meshgrid(np.linspace(0, XESoffAVG.shape[1], XESoffAVG.shape[1] ), xasprodata.delays)
# fig = plt.figure()
# ax = Axes3D(fig)
# surf = ax.plot_surface(X, Y, XESonAVG,cmap=cm.jet, linewidth=0.1, vmin=-0.03, vmax=0.06)
# fig.colorbar(surf, shrink=0.5, aspect=5)
# plt.xlabel('JF pixel')
# plt.ylabel('Time (ps)')
# plt.title('DimerACN XES pumped')
# #
# X, Y = np.meshgrid(np.linspace(0, XESoffAVG.shape[1], XESoffAVG.shape[1] ), xasprodata.delays)
# fig = plt.figure()
# ax = Axes3D(fig)
# surf = ax.plot_surface(X, Y, XESoffAVG,cmap=cm.jet, linewidth=0.1, vmin=-0.03, vmax=0.06)
# fig.colorbar(surf, shrink=0.5, aspect=5)
# plt.xlabel('JF pixel')
# plt.ylabel('Time (ps)')
# plt.title('DimerACN XES unpumped')
# #
# X, Y = np.meshgrid(np.linspace(0, XESoffAVG.shape[1], XESoffAVG.shape[1]), xasprodata.delays)
# fig = plt.figure()
# ax = Axes3D(fig)
# surf = ax.plot_surface(X, Y, np.divide(np.subtract(XESonAVG,XESoffAVG),XESoffAVG),cmap=cm.jet, linewidth=0.1, vmin=-0.03, vmax=2)
# fig.colorbar(surf, shrink=0.5, aspect=5)
# plt.xlabel('JF pixel')
# plt.ylabel('Time (ps)')
# plt.title('off')
# X, Y = np.meshgrid(np.linspace(0, XESoffAVG[:,110:180].shape[1], XESoffAVG[:,110:180].shape[1]), xasprodata.delays)
# fig = plt.figure()
# ax = Axes3D(fig)
# surf = ax.plot_surface(X, Y, np.divide(np.subtract(XESonAVG_new[:,110:180],XESoffAVG_new[:,110:180]),XESoffAVG_new[:,110:180]),cmap=cm.jet, linewidth=0.1, vmin=-0.03, vmax=2)
# fig.colorbar(surf, shrink=0.5, aspect=5)
# plt.xlabel('JF pixel')
# plt.ylabel('Time (ps)')
# plt.title('on')
