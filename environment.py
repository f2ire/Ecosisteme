###########
# MODULES #
###########
import math
import numpy as np
from cell import Cell
from environment_unit import EnvironmentalUnit
import time as t
import tools.physical_data as constants
import pygame

####################
# CLASS DEFINITION #
####################
class Environment:
  """
  Class stocking multiple environment_unit in a double array
  """
  width, length = 0,0
  number_columns, number_rows = 0,0

  environment_grid = []
  

  def __init__(self, length: int, width: int, initial_temperature: float = 298.15) -> None:
    """Initialize an environment with a length * width size
    Args:
      length (int): length of the environment (length of window in pixel)
      width (int): width of the environment (width of window in pixel)
    """
    self.length: int = length
    self.width: int  = width
    self.number_columns: int = round(self.width / EnvironmentalUnit.width)
    self.number_rows: int = round(self.length / EnvironmentalUnit.length)
    
    # Create a environment_grid with an EnvironmentalUnit object in each columns and that for each rows
    self.environment_grid: list = [
      [EnvironmentalUnit(x * EnvironmentalUnit.width, y * EnvironmentalUnit.length, initial_temperature)
      for x in range(self.number_columns)]
      for y in range(self.number_rows)
    ]
    return None
  
  def __str__(self) -> str:
    index = 0
    string = f"Evironment dimension ({self.width},{self.length}) \n"
    # Representing the environment environment_grid with 1 when the 'pixel' is occupied and 0 when it is not.
    string += "["
    for n in range(self.number_columns):
      string += f"{n},"
    string += " ]\n"
    for row in self.environment_grid:
      string += "["
      for unit in row:
        if unit.is_occupied:
          string += "X "
        else :
          string += ". "
      string += f"]{str(index)}\n"
      index += 1
    
    return string
      
  ###########
  # METHODS #
  ###########
  def usedSpace(self, entity, xlist: np.array, ylist: np.array, delete: bool = False) -> None:
    """ Sets all the coordinates of the environment environment_grid occupied by the cell on 'occupied' or 'not occupied' depending on the value of delete.
    
    Args:
      entity :  object of any classes (Cell ...)
      delete (bool): if set to True then the is_occupied parameter of all environmental units is set to False
      xlist (np.array): array containing every coordinates on the environment grid of an entity along the x axis 
      ylist (np.array): array containing every coordinates on the environment grid of an entity along the y axis 
    """
    #print(math.floor(xlist[0]), math.floor(xlist[-1]), math.floor(ylist[0]), math.floor(ylist[-1]))
    for x in xlist:
      for y in ylist:
        self.environment_grid[math.floor(x) % self.number_columns][math.floor(y) % self.number_rows].is_occupied = not delete
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
    # Increments for the for loops because we need only to go from an unit to another
    #x_i, y_i = EnvironmentalUnit.width, EnvironmentalUnit.length useless for the moment
  
    
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
        if self.environment_grid[x % self.number_columns][y % self.number_rows].is_occupied:
          return False
        else:pass
    return True
  
  def glucoseDiffusion(self)-> None:
    """Adjusts the nutrients in every environmental units according to the diffusion rates and the gradient. 
    The idea is to check if the units in the neighbourhood (upward, downward, right and leftward) contain more glucose and simulate 
    the creation of a gradient. If the
    """
    for x in range(self.length,EnvironmentalUnit.length):
      for y in range(self.width,EnvironmentalUnit.width):
        if self.isThereMoreNutrientAround((x,y),(x-1,y)):
          leftward_flux = -self.computeGlucoseFlux(self.environment_grid[x][y].temperature, self.environment_grid[x][y].glucose_concentration, self.environment_grid[x-1][y].glucose_concentration)
        else:
          leftward_flux = self.computeGlucoseFlux(self.environment_grid[x][y].temperature, self.environment_grid[x][y].glucose_concentration, self.environment_grid[x-1][y].glucose_concentration)
        
        if self.isThereMoreNutrientAround((x,y),(x+1,y)):
          rightward_flux = -self.computeGlucoseFlux(self.environment_grid[x][y].temperature, self.environment_grid[x][y].glucose_concentration, self.environment_grid[x+1][y].glucose_concentration)
        else:
          rightward_flux = self.computeGlucoseFlux(self.environment_grid[x][y].temperature, self.environment_grid[x][y].glucose_concentration, self.environment_grid[x+1][y].glucose_concentration)
        
        if self.isThereMoreNutrientAround((x,y),(x,y-1)):
          upward_flux = -self.computeGlucoseFlux(self.environment_grid[x][y].temperature, self.environment_grid[x][y].glucose_concentration, self.environment_grid[x][y-1].glucose_concentration)
        else:
          upward_flux = self.computeGlucoseFlux(self.environment_grid[x][y].temperature, self.environment_grid[x][y].glucose_concentration, self.environment_grid[x][y-1].glucose_concentration)
        
        if self.isThereMoreNutrientAround((x,y),(x,y+1)):
          downward_flux = -self.computeGlucoseFlux(self.environment_grid[x][y].temperature, self.environment_grid[x][y].glucose_concentration, self.environment_grid[x][y+1].glucose_concentration)
        else:
          downward_flux = self.computeGlucoseFlux(self.environment_grid[x][y].temperature, self.environment_grid[x][y].glucose_concentration, self.environment_grid[x][y+1].glucose_concentration)

        self.environment_grid[x][y].changeGlucoseConcentration(leftward_flux+rightward_flux+upward_flux+downward_flux)


  def computeGlucoseFlux(self, temperature: float, concentration1: float, concentration2: float) -> float:
    """Computes J, the flux of matter of glucose between two environmental units in position 1 (reference) and 2

    Args:
      temperature (float): in Kelvin
      concentration1 (float): molar concentration of the chemical in position 1, by convention the one of reference in kg/L
      concentration2 (float): molar concentration of the chemical in position 2 in kg/L

    Returns:
      float: the flux of matter, in kg/m²/s
    """
    return -constants.density_glucose*constants.computeGlucoseDiffusionCoefficient(temperature)*(concentration1-concentration2)

  def isThereMoreNutrientsAround(self, reference_position: tuple, comparison_position: tuple) -> bool:
    """Returns True if the environmental units located at comparison_position around the reference one contains more of a specified chemical, 
    if it chemical concentration is higher 

    Args:
      reference_position (tuple): tuple of length 2 containing the x and y coordinates of the reference environmetal unit on the environment grid
      comparison_position (tuple): tuple of length 2 containing the x and y coordinates of the environmetal unit that is being compared on the environment grid

    Returns:
      bool: True if the chemical concentration in compared environmental is greater than the reference one 
    """
    x_ref, y_ref = reference_position[0], reference_position[1]
    x_comparison, y_comparison = comparison_position[0], comparison_position[1]
    return self.environment_grid[x_ref][y_ref] < self.environment_grid[x_comparison][y_comparison]


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


  def displayGlucoseMap(self) -> None:
    pygame.init()
    glucose_map = pygame.display.set_mode((self.width, self.length))

#############
# MAIN CODE #
#############
if __name__ == "__main__":
  environment = Environment(100,100,200)
  immobile_cell = Cell(environment,25,30)
  mobile_cell = Cell(environment,18,17)

  # Display tests
  environment.displayTemperatureMap()

  # Colision tests
  #for i in range(15):
  #  print(environment)
  #  mobile_cell.moving(environment, direction=(0,1))
  #  t.sleep(1)