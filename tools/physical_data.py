###########
# MODULES #
###########
import math

######################
# PHYSICAL CONSTANTS #
######################
NA: float = 6.02214076*10**23 # Avogadero constant -> mol-1
R: float = 8.31446261815324 # Gas constant -> J/K/mol
KB: float = 1.380649*10**(-23) # Boltzmann constant -> J/mol
activation_energy_glucose: float = 1.775*10**4 # Activation energy of the glucose-water diffusion -> J/mol
frequency_factor_glucose: float = 8.380046902993091*10**2 # approximation, assuming it is constant and not dependant on temperature -> m2/s


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
  return frequency_factor_glucose*math.exp(-activation_energy_glucose/(temperature*NA*KB))


#############
# MAIN CODE #
#############
if __name__ == "__main__":
  Diffusion_coef = 0.651
  Temperature = 298.15
  A = math.exp(-activation_energy_glucose/(NA*KB*Temperature))
  print(Diffusion_coef/A)