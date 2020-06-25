# Engine-ISP-Calculator
## Required Libraries
- Cantera
- Numpy
- Matplotlib
- multiprocessing (only needed if you want to run analysis in multiproccessing mode)
- OS
- Functools
- time

## How is the ISP calculated?
There are two diffrent methods that this calculator uses to determine the maximum theoretical engine ISP. Both methods utilize conservation of energy to determine the exit velocity of the combustion products. For more information read the NASA CEA document: https://www.grc.nasa.gov/WWW/CEAWeb/RP-1311.pdf section 6. Both methods assume infinite combustor size and instantaneous equilibrium. 
They both utilize Cantera to calculate the thermodynamic properties of the gas. Cantera utilizes cti files to store  the NASA polynomials that are used to estimate the thermydynamic properties. The cti file in this repository is the gri30_highT. 

### First Method: Constant Entropy and Constant Specific Heat
This method assumes an isentropic process and that the specific heat of the gasses is constant after the reactants have been combusted. It first calculates the temperature at the inlet of engine (after reactants have been combusted) and the temperature at the nozzle exit. Then determines the enthalpy change using the specfic heat. After, it sets the change in enthalpy equal to the kinetic energy change and solves for the exit velocity. 

### Second Method: Constant Entropy
This method assumes only an isentropic process after the reactatns have been combusted. It calculates the entropy at the inlet of the engine and uses that entropy and the nozzle exit pressure to determine the enthalpy change. Which is then used to calcuate the exit velocity. 

## What is the Maximum ISP and how is it found?
In order to determine the best oxidizer to fuel mass ratio for the highest ISP, the ISP calculator is run at differnt oxidizer to mass fuel ratios. The maximum ISP is found in this series and the resulting oxidizer to mass fuel ratio is returned. 

## How to use Engine ISP Calculator
The ISPCalculator.py contains all the neccessary functions to run the different methods. In addition, there are other functions that can be used to calculate the ISP of propellents at different inlet pressures (currently the exit pressure is assumed to be 1 atmosphere). Another function is there that utilizes multiprocessing in order to decrease program run time. It only reduces run time with very large datasets.

## Reccomended Workflow
Create a new python file for each new engine that needs the optimal ISP to be determined. Determine over which oxidizer to fuel mass ratios the ISP needs to be calculated and if needed which inlet pressures the engine is operating at or a series of potential inlet pressures for the engine. Import the ISPcalculator.py file and utilize the appropriate functions. 