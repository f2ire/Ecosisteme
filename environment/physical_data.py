###########
# MODULES #
###########
import math

######################
# PHYSICAL CONSTANTS #
######################
TIME_ITERATION: int = 10**(-3) # Number of seconds flowing after each iteration of the game loop 
# Universal constants
NA: float = 6.02214076*10**23 # Avogadero constant -> mol-1
R: float = 8.31446261815324 # Gas constant -> J/K/mol
KB: float = 1.380649*10**(-23) # Boltzmann constant -> J/mol


# Glucose constants
GLUCOSE_DIFFUSION_COEFFICIENT: float = 0.651 # taken as constant for T = 298.15 K, in m²/s
GLUCOSE_DENSITY: float = 1.54*10**3 # kg/m³

# Water constants
WATER_DENSITY: float = 1.0*10**3 # kg/m³
WATER_THERMAL_CONDUCTIVITY: float = 0.6 # W/m/K
WATER_HEAT_CAPACITY: float = 4.185*10**3 # J/K/kg 


###########
# METHODS #
###########
def computeThermalEnergy(thermal_flux: float) -> float:
  """Returns Q, the thermal energy according to the formula :
  Q = Flux * dt where dt is the time of one iteration of the loop

  Args:
    thermal_flux (float): thermal flux, in W

  Returns:
    float: Q, the thermal energy, in J
  """
  return thermal_flux * TIME_ITERATION

def computeGlucoseFlux(concentration1: float, concentration2: float) -> float:
  """Computes J, the flux of matter of glucose between two environmental units in position 1 (reference) and 2 
  according to Fick's law of matter diffusion. J = rho*D*(C1-C2) 

  Args:
    concentration1 (float): molar concentration of the chemical in position 1, by convention the one of reference in kg/L
    concentration2 (float): molar concentration of the chemical in position 2 in kg/L

  Returns:
    float: the flux of matter, in kg/m²/s. Positive if concentration2 > concentration1
  """
  return -GLUCOSE_DENSITY*GLUCOSE_DIFFUSION_COEFFICIENT*(concentration1-concentration2)
  
def computeThermalFlux(temperature1: float, temperature2: float) -> float:
  """Computes phi, the thermal transfert from temperature1 to temperature2 in W/m² according to 
  Fourier's law of thermal diffusion
  
  Args:
    temperature1 (float): temperature, in K
    temperature2 (float): temperature, in K
  
  Returns:
    float: thermal flux, in W. Positive if temperature2 > temperature1, negative otherwise.
  """
  return -WATER_THERMAL_CONDUCTIVITY*(temperature1-temperature2)


#############
# MAIN CODE #
#############
if __name__ == "__main__":
  # Glucose flux computation tests
  print(computeThermalEnergy(5) == 0.005)
  print(computeGlucoseFlux(0.001,0.006)-5.0127 < 10**(-6)) # OK
  print(computeThermalFlux(350,300)== -30) # OK