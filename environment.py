###########
# MODULES #
###########
import math
import numpy as np
from cell import Cell
from environment_unit import EnvironmentalUnit
from environment_grid import EnvironmentGrid
import time as t
import physical_data as phy
import pygame

####################
# CLASS DEFINITION #
####################
class Environment:
  """
  Class stocking multiple environment_unit in a double array. In this class, every function related to 
  """
  width: int
  length: int

  environment_grid: EnvironmentGrid
  

  def __init__(self, length: int, width: int, initial_temperature: float = 298.15) -> None:
    """Initialize an environment with a length * width size
    Args:
      length (int): length of the environment (length of window in pixel)
      width (int): width of the environment (width of window in pixel)
    """
    self.length = length
    self.width  = width
    
    # Create a environment_grid with an EnvironmentalUnit object in each columns and that for each rows
    self.environment_grid = EnvironmentGrid(round(self.width / EnvironmentalUnit.width), round(self.length / EnvironmentalUnit.length))
    return None
  
  def __str__(self) -> str: 
    return f"Evironment dimension ({self.width},{self.length}) \n"+str(self.environment_grid)
      
  ###########
  # METHODS #
  ###########
  def usedSpace(self, xlist: np.array, ylist: np.array, delete: bool = False) -> None:
    """ Sets all the coordinates of the environment environment_grid occupied by the cell on 'occupied' or 'not occupied' depending on the value of delete.
    
    Args:
      delete (bool): if set to True then the is_occupied parameter of all environmental units is set to False
      xlist (np.array): array containing every coordinates on the environment grid of an entity along the x axis 
      ylist (np.array): array containing every coordinates on the environment grid of an entity along the y axis 
    """
    for x in xlist:
      for y in ylist:
        self.environment_grid.getEnvironmentalUnit(math.floor(x) % self.environment_grid.colum_number, math.floor(y) % self.environment_grid.row_number).is_occupied = not delete
    return None


  def isSpace(self, xlist: np.array, ylist: np.array, direction: tuple) -> bool:
    """ Checks if the environment units in a certain direction are available for the entity to move or replicate

    Args:
      xlist (np.array): array containing every coordinates on the environment environment_grid of an entity along the x axis 
      ylist (np.array): array containing every coordinates on the environment environment_grid of an entity along the y axis 
      direction (tuple): tuple of the maximum (absolute value) coordinates where the action will took place. For a cell entity, 
                         it should either be the values of the movement or the place where the daughter cell gonna appear

    Returns:
      bool: True if the space is available for the action, False if not
    """
    # Maximisation of the movement because it has to be an integer in order to be casted in the environment environment_grid
    # Multiplication by 2 or else the checking happens only on the surface of the actual entity
    if direction[0] > 0:
      xm = 2*math.ceil(direction[0])
    else:
      xm = math.floor(2*direction[0])
    if direction[1] > 0:
      ym = 2*math.ceil(direction[1])
    else:
      ym = math.floor(2*direction[1])

    xstart, ystart, xend, yend = math.floor(xlist[0]), math.floor(ylist[0]), math.floor(xlist[-1]), math.floor(ylist[-1])
    #print(xstart,xend,xm,";",ystart,yend,ym)
    
    if xm > 0 and ym == 0:
      return self.areAllUnitsNotOccupied(xend, xend+xm, ystart, yend)

    elif xm < 0 and ym == 0:
      return self.areAllUnitsNotOccupied(xstart+xm, xstart, ystart, yend)

    elif xm == 0 and ym > 0:
      return self.areAllUnitsNotOccupied(xstart, xend, yend, yend+ym)

    elif xm == 0 and ym < 0:
      return self.areAllUnitsNotOccupied(xstart, xend, ystart+ym, ystart)

    elif xm > 0 and ym > 0:
      if self.areAllUnitsNotOccupied(xend, xend+xm, ystart+ym, yend+ ym):
        if self.areAllUnitsNotOccupied(xstart+xm, xend, yend, yend+ym):
          return True
      return False 

    elif xm > 0 and ym < 0:
      if self.areAllUnitsNotOccupied(xend, xend+xm, ystart+ym, yend+ ym):
        if self.areAllUnitsNotOccupied(xstart+xm, xend, ystart+ym, ystart):
          return True
      return False 

    elif xm < 0 and ym > 0:
      if self.areAllUnitsNotOccupied(xstart+xm, xstart, ystart+ym, yend+ym):
        if self.areAllUnitsNotOccupied(xstart, xend+xm, yend, yend+ym):
          return True
      return False
      
    else:
      if self.areAllUnitsNotOccupied(xstart+xm, xstart, ystart+ym, yend+ym):
        if self.areAllUnitsNotOccupied(xstart, xend+xm, ystart+ym, ystart):
          return True
      return False

  
  def areAllUnitsNotOccupied(self, starting_x: int, ending_x: int, starting_y: int, ending_y: int) -> bool:
    """Navigates in all the environmental units of the environment grid between the starting x and y coordinates and the ending x and y. 
    For each environmental unit encountered, it checks its is_occupied attribute. If it's set on True, then the function returns False.
    The function returns True if and only if every environmental units have their is_occuied attribute set on False. 

    Args:
      starting_x (int): x coordinates of the environment grid where to begin the search 
      ending_x (int): x coordinates of the environment grid where to end the search
      starting_y (int): y coordinates of the environment grid where to begin the search 
      ending_y (int): y coordinates of the environment grid where to end the search

    Returns:
      bool: True if every environmental units have their is_occuied attribute set on False, False otherwise.
    """
    for x in range(starting_x, ending_x):
      for y in range(starting_y, ending_y):
        if self.environment_grid.getEnvironmentalUnit(x % self.number_columns, y % self.number_rows).is_occupied:
          return False
        else:pass
    return True
  
  def diffuseGlucose(self)-> None:
    """Adjusts the glucose concentration in every environmental units.
    For each environmental unit, 4 flux are calculated, one for each unit directly in contact with it
    """
    for x in range(self.length):
      for y in range(self.width):
        leftward_flux = self.computeGlucoseFlux(self.environment_grid[x][y].temperature, self.environment_grid[x][y].glucose_concentration, self.environment_grid[x-1][y].glucose_concentration)
        rightward_flux = self.computeGlucoseFlux(self.environment_grid[x][y].temperature, self.environment_grid[x][y].glucose_concentration, self.environment_grid[x+1][y].glucose_concentration)
        upward_flux = self.computeGlucoseFlux(self.environment_grid[x][y].temperature, self.environment_grid[x][y].glucose_concentration, self.environment_grid[x][y-1].glucose_concentration)
        downward_flux = self.computeGlucoseFlux(self.environment_grid[x][y].temperature, self.environment_grid[x][y].glucose_concentration, self.environment_grid[x][y+1].glucose_concentration)
        self.environment_grid[x][y].changeGlucoseConcentration(leftward_flux+rightward_flux+upward_flux+downward_flux)


  def computeGlucoseFlux(self, temperature: float, concentration1: float, concentration2: float) -> float:
    """Computes J, the flux of matter of glucose between two environmental units in position 1 (reference) and 2 
    according Fick's law of matter diffusion.

    Args:
      temperature (float): in Kelvin
      concentration1 (float): molar concentration of the chemical in position 1, by convention the one of reference in kg/L
      concentration2 (float): molar concentration of the chemical in position 2 in kg/L

    Returns:
      float: the flux of matter, in kg/m²/s
    """
    return -phy.density_glucose*phy.computeGlucoseDiffusionCoefficient(temperature)*(concentration1-concentration2)

  
  def diffuseTemperature(self) -> None:
    """Adjusts the temperature of every environmental units in the enviroment_grid according to Fourier's law of thermal diffusion
    For each environmental unit, 4 flux are calculated, one for each unit directly in contact with it
    """
    for x in range(self.length):
      for y in range(self.width):
        lefward_flux = self.computeThermalFlux(self.environment_grid[x][y].temperature, self.environment_grid[x-1][y].temperature)
        rightward_flux = self.computeThermalFlux(self.environment_grid[x][y].temperature, self.environment_grid[x+1][y].temperature)
        upward_flux = self.computeThermalFlux(self.environment_grid[x][y].temperature, self.environment_grid[x][y-1].temperature)
        downward_flux = self.computeThermalFlux(self.environment_grid[x][y].temperature, self.environment_grid[x][y+1].temperature)
        self.environment_grid[x][y].changeTemperature(lefward_flux+rightward_flux+upward_flux+downward_flux)


  def computeThermalFlux(self, temperature1: float, temperature2: float) -> float:
    """Computes phi, the thermal transfert from temperature1 to temperature2 in W/m² according to Fourier's law of thermal diffusion

    Args:
      temperature1 (float): temperature, in K
      temperature2 (float): temperature, in K

    Returns:
      float: thermal flux, in W/m². Positive if temperature2 > temperature1, negative otherwise.
    """
    return -phy.thermal_conductivity_water*(temperature1-temperature2)

  def displayTemperatureMap(self) -> None:
    """Display the temperature map of the environment using pygame
    """
    pygame.init()
    temperature_map = pygame.display.set_mode((self.width+10, self.length+10))
    self.computeAllTemperatureColors()
    while True:
      event = pygame.event.poll()  # Collecting an event from the user
      if event.type == pygame.QUIT:  # End loop if user click on cross butun
        break

      for x in range(self.number_columns):
        for y in range(self.number_rows):
          temperature_map.fill(self.environment_grid[x][y].temperature_color, self.environment_grid[x][y].rectangle_tuple)
          pygame.display.flip()
    pygame.quit()


  def computeAllTemperatureColors(self) -> None:
    """For each environmtal units in the environment grid, computes its temperature_color with the adaptTemperatureColor function 
    """
    for x in range(self.number_columns):
      for y in range(self.number_rows):
        self.environment_grid[x][y].adaptTemperatureColor()


  def displayGlucoseConcentrationMap(self) -> None:
    pygame.init()
    glucose_map = pygame.display.set_mode((self.width, self.length))

#############
# MAIN CODE #
#############
if __name__ == "__main__":
  environment = Environment(100,100,200)
  immobile_cell = Cell(environment,25,30)
  mobile_cell = Cell(environment,18,17)

  # Print test
  print(environment)

  # Display tests
  environment.displayTemperatureMap()

  # Colision tests
  #for i in range(15):
  #  print(environment)
  #  mobile_cell.moving(environment, direction=(0,1))
  #  t.sleep(1)