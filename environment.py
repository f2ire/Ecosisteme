###########
# MODULES #
###########
import math
import numpy as np
from cell import Cell
from environment_unit import EnvironmentalUnit
import time as t

####################
# CLASS DEFINITION #
####################
class Environment:
  """
  Class stocking multiple environment_unit in a double array
  """
  # Parameters 
  nutrients_diffusion = 0.05 # in g/min
  #glucose_diffusion = 0.004 # in g/min
  #nitrogen_diffusion = 0.02 # in g/min
  #oxygen_diffusion = 3 # in g/min
  #co2_diffusion = 1 # in g/min

  def __init__(self, length: int, width: int) -> None:
    """Initialize an environment with a length * width size
    Args:
      length (int): length of the environment (length of window in pixel)
      width (int): width of the environment (width of window in pixel)
    """
    self.length: int = length
    self.width: int  = width
    self.number_columns: int = round(self.width / EnvironmentalUnit.width)
    self.number_rows: int = round(self.length / EnvironmentalUnit.length)
    
    # Create a grid with an EnvironmentalUnit object in each columns and that for each rows
    self.grid: list = [
      [EnvironmentalUnit(x * EnvironmentalUnit.width, y * EnvironmentalUnit.length)
      for x in range(self.number_columns)]
      for y in range(self.number_rows)
    ]
    return None
  
  def __str__(self) -> str:
    index = 0
    string = f"Evironment dimension ({self.width},{self.length}) \n"
    # Representing the environment grid with 1 when the 'pixel' is occupied and 0 when it is not.
    string += "["
    for n in range(self.number_columns):
      string += f"{n},"
    string += " ]\n"
    for row in self.grid:
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
    """ Sets all the coordinates of the environment grid occupied by the cell on 'occupied' or 'not occupied' depending on the value of delete.
    
    Args:
      entity :  object of any classes (Cell ...)
      delete (bool): if set to True then the is_occupied parameter is set to False
      xlist (np.array): array containing every coordinates on the environment grid of an entity along the x axis 
      ylist (np.array): array containing every coordinates on the environment grid of an entity along the y axis 
    """
    #print(math.floor(xlist[0]), math.floor(xlist[-1]), math.floor(ylist[0]), math.floor(ylist[-1]))
    for x in xlist:
      for y in ylist:
        self.grid[math.floor(x) % self.number_columns][math.floor(y) % self.number_rows].is_occupied = not delete
    return None


  def isSpace(self, xlist: np.array, ylist: np.array, direction: tuple) -> bool:
    """ Checks if the environment units in a certain direction are available for the entity to move or replicate

    Args:
      xlist (np.array): array containing every coordinates on the environment grid of an entity along the x axis 
      ylist (np.array): array containing every coordinates on the environment grid of an entity along the y axis 
      direction (tuple): tuple of the maximum (absolute value) coordinates where the action will took place. For a cell entity, 
                         it should either be the values of the movement or the place where the daughter cell gonna appear

    Returns:
      bool: True if the space is available for the action, False if not
    """
    # Maximisation of the movement because it has to be an integer in order to be casted in the environment grid
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
  
    # 8 cases in total
    # Case 1
    if xm > 0 and ym == 0:
      for x in range(xend, xend+xm):
        for y in ylist:
          #print(x,y)
          if self.grid[x % self.number_columns][math.floor(y) % self.number_rows].is_occupied: # if one 'pixel' is occupied then it returns False
            return False
          else:pass
      # If after the checking of all the space where the action will take place, no unit is occupied it returns True
      return True
    
    # Case 2
    elif xm < 0 and ym == 0:
      for x in range(xstart+xm, xstart):
        for y in ylist:
          #print(x,y)
          if self.grid[x % self.number_columns][math.floor(y) % self.number_rows].is_occupied: # if one 'pixel' is occupied then it returns False
            return False
          else:pass
      # If after the checking of all the space where the action will take place, no unit is occupied it returns True
      return True

    # Case 3
    elif xm == 0 and ym > 0:
      for x in xlist:
        for y in range(yend, yend+ym):
          #print(x,y)
          if self.grid[math.floor(x) % self.number_columns][y % self.number_rows].is_occupied: # if one 'pixel' is occupied then it returns False
            return False
          else:pass
      # If after the checking of all the space where the action will take place, no unit is occupied it returns True
      return True

    # Case 4
    elif xm == 0 and ym < 0:
      for x in xlist:
        for y in range(ystart+ym, ystart):
          #print(x,y)
          if self.grid[math.floor(x) % self.number_columns][y % self.number_rows].is_occupied: # if one 'pixel' is occupied then it returns False
            return False
          else:pass
      # If after the checking of all the space where the action will take place, no unit is occupied it returns True
      return True

    # Case 5
    elif xm > 0 and ym > 0:
      for x in range(xend, xend+xm):
        for y in range(ystart+ym, yend+ ym):
          #print(x,y)
          if self.grid[x % self.number_columns][y % self.number_rows].is_occupied: # if one 'pixel' is occupied then it returns False
            return False
          else:pass
      for x in range(xstart+xm, xend):
        for y in range(yend, yend+ym):
          #print(x,y)
          if self.grid[x % self.number_columns][y % self.number_rows].is_occupied: # if one 'pixel' is occupied then it returns False
            return False
          else:pass
      # If after the checking of all the space where the action will take place, no unit is occupied it returns True
      return True

    # Case 6
    elif xm > 0 and ym < 0:
      for x in range(xend, xend+xm):
        for y in range(ystart+ym, yend+ ym):
          #print(x,y)
          if self.grid[x % self.number_columns][y % self.number_rows].is_occupied: # if one 'pixel' is occupied then it returns False
            return False
          else:pass
      for x in range(xstart+xm, xend):
        for y in range(ystart+ym, ystart):
          #print(x,y)
          if self.grid[x % self.number_columns][y % self.number_rows].is_occupied: # if one 'pixel' is occupied then it returns False
            return False
          else:pass
      # If after the checking of all the space where the action will take place, no unit is occupied it returns True
      return True  

    # Case 7
    elif xm < 0 and ym > 0:
      for x in range(xstart+xm, xstart):
        for y in range(ystart+ym, yend+ym):
          #print(x,y)
          if self.grid[x % self.number_columns][y % self.number_rows].is_occupied: # if one 'pixel' is occupied then it returns False
            return False
          else:pass
      for x in range(xstart, xend+xm):
        for y in range(yend, yend+ym):
          #print(x,y)
          if self.grid[x % self.number_columns][y % self.number_rows].is_occupied: # if one 'pixel' is occupied then it returns False
            return False
          else:pass
      # If after the checking of all the space where the action will take place, no unit is occupied it returns True
      return True

      # Case 8
    else:
      for x in range(xstart+xm, xstart):
        for y in range(ystart+ym, yend+ym):
          #print(x,y)
          if self.grid[x % self.number_columns][y % self.number_rows].is_occupied: # if one 'pixel' is occupied then it returns False
            return False
          else:pass
      for x in range(xstart, xend+xm):
        for y in range(ystart+ym, ystart):
          #print(x,y)
          if self.grid[x % self.number_columns][y % self.number_rows].is_occupied: # if one 'pixel' is occupied then it returns False
            return False
          else:pass
      # If after the checking of all the space where the action will take place, no unit is occupied it returns True
      return True

  def diffusingNutrients(self)-> None:
    """Adjusts the nutrients in every environmental units according to the diffusion rates and the gradient. 
    The idea is to check if the units in the neighbourhood (upward, downward, right and leftward) contain more nutrients and simulate 
    the creation of a gradient.
    """
    nutrientEvolutionCounter = 0 # -1 when nutrient mater is out pumped from the unit, +1 otherwise
    for x in range(self.length,EnvironmentalUnit.length):
      for y in range(self.width,EnvironmentalUnit.width):
        if self.grid[(x-1)%self.number_columns][y].nutrient < self.grid[x][y].nutrient: # leftward
          nutrientEvolutionCounter -= 1
        else:
          nutrientEvolutionCounter += 1
        if self.grid[(x+1)%self.number_columns][y].nutrient < self.grid[x][y].nutrient: # rightward
          nutrientEvolutionCounter -= 1
        else:
          nutrientEvolutionCounter += 1
        if self.grid[x][(y-1)%self.number_rows].nutrient < self.grid[x][y].nutrient: # upward
          nutrientEvolutionCounter -= 1
        else:
          nutrientEvolutionCounter += 1
        if self.grid[x][(y+1)%self.number_rows].nutrient < self.grid[x][y].nutrient: # downward
          nutrientEvolutionCounter -= 1
        else:
          nutrientEvolutionCounter += 1

        # Updtading the number of nutrient in an environmental unit 
        self.grid[x][y].nutrient = self.grid[x][y].nutrient + nutrientEvolutionCounter*self.grid[x][y].nutrient*self.nutrients_diffusion

#############
# MAIN CODE #
#############
if __name__ == "__main__":
  env = Environment(100,100)
  blobby = Cell(env,25,30)
  blobbou = Cell(env,18,17)
  for i in range(15):
    print(env)
    blobby.moving(env)
    t.sleep(1)