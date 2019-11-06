import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import pickle
import RawDataClass as RDC
import ProcessedDataClass as PDC


def plotRIXS(scans,base,dirxas,dirrixs,ploton):
    RIXSon = []
    RIXSoff = []
    for i in range(0, len(scans)):
        basename = base + '%02d/' % scans[i]
        with open(dirxas + basename + "xasrawdata.pkl", "rb") as f:
            xasrawdata = pickle.load(f)
        with open(dirrixs + basename + "rixsprodata.pkl", "rb") as f:
            rixsprodata = pickle.load(f)
        RIXSon.append(rixsprodata.RIXS_map_pumped)
        RIXSoff.append(rixsprodata.RIXS_map_unpumped)

    RIXSon = np.asarray(RIXSon)
    RIXSoff = np.asarray(RIXSoff)

    RIXSonTot = np.zeros((55, 300))
    RIXSoffTot = np.zeros((55, 300))
    for i in range(0, len(RIXSoff)):
        RIXSonTot = RIXSon[i] + RIXSonTot
        RIXSoffTot = RIXSoff[i] + RIXSoffTot

    RIXSonAVG = RIXSonTot / len(RIXSon)
    RIXSoffAVG = RIXSoffTot / len(RIXSoff)

    if ploton is True:
        X, Y = np.meshgrid(np.linspace(0, RIXSonAVG.shape[1], RIXSonAVG.shape[1] + 1), xasrawdata.Energy)
        plt.subplot(2, 1, 1)
        plt.pcolor(X, Y, RIXSonAVG, vmax=0.1)
        plt.colorbar()
        plt.xlabel('JF pixel')
        plt.ylabel('Mono Energy (eV)')
        plt.title('DimerACN RIXS pumped 10ps')
        plt.tight_layout()

        X, Y = np.meshgrid(np.linspace(0, RIXSoffAVG.shape[1], RIXSoffAVG.shape[1] + 1), xasrawdata.Energy)
        plt.figure()
        plt.subplot(2, 1, 1)
        plt.pcolor(X, Y, RIXSoffAVG, vmax=0.1)
        plt.colorbar()
        plt.xlabel('JF pixel')
        plt.ylabel('Mono Energy (eV)')
        plt.title('DimerACN RIXS unpumped 10ps')
        plt.tight_layout()

        X, Y = np.meshgrid(np.linspace(0, RIXSoffAVG.shape[1], RIXSoffAVG.shape[1] + 1), xasrawdata.Energy)
        plt.figure()
        plt.subplot(2, 1, 1)
        plt.pcolor(X, Y, RIXSonAVG-RIXSoffAVG, vmax=0.05)
        plt.colorbar()
        plt.xlabel('JF pixel')
        plt.ylabel('Mono Energy (eV)')
        plt.title('DimerACN RIXS pumped-unpumped 10ps')
        plt.tight_layout()

    return RIXSonAVG,RIXSoffAVG,xasrawdata
