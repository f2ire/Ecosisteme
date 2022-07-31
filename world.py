###########
# MODULES #
###########
from environment.environment_grids import *
from environment.environment_units import *
import math
import pygame

####################
# CLASS DEFINITION #
####################
class World:
  """
  Class containing all the physical and chemical grids needed to represent a functional environment.

  Attributes:
    width (float) : size of the width of the world in meters
    length (float) : size of the length of the world in meters
    environment_grid (EnvironmentGrid) : object of class EnvironmentGrid
    temperature_grid (TemperatureGrid) : object of class TemperatureGrid
    glucose_grid (GlucoseGrid) : object of class GlucoseGrid
  """
  width: int # m
  length: int # m

  environment_grid: EnvironmentGrid
  temperature_grid: TemperatureGrid
  glucose_grid: GlucoseGrid
  
  def __init__(self, width: int, length: int, initial_temperature: float = 298.15, initial_glucose: float = 0) -> None:
    """Initialize an environment with a length x width size
    Args:
      width (int): width of the environment in meters
      length (int): length of the environment in meters
      initial_temperature (float): initial value of temperature of the environment in Kelvin 
      initial_glucose (float): initial value of glucose concentration in the environment in kg.m⁻³
    """
    self.width, self.length = width, length
    
    self.environment_grid = EnvironmentGrid(self.width, self.length )
    self.temperature_grid = TemperatureGrid(self.width, self.length , initial_temperature)
    self.glucose_grid = GlucoseGrid(self.width, self.length , initial_glucose)
  
  def __str__(self) -> str: 
    string = f"Evironment dimension ({self.width},{self.length}) \n"+str(self.environment_grid)
    string += str(self.environment_grid)
    return string
      
  ###########
  # METHODS #
  ###########
  def getWorldScale(self) -> int:
    return round(math.log10(self.width))

  def computeWindowSize(self) -> tuple:
    scale = -self.getWorldScale()
    return (2.4 * self.width * 10**(scale + 2), 2.4 * self.length * 10**(scale + 2))

  def createUnitDisplayRectangle(self, x_position: int, y_position: int) -> tuple:
    scale = -self.getWorldScale()
    return (x_position, y_position, EnvironmentUnit.width * 10**(scale + 2.3), EnvironmentUnit.length * 10**(scale + 2.3))

  def displayTemperatureMap(self) -> None:
    """Display the temperature map of the environment using pygame
    """
    pygame.init()
    window_dimension = self.computeWindowSize()
    temperature_map = pygame.display.set_mode(window_dimension)
    self.temperature_grid.computeAllTemperatureColors()
    while True:
      event = pygame.event.poll()  # Collecting an event from the user
      if event.type == pygame.QUIT:  # End loop if user click on cross butun
        break

      x,y = 20,20
      for row in self.temperature_grid.temperature_units_list:
        for temp_unit in row:
          temp_unit: TemperatureUnit
          temp_unit_display_rectangle = self.createUnitDisplayRectangle(x,y)
          temperature_map.fill(temp_unit.color, temp_unit_display_rectangle)
          x += temp_unit_display_rectangle[2]
        x = 20
        y += temp_unit_display_rectangle[3]
      pygame.display.flip()
    pygame.quit()

  def displayGlucoseConcentrationMap(self) -> None:
    pygame.init()
    window_dimension = self.computeWindowSize()
    glucose_map = pygame.display.set_mode(window_dimension)
    self.glucose_grid.computeAllGlucoseColor()
    while True:
      event = pygame.event.poll()  # Collecting an event from the user
      if event.type == pygame.QUIT:  # End loop if user click on cross butun
        break

      x,y = 20,20
      for row in self.glucose_grid.glucose_units_list:
        for glucose_unit in row:
          glucose_unit: TemperatureUnit
          glucose_unit_display_rectangle = self.createUnitDisplayRectangle(x,y)
          glucose_map.fill(glucose_unit.color, glucose_unit_display_rectangle)
          x += glucose_unit_display_rectangle[2]
        x = 20
        y += glucose_unit_display_rectangle[3]
      pygame.display.flip()
    pygame.quit()

#############
# MAIN CODE #
#############
if __name__ == "__main__":
  the_world = World(10**(-5), 10**(-5)) # 40 x 40 units
  print(the_world) # OK
  print(the_world.getWorldScale() == -5) # OK
  print(the_world.computeWindowSize() == (240,240)) # OK
  print(the_world.createUnitDisplayRectangle(5,3) == (5,3,25*10**(-0.7),25*10**(-0.7))) # OK
  the_world.temperature_grid.changeMultipleTemperature([3,4,5,6],[3,4,5,6],2000)
  the_world.displayTemperatureMap() # OK
  the_world.glucose_grid.changeMultipleGlucoseConcentration([3,4,5,6],[3,4,5,6],0.004)
  #the_world.displayGlucoseConcentrationMap() # OK