"""
Created on: 9/14/2019 at 1:49pm
Author: Jacob Posey
Last Updated: 1/27/2020
"""
#%%Imports
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cantera as ct
plt.rcParams.update({'font.size':18})
#%%Initializers
u_ = np.zeros(3)
T_ = np.zeros(3)
p_ = np.zeros(3)
A_ = np.zeros(3)
D_ = np.zeros(3)
M_ = np.zeros(3)
c_ = np.zeros(3)
rho_ = np.zeros(3)
#%%Inputs
option0 = 0
Lstar = 3
mdotIGN = 4.606/1000
mdotO = 0.2 #oxidizer mass flow rate [kg/s]
FOS = 10 #factor of safety for chamber thickness [-]
p_[0] = 300*6894.757 #chamber pressure [Pa]
D_[0] = 3*0.0254 #chamber diameter [m]
p_[2] = 1*101325
theta = np.radians(15)
N = 4000
OF = 1.4
flatStep = 0.006
#%%Constants
g = 9.80665
Ru = 8.314
M_[1] = 1
#%%Thermodynamic Equilibrium
if option0 == 0:
	IspRange = []
	OFrange = np.linspace(0.1,10,100)
	h = 0 #index for selecting optimal ISP
	for ii in range(100):
		gas = ct.Solution('gri30_highT.cti')
		gas.TPY = 298,p_[0],{'CH3OH':1,'O2':OFrange[ii],'N2':3.76*OFrange[ii]}
		gas.equilibrate('HP')
		gamma = gas.cp_mass/gas.cv_mass
		M_avg = gas.mean_molecular_weight
		T_[0] = gas.T
		IspRange.append((1/g)*np.sqrt(2*((gamma*Ru*1000)/((gamma-1)*M_avg))*T_[0]*(1-((p_[2]/p_[0])**((gamma-1)*gamma)))))
		if ii > 0:
			if IspRange[ii] > IspRange[ii-1]:
				h = ii
	OF = OFrange[h]
gas = ct.Solution('gri30_highT.cti')
gas.TPY = 298,p_[0],{'CH3OH':1,'O2':OF,'N2':3.76*OF}
gas.equilibrate('HP')
M_avg = gas.mean_molecular_weight
T_[0] = gas.T
gamma = gas.cp_mass/gas.cv_mass
#%%Isentropic Calculations
# mdot = mdotO+(mdotO/OF)+mdotIGN
# R = (Ru*1000)/M_avg
# rho_[0] = p_[0]/(R*T_[0])
# A_[0] = np.pi*((D_[0]/2)**2)
# u_[0] = mdot/(A_[0]*rho_[0])
# p_[1] = p_[0]*((2/(gamma+1))**(gamma/(gamma-1)))
# rho_[1] = rho_[0]*((2/(gamma+1))**(1/(gamma-1)))
# T_[1] = T_[0]*(2/(gamma+1))
# c_[1] = np.sqrt(gamma*R*T_[1])
# u_[1] = c_[1]
# A_[1] = mdot/(rho_[1]*c_[1])
# D_[1] = 2*np.sqrt(A_[1]/np.pi)
# u_[1] = mdot/(rho_[1]*A_[1])
# M_[2] = np.sqrt(((gamma+1)/(gamma-1))*(((p_[1]/p_[2])**((gamma-1)/gamma))-(2/(gamma+1))))
# A_[2] = (A_[1]/M_[2])*((((gamma+1)/2)/(1+((gamma-1)/2)*(M_[2]**2)))**((gamma+1)/(2-(2*gamma))))
# D_[2] = 2*np.sqrt(A_[2]/np.pi)
# T_[2] = T_[1]/((2/(gamma+1))+(((gamma-1)/(gamma+1))*(M_[2]**2)))
# c_[2] = np.sqrt(gamma*R*T_[2])
# u_[2] = M_[2]*c_[2]
# rho_[2] = p_[2]/(R*T_[2])
# F = (u_[2]*mdot)+((p_[2]-101325)*A_[2])
# Isp = u_[2]/g
# epsC = A_[0]/A_[1]
# epsE = A_[2]/A_[1]
# c_[0] = np.sqrt(gamma*R*T_[0])
# M_[0] = u_[0]/c_[0]
# cStar = (p_[0]*A_[1])/mdot
# #%%Contour Drawing
# m = [-np.tan(2*theta),np.sin(theta)]
# xt = ((D_[1]/2)-(D_[0]/2))/m[0]
# xE = (((D_[2]/2)-(D_[1]/2))/m[1])+xt+flatStep
# x = np.linspace(0,xE,N)
# y = []
# for ii in range(N):
# 	if x[ii] <= xt+flatStep:
# 		if x[ii] <= xt:
# 			y.append((m[0]*x[ii])+(D_[0]/2))
# 		else:
# 			y.append(D_[1]/2)
# 	elif x[ii] > xt+flatStep:
# 		y.append((m[1]*(x[ii]-xt-flatStep))+(D_[1]/2))
# Lc = (Lstar-((1/3)*np.sqrt(A_[1]/np.pi)*(1/np.tan(2*theta))*((epsC**(1/3))-1)))/epsC
# plt.plot([-Lc,0],[D_[0]/2,D_[0]/2])
# plt.plot(x,y)
# plt.axis('equal')
# path = pd.DataFrame(data=[np.array(x),np.array(y),np.pi*(np.array(y)**2)])
# contour = pd.DataFrame(data=[np.hstack((np.linspace(0,Lc,N),np.array(x)+Lc)),np.hstack((np.ones(N)*(D_[0]/2),np.array(y)))])
# path = path.transpose()
# contour = contour.transpose()
# path.to_csv('AirEngine.csv',index=False)
# contour.to_csv('AirEngineContour.csv',index=False)
# #%%MOM Analysis
# sigy = 413685438
# thicc = (p_[0]*(D_[0]/2))/(sigy/FOS)