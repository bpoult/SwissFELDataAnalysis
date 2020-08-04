#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 03:12:17 2020

@author: ext-liekhussc_c
"""

import h5py
import numpy as np


def _make_reprates_on(pulse_ids, reprate):
    return pulse_ids % (100 / reprate) == 0

def _make_reprates_off(pulse_ids, reprate):
    return np.logical_not(_make_reprates_on(pulse_ids, reprate))

def _make_reprates_FEL_on_laser_off(pulse_ids, reprate_FEL, reprate_laser):
    return np.logical_and(_make_reprates_on(pulse_ids, reprate_FEL), _make_reprates_off(pulse_ids, reprate_laser))

def _make_reprates_on_off(pulse_ids, reprate_FEL, reprate_laser):
    reprate_on  = _make_reprates_on(pulse_ids, reprate_laser)
    reprate_off = _make_reprates_FEL_on_laser_off(pulse_ids, reprate_FEL, reprate_laser)
    return reprate_on, reprate_off

def load_JF_cropped_data_pump(fname, roi, reprate_FEL, reprate_laser, nshots=None):
    with h5py.File(fname, "r") as f:
        
        pulse_ids = f[f"pulse_ids"][:nshots]
        images    = f[f"images_roi{roi}"][:nshots]
        
    reprate_on, reprate_off = _make_reprates_on_off(pulse_ids, reprate_FEL, reprate_laser)
    
    images_on  = images[reprate_on]
    images_off = images[reprate_off]
    pulse_ids_on = pulse_ids[reprate_on]
    pulse_ids_off = pulse_ids[reprate_off]

    return images_on, images_off, pulse_ids_on, pulse_ids_off