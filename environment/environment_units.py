###########
# MODULES #
###########
import math
import physical_data as phy

####################
# CLASS DEFINITION #
####################
class EnvironmentUnit:
  """The fondamental unit of the environment represented by a cube of shape width x length x height.
  This class is used to keep tracks of the position of entities in the environment. 
  This class is also used to defined other units that will store essential data for the environment.
  This class contains attributes shared by all the subclasses.
  For the calculus, an unit is represented as a cube of water.

  Attributes :
    width (int): the size of one side of the unit, in m
    length (int): the size of one side of the unit, in m
    height (int): the size of one side of the unit, in m
    surface (float): surface of one unit, in m²
    volume (float): volume of one unit, in m³
    mass (float): total mass of one unit, calculated as it's a cube of water
    x (int): positional x coordinates of the unit
    y (int): positional y coordinates of the unit
    is_occupied (bool): True if the occupation unit is occupated by an entity of the environment, False if nothing lays in it
  """
  width: int = 2*10**(-3) # m
  length: int = 2*10**(-3) # m 
  height: int = 2*10**(-3) # m
  surface: float = width * length # m²
  volume: float =  width * length * height # m³
  mass: float = volume * phy.WATER_DENSITY # kg

  x: int
  y: int

  is_occupied: bool = False

  def __init__(self, posx: int, posy: int) -> None:
    self.x, self.y = posx, posy

  def __str__(self) -> str:
    return f"""Unit of shape {self.width} x {self.length}\nAt position ({self.x}, {self.y})\n"""


class TemperatureUnit(EnvironmentUnit):
  """An environmental unit used to store and modify the temperature of the environment.
  
  Attributes :
    temperature (float): temperature of the unit, in Kelvin
    color (tuple): tuple in RGB format, used to display a temperature map of the environment
  
  Functions : 
    changeTemperature
    adaptTemperatureColor
  """
  temperature: float
  color: tuple

  def __init__(self, posx: int, posy: int, initial_temperature: float) -> None:
    """
      initial_temperature (float): initial temperature of the unit, in Kelvin
    """
    super().__init__(posx, posy)
    self.temperature = initial_temperature
    self.adaptTemperatureColor()

  def __str__(self) -> str:
    return super().__str__() + f"Having a temperature of : {self.temperature} K\nIts color in RGB encoding is : ({self.color[0]},{self.color[1]},{self.color[2]})\n"

  def changeTemperature(self, thermal_flux: float) -> None:
    """Update the actual temperature attribute of the temperature unit according to the thermal flux it's receiving.
    Calculus is made following the equation Tf = Ti + Q/(m*c). Tf and Ti are final and initial temperature of the unit.
    m is the total mass of the unit, c it's heat capacity and Q the received thermal energy

    Args:
      thermal_flux (float): thermal flux the unit is receiving, in W
    """
    self.temperature += phy.computeThermalEnergy(thermal_flux) / (self.mass * phy.WATER_HEAT_CAPACITY) 
  
  def adaptTemperatureColor(self) -> None:
    """Modifies the unit's temperature color according to its temperature.
    The color should be blue when the temperature is low, green when it is optimal and red when it's too high.
    """
    self.color = (255/2*math.erf((self.temperature-350)/50)+255/2,
                              255*math.exp(-1/1000*(self.temperature-320)**2),
                              255*math.exp(-self.temperature/300))


class GlucoseUnit(EnvironmentUnit):
  """An environmental unit used to store and modify the glucose concentration of the environment.
  
  Attributes :
    glucose_concentration (float): glucose concetration of the unit, in km/m³
    color (tuple): tuple in RGB format, used to display a glucose map of the environment
  
  Functions : 
    changeGlucoseConcentration
    adaptGlucoseColor
  """
  glucose_concentration: float
  color: tuple

  def __init__(self, posx: int, posy: int, initial_concentration: float) -> None:
    """
      initial_concentration (float): initial glucose concentration, in kg/m³
    """
    super().__init__(posx, posy)
    self.glucose_concentration = initial_concentration
    self.adaptGlucoseColor()
  
  def __str__(self) -> str:
    return super().__str__() + f"Having a glucose concentration of : {self.glucose_concentration} kg.m⁻³\nIts color in RGB encoding is : ({self.color[0]},{self.color[1]},{self.color[2]})\n"
  
  def changeGlucoseConcentration(self, glucose_added_mass: float) -> None:
    """Updates the actual glucose concentration of the unit according to an incoming mass of glucose. 

    Args:
      glucose_added_mass (float): mass of glucose transiting through the unit, in kg. 
        Positive if the unit is receiving glucose, negative if it's losing
    """
    self.glucose_concentration += glucose_added_mass/self.volume
    self.adaptGlucoseColor()

  def adaptGlucoseColor(self) -> None:
    """Modifies the unit's color following a linear relationship with it's glucose concentration.
    When the concentration is equal to zéro, the color of the unit is mainly red. 
    When the concetration is hight, the color becames green.
    """
    self.color = (255-255*self.glucose_concentration,
    255*self.glucose_concentration,
    45)


#############
# MAIN CODE #
#############
if __name__ == "__main__":
  test_occupation_unit = EnvironmentUnit(0,0)
  test_temperature_unit = TemperatureUnit(1,0,298.15)
  test_glucose_unit = GlucoseUnit(0,1,0.005)

  # Print tests
  print(test_occupation_unit) # OK
  print(test_temperature_unit) # OK
  print(test_glucose_unit) # OK

  # Variable change tests
  test_temperature_unit.changeTemperature(thermal_flux=0.5) ; print(test_temperature_unit.temperature == (5*10**(-4)/(8*10**(-6)*4.185*10**3))+298.15)
  test_glucose_unit.changeGlucoseConcentration(5*10**(-10)) ; print(test_glucose_unit.glucose_concentration == 0.005+0.5/8)