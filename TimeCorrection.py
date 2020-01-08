import numpy as np



def TimeCorrection(xasrawdata, Tzero_mm):
    delay_mm = np.empty(0)
    delay_ps = []
    Tcorrected_pump = []
    column = []
    for i in range(0, len(xasrawdata.delay_SH_pump)):
        delay_ps.append(1e12 * (xasrawdata.delay_SH_pump[i] - Tzero_mm) * 2 * 1e-3 / 3e8)
        for j in range(len(xasrawdata.delay_SH_pump[i])):
            column.append(delay_ps[i][j] + xasrawdata.PALM_pump[i][j] * 1e-3)
        Tcorrected_pump.append(column)
        column = []
        Tcorrected_pump[i]=np.asarray(Tcorrected_pump[i])
    xasrawdata.changeValue(delay_ps=delay_ps,
                           Tcorrected_pump=Tcorrected_pump)

    return xasrawdata
