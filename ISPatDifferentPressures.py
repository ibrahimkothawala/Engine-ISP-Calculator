# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 2020

@author: Ibrahim Kothawala
"""
"""
Calculate the specfic impulse using ISPCalculator at different inlet pressures
"""
#%% Imports 
import numpy as np
import ISPcalculator
import cantera as ct
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#%% Inputs
gas = ct.Solution('gri30_highT.cti')
fuelSpecies = ['CH3OH'] #molecules that the fuel is made up of
fuel = 'CH3OH' #fuel mixture
oxSpecies = ['O2','N2'] #molecules that make up the oxidizer mixture
oxidizer = 'O2:1.0,N2:3.76' #oxidizer mixture
pExit = ct.one_atm #exit pressuer [pa]
pres_pts = 100
pressureRange = np.linspace(3*ct.one_atm,100*ct.one_atm,pres_pts) #range of pressures to calculate ISP over
maxISParray = np.zeros(pres_pts)

#%% Main Function Loop
for ii in range(pres_pts):
    args = pressureRange[ii],pExit,fuel,oxidizer
    soln = ISPcalculator.maximum_isp(gas,args)
    maxISParray[ii] = soln[-1]
    if ii == 0:
        phiRange = soln[0]
        fullISP_array = np.zeros((pres_pts,len(phiRange)))
        fullISP_array[ii,:] = soln[1]
    else:
        fullISP_array[ii,:] = soln[1] 

#%% Plotting 2D
xlabel = 'Pressure [mPa]'
plt.plot(pressureRange/1e6, maxISParray,'-')
plt.title('Maximum ISP versus Pressure')
plt.xlabel(xlabel,fontsize='large')
plt.ylabel('ISP [s]',fontsize='large')
plt.savefig('max ISP at different inlet Pressures.png')
plt.show()

#%% Plotting 3D
fig = plt.figure()
ax = fig.add_subplot(111,projection = '3d')
ax.plot_surface(pressureRange,phiRange,fullISP_array)
ax.view_init(60,0)
ax.set_xlabel('Pressure')
ax.set_ylabel('Equivalence Ratio')
plt.show
plt.savefig('ISPsurface.png',dpi=1000)

# %%
