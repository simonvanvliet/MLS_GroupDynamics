#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 2019

Last Update Oct 22 2019

Run single model and plot result

@author: Simon van Vliet & Gil Henriques
Department of Zoology
University of Britisch Columbia
vanvliet@zoology.ubc.ca
henriques@zoology.ubc.ca

============================================================================
Run Model and plot results
============================================================================"""

import sys
sys.path.insert(0, '..')

from mainCode import MlsGroupDynamics_main as mls
import plotSingleRun as pltRun
import time

#set model parameters
K_tot_def = 20000
model_par = {
        #time and run settings
        "maxRunTime":       900,     #max cpu time in seconds
        "maxT":             100,  # total run time
        "maxPopSize":       40000,  #stop simulation if population exceeds this number
        "minT":             200,    # min run time
        "sampleInt":        1,      # sampling interval
        "mav_window":       100,    # average over this time window
        "rms_window":       100,    # calc rms change over this time window
        "rms_err_trNCoop":  1E-2,   # when to stop calculations
        "rms_err_trNGr":    5E-2,   # when to stop calculations
        # settings for initial condition
        "init_groupNum":    100,     # initial # groups
        "init_fCoop":       1,
        "init_groupDens":   50,     # initial total cell number in group
        # settings for individual level dynamics
        # complexity
        "indv_NType":       1,
        "indv_asymmetry":   1,      # difference in growth rate b(j+1) = b(j) / asymmetry
        # mutation load
        "indv_cost":        0.01,   # cost of cooperation
        "indv_mutR":        1E-3,   # mutation rate to cheaters
        "indv_migrR":       0,      # mutation rate to cheaters
        # group size control
        "indv_K":           100,     # total group size at EQ if f_coop=1
        "delta_indv":       1,      # zero if death rate is simply 1/k, one if death rate decreases with group size
        # setting for group rates
        # fission rate
        'gr_CFis':          0.1,
        'gr_SFis':          0,     # measured in units of 1 / indv_K
        'grp_tau':          1,     # constant multiplies group rates
        # extinction rate
        'delta_grp':        0,      # exponent of density dependence on group #
        'K_grp':            0,      # carrying capacity of groups
        'delta_tot':        1,      # exponent of density dependence on total #individual
        'K_tot':            3E4,    # carrying capacity of total individuals
        'delta_size':       0,      # exponent of size dependence
        # settings for fissioning
        'offspr_size':      0.01,  # offspr_size <= 0.5 and
        'offspr_frac':      0.01,    # offspr_size < offspr_frac < 1-offspr_size'
         # extra settings
        'run_idx':          1,
        'perimeter_loc':    0
    }
  



#run model

# run code
start = time.time()
output = mls.run_model_dynamics_fig(model_par)
pltRun.plot_single_run(model_par, output)


end = time.time()

# print timing
print("Elapsed time run 1 = %s" % (end - start))



