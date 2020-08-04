import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import pickle
import RawDataClass as RDC
import ProcessedDataClass as PDC


def plotRIXS(scans, base, dirxas, dirrixs, ploton):
    RIXSonTot = []
    RIXSoffTot = []
    herfd_pumped = []
    herfd_unpumped = []
    herfd_diff = []
    herfd_on = []
    herfd_off = []
    herfd_Difference = []
    ReferenceEnergy = [2852.0, 2851.0, 2850.0, 2849.0, 2848.0, 2847.0, 2846.5, 2846.0, 2845.5, 2845.0, 2844.75, 2844.5,
                       2844.25, 2844.0,
                       2843.75, 2843.5, 2843.25, 2843.0, 2842.75, 2842.5, 2842.25, 2842.0, 2841.75, 2841.5, 2841.25,
                       2841.0, 2840.75, 2840.5,
                       2840.25, 2840.0, 2839.75, 2839.5, 2839.25, 2839.0, 2838.75, 2838.5, 2838.25, 2838.0, 2837.75,
                       2837.5, 2837.25, 2837.0,
                       2836.75, 2836.5, 2836.25, 2836.0, 2835.75, 2835.5, 2835.25, 2835.0, 2834.5, 2834.0, 2833.0,
                       2832.0, 2831.0]
    Energy = ReferenceEnergy
    plt.figure()
    for i in range(0, len(scans)):
        basename = base + '%02d/' % scans[i]
        with open(dirxas + basename + "xasrawdata.pkl", "rb") as f:
            xasrawdata = pickle.load(f)
        with open(dirrixs + basename + "rixsprodata.pkl", "rb") as f:
            rixsprodata = pickle.load(f)
        herfd_on=rixsprodata.RIXS_map_pumped[:,167]
        herfd_off=rixsprodata.RIXS_map_unpumped[:,167]
        herfd_diff=np.subtract(rixsprodata.RIXS_map_pumped[:,167], rixsprodata.RIXS_map_unpumped[:,167])
        index = []
        for elements in range(0, len(xasrawdata.Energy)):
            Element = min(ReferenceEnergy, key=lambda var: abs(var - xasrawdata.Energy[elements]))
            index.append(ReferenceEnergy.index(Element))

        w, h = 300,55
        RIXSonTot.append([[0 for x in range(w)] for y in range(h)])
        RIXSoffTot.append([[0 for x in range(w)] for y in range(h)])
        herfd_pumped.append([0]*55)
        herfd_unpumped.append([0]*55)
        for variable in range(0, len(index)):
            addVals = index[variable]
            RIXSonTot[i][addVals] = rixsprodata.RIXS_map_pumped[variable]
            RIXSoffTot[i][addVals] = rixsprodata.RIXS_map_unpumped[variable]
            herfd_pumped[i][addVals]=herfd_on[variable]
            herfd_unpumped[i][addVals]=herfd_off[variable]
        plt.plot(herfd_unpumped[i])
    RIXSon = np.asarray(RIXSonTot)
    RIXSoff = np.asarray(RIXSoffTot)
    herfd_pumped = np.asarray(herfd_pumped)
    herfd_unpumped = np.asarray(herfd_unpumped)
    RIXSon[RIXSon == 0] = np.nan
    RIXSoff[RIXSoff == 0] = np.nan
    herfd_pumped[herfd_pumped == 0] = np.nan
    herfd_unpumped[herfd_unpumped == 0] = np.nan


    RIXSonAVG = np.nanmean(RIXSon, axis=0)
    RIXSoffAVG = np.nanmean(RIXSoff, axis=0)
    herfd_pumped = np.nanmean(herfd_pumped,axis = 0)
    herfd_unpumped = np.nanmean(herfd_unpumped,axis = 0)
    RIXSonAVG = np.nan_to_num(RIXSonAVG)
    RIXSoffAVG = np.nan_to_num(RIXSoffAVG)
    herfd_pumped = np.nan_to_num(herfd_pumped)
    herfd_unpumped = np.nan_to_num(herfd_unpumped)

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
