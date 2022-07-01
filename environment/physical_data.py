###########
# MODULES #
###########
import math

######################
# PHYSICAL CONSTANTS #
######################
TIME_ITERATION = 10**(-3) # Number of seconds flowing after each iteration of the game loop 
# Universal constants
NA: float = 6.02214076*10**23 # Avogadero constant -> mol-1
R: float = 8.31446261815324 # Gas constant -> J/K/mol
KB: float = 1.380649*10**(-23) # Boltzmann constant -> J/mol


# Glucose constants

GLUCOSE_ACTIVATION_ENERGY: float = 1.775*10**4 # Activation energy of the glucose-water diffusion -> J/mol
GLUCOSE_FREQUENCY_FACTOR: float = 8.380046902993091*10**2 # approximation, assuming it is constant and not dependant on temperature -> m2/s
GLUCOSE_DENSITY: float = 1.54*10**3 # kg/m³

# Water constants
WATER_DENSITY: float = 1.0*10**3 # kg/m³
WATER_THERMAL_CONDUCTIVITY = 0.6 # W/m/K


###########
# METHODS #
###########
def computeGlucoseDiffusionCoefficient(temperature: float) -> float:
  """Computes D, the coefficient of the diffusion of glucose in water solvant according to the temperature

  Args:
    temperature (float): the temperature of the solution of the environment, in Kelvin

  Returns:
    float: D, the coefficient of the diffusion of glucose in water solvant, in m²/s
  """
  return GLUCOSE_FREQUENCY_FACTOR*math.exp(-GLUCOSE_ACTIVATION_ENERGY/(temperature*NA*KB))


#############
# MAIN CODE #
#############
if __name__ == "__main__":
  Diffusion_coef = 0.651
  Temperature = 298.15
  A = math.exp(-GLUCOSE_ACTIVATION_ENERGY/(NA*KB*Temperature))
  print(Diffusion_coef/A)