###########
# MODULES #
###########
import math
from pipes import Template

######################
# PHYSICAL CONSTANTS #
######################
NA: float = 6.02214076*10**23 # Avogadero constant
R: float = 8.31446261815324 # Gas constant
KB: float = 1.380649*10**(-23) # Boltzmann constant
EA: float = 1.775*10**4 # Activation energy of the glucose-water diffusion -> J/mol
D0 = 7.7684529398*10**(-4) # approximation of the frequency factor of the glucose-water diffusion


###########
# METHODS #
###########
def computeGlucoseDiffusionCoefficient(temperature: float) -> float:
  """Computes D, the coefficient of the diffusion of glucose in water solvant according to the temperature

  Args:
    temperature (float): the temperature of the solution of the environment, in Kelvin

  Returns:
    float: D, the coefficient of the diffusion of glucose in water solvant. 
  """
  return D0*math.exp(-EA/(temperature*NA*KB))


#############
# MAIN CODE #
#############
if __name__ == "__main__":
  Diffusion_coef = 0.651
  Temperature = 298.15
  A = math.exp(-EA/(NA*KB*Temperature))
  print(Diffusion_coef/A)