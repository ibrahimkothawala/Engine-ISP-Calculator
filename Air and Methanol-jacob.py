#%% Imports, Constants, and Base Function Definitions
import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
import ISPcalculator
#constants
g = 9.81 #m/s  

#%% Sample inputs for main function   
inlet_gas = ct.Solution('gri30_highT.cti')
inlet_gas.basis = 'mass'
p_exit = ct.one_atm #pascals
p_chamber = 2068427.1 #pascals
fuelSpecies = ['CH3OH'] #molecules that the fuel is made up of
fuel = 'CH3OH' #fuel mixture
oxSpecies = ['O2','N2'] #molecules that make up the oxidizer mixture
oxidizer = 'O2:1.0,N2:3.76' #oxidizer mixture
phi_range = np.linspace(0.0001,10,100) #range of equivalence ratio for the calculation
args = p_chamber,p_exit,fuel,oxidizer
#%% #Plotting and Function Tests
soln = ISPcalculator.maximum_isp(inlet_gas,args)
oxToFuelRatio = ISPcalculator.stoichRatio(inlet_gas,fuel,oxidizer,fuelSpecies,oxSpecies)/soln[-2]
print('The Maximum ISP occurs at this equivalence ratio: ', soln[-2])
print('The Maximum ISP occurs at this oxidizer to mass ratio: ',oxToFuelRatio)
print('the Maximum ISP is: ',soln[-1])