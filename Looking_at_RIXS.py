import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import pickle
import RawDataClass as RDC
import ProcessedDataClass as PDC


def plotRIXS(scans, base, dirxas, dirrixs, ploton):
    RIXSon = []
    RIXSoff = []
    herfd_pumped = []
    herfd_unpumped = []
    herfd_Difference = []
    for i in range(0, len(scans)):
        basename = base + '%02d/' % scans[i]
        with open(dirxas + basename + "xasrawdata.pkl", "rb") as f:
            xasrawdata = pickle.load(f)
        with open(dirrixs + basename + "rixsprodata.pkl", "rb") as f:
            rixsprodata = pickle.load(f)
        RIXSon.append(rixsprodata.RIXS_map_pumped)
        RIXSoff.append(rixsprodata.RIXS_map_unpumped)
        herfd_pumped.append(rixsprodata.RIXS_map_pumped[:,167])
        herfd_unpumped.append(rixsprodata.RIXS_map_unpumped[:,167])
        herfd_Difference.append(np.subtract(rixsprodata.RIXS_map_pumped[:,167], rixsprodata.RIXS_map_unpumped[:,167]))


    RIXSon = np.asarray(RIXSon)
    RIXSoff = np.asarray(RIXSoff)
    herfd_pumped = np.asarray(herfd_pumped)
    herfd_unpumped = np.asarray(herfd_unpumped)
    herfd_Difference = np.asarray(herfd_Difference)
    RIXSon[RIXSon == 0] = np.nan
    RIXSoff[RIXSoff == 0] = np.nan
    herfd_pumped[herfd_pumped == 0] = np.nan
    herfd_unpumped[herfd_unpumped == 0] = np.nan
    herfd_Difference[herfd_Difference == 0] = np.nan

    # RIXSonTot = np.zeros((55, 300))
    # RIXSoffTot = np.zeros((55, 300))
    # for i in range(0, len(RIXSoff)):
    #     RIXSonTot = RIXSon[i] + RIXSonTot
    #     RIXSoffTot = RIXSoff[i] + RIXSoffTot

    RIXSonAVG = np.nanmean(RIXSon, axis=0)
    RIXSoffAVG = np.nanmean(RIXSoff, axis=0)
    herfd_pumped = np.nanmean(herfd_pumped,axis = 0)
    herfd_unpumped = np.nanmean(herfd_unpumped,axis = 0)
    herfd_Difference = np.nanmean(herfd_Difference, axis=0)
    RIXSonAVG = np.nan_to_num(RIXSonAVG)
    RIXSoffAVG = np.nan_to_num(RIXSoffAVG)
    herfd_pumped = np.nan_to_num(herfd_pumped)
    herfd_unpumped = np.nan_to_num(herfd_unpumped)
    herfd_Difference = np.nan_to_num(herfd_Difference)

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
        plt.pcolor(X, Y, RIXSonAVG - RIXSoffAVG, vmax=0.05)
        plt.colorbar()
        plt.xlabel('JF pixel')
        plt.ylabel('Mono Energy (eV)')
        plt.title('DimerACN RIXS pumped-unpumped 10ps')
        plt.tight_layout()

    return RIXSonAVG, RIXSoffAVG, xasrawdata, herfd_pumped, herfd_unpumped,herfd_Difference
