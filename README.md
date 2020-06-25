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
