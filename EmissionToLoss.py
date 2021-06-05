import numpy as np


def emiss2loss(rixsmap, emiss, mono):
    '''
    Convert mono vs emiss RIXS map into mono vs energy loss RIXS map
    '''
    loss_step = np.round((np.amax(emiss) - np.amin(emiss)) / len(emiss), 1)
    loss_min = np.round(np.amin(mono) - np.amax(emiss), 1)
    loss_max = np.round(np.amax(mono) - np.amin(emiss), 1)

    loss = np.arange(loss_min, loss_max, loss_step)
    loss = np.sort(loss)
    rixsmap2 = np.zeros((len(loss), len(mono)))
    for i in np.arange(len(mono)):
        loss0 = mono[i] - emiss
        rixs0 = rixsmap[:, i]
        rixsmap2[:, i] = np.interp(loss, loss0, rixs0, left=0, right=0)
    return rixsmap2, loss, mono
