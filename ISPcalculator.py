# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 14:08:54 2020

@author: Ibrahim Kothawala
"""
"""
Calculate the specfic impulse according to these equations:
https://web.mit.edu/16.unified/www/SPRING/propulsion/notes/node102.html

"""

#%% Imports, Constants, and Base Function Definitions
import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp
import os
import time
from functools import partial
#constants
g = 9.81 #m/s

#calculates the ISP assuming constant entropy and cp
def isp(chamberTemp,cp,gamma,p_exit,p_chamber):
    return np.sqrt(2*cp*chamberTemp*(1-(p_exit/p_chamber)**(1-1/gamma)))/g

#calculates the ISP assuming constant entropy
def isp_isentropic(inlet_gas,p_exit):
    inlet_gas.equilibrate('HP')
    h_inlet = inlet_gas.h
    s = inlet_gas.s
    inlet_gas.SP = s,p_exit
    h_outlet = inlet_gas.h
    return np.sqrt(2*(h_inlet-h_outlet))/g

#calculates ISP the same as function above but is used in mutliprocessing because 
#the Solution object in Cantera is not picklable
#https://github.com/Cantera/enhancements/issues/10
def isp_isentropic_multi_process(gas,pChamber,p_exit,inletT,ox,fuel,phi):
    gas.TP = inletT,pChamber
    gas.set_equivalence_ratio(phi,fuel,ox)
    gas.equilibrate('HP')
    h_inlet = gas.h
    s = gas.s
    gas.SP = s,p_exit
    h_outlet = gas.h
    return np.sqrt(2*(h_inlet-h_outlet))/g

#Calculates the oxidizer to fuel mass ratio
def stoichRatio(gas,fuel,oxidizer,fuelSpecies,oxidizerSpecies):
    fuelMass = 0
    oxMass = 0
    gas.set_equivalence_ratio(1,fuel,oxidizer)
    for oxSpecie in oxidizerSpecies:
        oxMass+= gas.Y[gas.species_index(oxSpecie)]
    for fuelSpecie in fuelSpecies:
        fuelMass+= gas.Y[gas.species_index(fuelSpecie)]
    return oxMass/fuelMass

#%% Main Function 
#returns the range of phi values calculated upon, the isp calcuted, the phi that 
#the maximum isp occurs on, and the maximum isp plots the isp against phi and other parameters
def maximum_isp(inlet_gas,args,phi_range= np.linspace(0.0001,10,100),plots_val=False):
    p_chamber,p_exit,fuel,oxidizer = args
    phi_pts = len(phi_range)
    temp_range = np.zeros(phi_pts)
    cp_range = np.zeros(phi_pts)
    gamma_range = np.zeros(phi_pts)
    isp_range = np.zeros(phi_pts)
    isp_isen = np.zeros(phi_pts)
    
    for ii in range(phi_pts):
        #calculating the ISP assuming cp and entropy are constant
        inlet_gas.TP= 300,p_chamber
        inlet_gas.set_equivalence_ratio(phi_range[ii],fuel,oxidizer)
        inlet_gas.equilibrate('HP')
        temp_range[ii] = inlet_gas.T
        cp_range[ii] = inlet_gas.cp
        gamma_range[ii] = inlet_gas.cp/inlet_gas.cv
        isp_range[ii] = isp(temp_range[ii],cp_range[ii],gamma_range[ii],p_exit,p_chamber)
        #calculating the ISP by assuming isentropic
        inlet_gas.TP= 300,p_chamber
        inlet_gas.set_equivalence_ratio(phi_range[ii],fuel,oxidizer)
        isp_isen[ii] = isp_isentropic(inlet_gas,p_exit)
    #Plots
    if plots_val:
        xlabel = 'Equivalence Ratio'
        fig, axs = plt.subplots(4, 1, constrained_layout=True)
        axs[0].plot(phi_range, temp_range,'-')
        axs[0].set_title('Adiabatic Flame Temp')
        axs[0].set_xlabel(xlabel)
        axs[0].set_ylabel('Temperature [K]')
        fig.suptitle('Calculation of ISP: effect of thermodynamic properties', fontsize=12)

        axs[1].plot(phi_range,cp_range, '-')
        axs[1].set_xlabel(xlabel)
        axs[1].set_title('Specific Heat Cp')
        axs[1].set_ylabel('Cp [j/kg/K]')

        axs[2].plot(phi_range,gamma_range, '-')
        axs[2].set_xlabel(xlabel)
        axs[2].set_title('Gamma')
        axs[2].set_ylabel('Gamma')

        axs[3].plot(phi_range,isp_range, '-', label='Constant Cp')
        axs[3].plot(phi_range,isp_isen, '--', label='Nonconstant Cp')
        axs[3].set_xlabel(xlabel)
        axs[3].set_title('Specific Impulse')
        axs[3].set_ylabel('ISP [s]')
        axs[3].legend(loc='lower right')
        plt.show()
    return phi_range,isp_isen,phi_range[np.argmax(isp_isen)],max(isp_isen)

#multi processing funtion to speed up analysis when looking at various chamber pressures.
def maximum_isp_multi_processing(gas,phi_range,p_exit,inletT,ox,fuel,pChamber):
    f = partial(isp_isentropic_multi_process, gas, pChamber,p_exit, inletT,ox,fuel)
    isp_range = [f(phi) for phi in phi_range]
    return isp_range,phi_range,max(isp_range),phi_range[np.argmax(isp_range)]

def max_isp_different_pressures(cti_file_or_gas,phi_range,p_exit,inletT,ox,fuel,pChamberRange):
    if isinstance(cti_file_or_gas,str):
        gas = ct.Solution(cti_file_or_gas)
    else:
        gas = cti_file_or_gas
    f = partial(maximum_isp_multi_processing,gas,phi_range,p_exit,inletT,ox,fuel)
    soln = [f(pChamber) for pChamber in pChamberRange]
    return soln

#only use this function if you are dealing with very large datasets >500 as it only adds marginal time improvement above the 
#previous function
def max_isp_different_pressures_multi_processing(cti_file,phi_range,p_exit,inletT,ox,fuel,pChamberRange):
    numProcess = os.cpu_count()
    pool = mp.Pool(numProcess)
    chunks = [pChamberRange[i::numProcess] for i in range(numProcess)]
    f = partial(max_isp_different_pressures,cti_file,phi_range,p_exit,inletT,ox,fuel)
    soln = pool.map(f,chunks)
    return soln

#%% Testing Functions Above
if __name__ == '__main__':
    cti_file = 'gri30_highT.cti'
    inlet_gas = ct.Solution(cti_file)
    inlet_gas.basis = 'mass'
    p_exit = ct.one_atm #pascals
    p_chamber = 2068427.1 #pascals
    inletT = 300
    fuelSpecies = ['CH3OH'] #molecules that the fuel is made up of
    fuel = 'CH3OH' #fuel mixture
    oxSpecies = ['O2','N2'] #molecules that make up the oxidizer mixture
    oxidizer = 'O2:1.0,N2:3.76' #oxidizer mixture
    phi_range = np.linspace(0.0001,10,100) #range of equivalence ratio for the calculation
    p_chamberRange = np.linspace(3*p_exit,100*p_exit,500)
    start_time = time.clock()
    soln = max_isp_different_pressures(inlet_gas,phi_range,p_exit,inletT,oxidizer,fuel,p_chamberRange)
    no_multi_process = time.clock()-start_time
    print(no_multi_process)
    soln1 = max_isp_different_pressures_multi_processing(cti_file,phi_range,p_exit,inletT,oxidizer,fuel,p_chamberRange)
    multi_process = time.clock() - no_multi_process
    print(multi_process)
    
    
    
    # args = p_chamber,p_exit,fuel,oxidizer
    # print(time.clock())
    # soln = maximum_isp(inlet_gas,args)
    # oxToFuelRatio = stoichRatio(inlet_gas,fuel,oxidizer,fuelSpecies,oxSpecies)/soln[-2]
    # print('The Maximum ISP occurs at this equivalence ratio: ', soln[-2])
    # print('The Maximum ISP occurs at this oxidizer to mass ratio: ',oxToFuelRatio)
    # print('the Maximum ISP is: ',soln[-1])