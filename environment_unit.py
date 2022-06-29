###########
# MODULES #
###########
import math

####################
# CLASS DEFINITION #
####################
class EnvironmentalUnit:
  """This class provides the smallest element of our environment
  Object of a square of length x width.
  This element is capable of welcoming only a single living individuals in it's surface
  Furthermore, it store environmental parameters such as temperature, pression, height etc.
  Attribute
  -------
  xlist : list
    List of all int x in the object
  ylist : list
    List of all int y in the object
  -------
  """
  
  width: int = 2
  length: int = 2

  x,y = 0,0

  is_occupied: bool = False
  
  volume: float = 1 # m³
  temperature: float = 0 # in K
  glucose_concentration: float = 0 # in kg/m³
  #oxygen_concentration: float = 0 # in kg/m³
  #nitrogen: float = 0 # in kg/m³
  #co2: float = 0 # in kg/m³3

  temperature_color: tuple = (0,0,0) # RGB
  
  glucose_color: tuple = (0,0,0) # RGB

  # FONDAMENTAL METHODS
  def __init__(self, posx: int, posy: int, temperature: float = 298.15):
    """
    Unit of a object Environment.
    Args:
      posx (int): positions on x axis
      posy (int): positions on y axis
      temperature (float) : temperature of the environmental unit, in Kelvin, default equal to 25°C or 298.15 K 
    """
    self.xlist: list = list(range(posx, posx + self.length))
    self.ylist: list = list(range(posy, posy + self.width))

    self.x, self.y = posx, posy

    self.rectangle_tuple = (self.x, self.y, self.width, self.length)

    self.temperature = temperature
    self.adaptTemperatureColor()


  def __str__(self) -> str:
    return f"""Unit at ({self.xlist[0]}, {self.ylist[0]}), having a temperature of:\t{self.temperature} Kelvin\n
  RED: {self.temperature_color[0]}\tGREEN: {self.temperature_color[1]}\tBLUE: {self.temperature_color[2]}"""

  
  # OTHER METHODS
  def changeGlucoseConcentration(self, glucose_mass: float) -> None:
    """Adds or removes concentration to the class attribute glucose_concentration

    Args:
      concentration (float): value to be added to glucose_concentration, can be negative in order to remove glucose from the environmental unit, in g/L
    """
    self.glucose_concentration += glucose_mass/self.volume


  def changeTemperature(self, temperature: float) -> None:
    """Replaces the actual temperature attribute of the environmental unit by the temperature argument

    Args:
      temperature (float): new temperature of the environmental unit, in Kelvin
    """
    self.temperature = temperature

  def adaptTemperatureColor(self) -> None:
    """Modifies the unit's temperature color according to its temperature 
        The color should be blue when the temperature is low, green when it is optimal and red when it's too high
    """
    
    self.temperature_color = (255/2*math.erf((self.temperature-350)/50)+255/2, # RED
                              255*math.exp(-1/1000*(self.temperature-320)**2), # GREEN
                              255*math.exp(-self.temperature/300) # BLUE
                              )  
    return None

############
# MAIN CODE #
#############
if __name__ == "__main__":
  unit1 = EnvironmentalUnit(5,5, temperature=200)
  
  print(unit1)
  
  
  # Color computations tests 
  