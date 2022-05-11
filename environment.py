###########
# MODULES #
###########
from itertools import starmap
import math
from matplotlib.axis import XAxis
import numpy as np
from cell import Cell
from environment_unit import EnvironmentalUnit

####################
# CLASS DEFINITION #
####################
class Environment:
  """
  Class stocking multiple environment_unit
  
  """
  def __init__(self, length: int, width: int) -> None:
    """Initialize an environment with a length * width size
    Args:
      length (int): length of the environment (length of window in pixel)
      width (int): width of the environment (width of window in pixel)
    """
    self.length: int = length
    self.width: int = width
    self.number_columns: int = round(self.width / EnvironmentalUnit.width)
    self.number_rows: int = round(self.length / EnvironmentalUnit.length)
    
    # Create a grid with an EnvironmentalUnit object in each columns and that for each rows
    self.grid: list = [
      [EnvironmentalUnit(x * EnvironmentalUnit.width, y * EnvironmentalUnit.length,)
      for x in range(self.number_columns)]
      for y in range(self.number_rows)
    ]
    return None
  
  def __str__(self) -> str:
    index = 0
    string = f"Evironment dimension ({self.width},{self.length}) \n"
    # Representing the environment grid with 1 when the 'pixel' is occupied and 0 when it is not.
    string += f" {[x for x in range(self.number_columns)]} \n"
    for row in self.grid:
      string += "["
      for unit in row:
        if unit.is_occupied:
          string += "1 "
        else :
          string += "0 "
      string += f"]{str(index)}\n"
      index += 1
    
    return string
      
  ###########
  # METHODS #
  ########### 
  def UsedSpace(self, x_list: np.array, y_list: np.array, delete: bool = False) -> None:
    """ Sets all the coordinates of the environment grid occupied by the cell on 'occupied' or 'not occupied' depending on the value of delete.
    
    Args:
      delete (bool): if set to True then the is_occupied parameter is set to False
      x_list (np.array): array containing every coordinates on the environment grid of an entity along the x axis 
      y_list (np.array): array containing every coordinates on the environment grid of an entity along the y axis 
    """
    for x in x_list:
      for y in y_list:
        if(not delete):
          self.grid[x % self.number_columns][y % self.number_rows].is_occupied = True
        else :
          self.grid[x % self.number_columns][y % self.number_rows].is_occupied = False
    
    return None
  

  def IsSpace(self, x_list: np.array, y_list: np.array, direction: tuple) -> bool:
    """ Checks if the environment units in a certain direction are available for the entity to move or replicate

    Args:
      x_list (np.array): array containing every coordinates on the environment grid of an entity along the x axis 
      y_list (np.array): array containing every coordinates on the environment grid of an entity along the y axis 
      direction (tuple): tuple of the maximum (absolute value) coordinates where the action will took place. For a cell entity, 
                         it should either be the values of the movement or the place where the daughter cell gonna appear

    Returns:
      bool: True if the space is available for the action, False if not
    """
    # Maximisation of the movement because it has to be an integer in order to be casted in the environment grid
    if direction[0] > 0:
      xm = math.ceil(direction[0])
    else:
      xm = math.floor(direction[0])
    if direction[1] > 0:
      ym = math.ceil(direction[1])
    else:
      ym = math.floor(direction[1])

    xstart, ystart, xend, yend = x_list[0], y_list[0], x_list[-1], y_list[-1]
    # Increments for the for loops because we need only to go from an unit to another
    x_i, y_i = EnvironmentalUnit.width, EnvironmentalUnit.length 
  
    # 8 cases in total 
    # Case 1
    if xm > 0 and ym == 0:
      for x in range(xend, xend+xm, x_i):
        for y in y_list:
          if self.grid[x % self.number_columns][y % self.number_rows].is_occupied: # if one 'pixel' is occupied then it returns False
            return False
          else:pass
      # If after the checking of all the space where the action will take place, no unit is occupied it returns True
      return True
    
    # Case 2
    elif xm < 0 and ym == 0:
      for x in range(xstart+xm, xstart, x_i):
        for y in y_list:
          if self.grid[x % self.number_columns][y % self.number_rows].is_occupied: # if one 'pixel' is occupied then it returns False
            return False
          else:pass
      # If after the checking of all the space where the action will take place, no unit is occupied it returns True
      return True

    # Case 3
    elif xm == 0 and ym > 0:
      for x in x_list:
        for y in range(yend, yend+ym, y_i):
          if self.grid[x % self.number_columns][y % self.number_rows].is_occupied: # if one 'pixel' is occupied then it returns False
            return False
          else:pass
      # If after the checking of all the space where the action will take place, no unit is occupied it returns True
      return True

    # Case 4
    elif xm == 0 and ym < 0:
      for x in x_list:
        for y in range(ystart+ym, ystart, y_i):
          if self.grid[x % self.number_columns][y % self.number_rows].is_occupied: # if one 'pixel' is occupied then it returns False
            return False
          else:pass
      # If after the checking of all the space where the action will take place, no unit is occupied it returns True
      return True

    # Case 5
    elif xm > 0 and ym > 0:
      for x in range(xend, xend+xm, x_i):
        for y in range(ystart+ym, yend+ ym, y_i):
          if self.grid[x % self.number_columns][y % self.number_rows].is_occupied: # if one 'pixel' is occupied then it returns False
            return False
          else:pass
      for x in range(xstart+xm, xend, x_i):
        for y in range(yend, yend+ym, y_i):
          if self.grid[x % self.number_columns][y % self.number_rows].is_occupied: # if one 'pixel' is occupied then it returns False
            return False
          else:pass
      # If after the checking of all the space where the action will take place, no unit is occupied it returns True
      return True

    # Case 6
    elif xm > 0 and ym < 0:
      for x in range(xend, xend+xm, x_i):
        for y in range(ystart+ym, yend+ ym, y_i):
          if self.grid[x % self.number_columns][y % self.number_rows].is_occupied: # if one 'pixel' is occupied then it returns False
            return False
          else:pass
      for x in range(xstart+xm, xend, x_i):
        for y in range(ystart+ym, ystart, y_i):
          if self.grid[x % self.number_columns][y % self.number_rows].is_occupied: # if one 'pixel' is occupied then it returns False
            return False
          else:pass
      # If after the checking of all the space where the action will take place, no unit is occupied it returns True
      return True  

    # Case 7
    elif xm < 0 and ym > 0:
      for x in range(xstart+xm, xstart, x_i):
        for y in range(ystart+ym, yend+ym, y_i):
          if self.grid[x % self.number_columns][y % self.number_rows].is_occupied: # if one 'pixel' is occupied then it returns False
            return False
          else:pass
      for x in range(xstart, xend+xm, x_i):
        for y in range(yend, yend+ym, y_i):
          if self.grid[x % self.number_columns][y % self.number_rows].is_occupied: # if one 'pixel' is occupied then it returns False
            return False
          else:pass
      # If after the checking of all the space where the action will take place, no unit is occupied it returns True
      return True

      # Case 8
    else:
      for x in range(xstart+xm, xstart, x_i):
        for y in range(ystart+ym, yend+ym, y_i):
          if self.grid[x % self.number_columns][y % self.number_rows]: # if one 'pixel' is occupied then it returns False
            return False
          else:pass
      for x in range(xstart, xend+xm, x_i):
        for y in range(ystart+ym, ystart, y_i):
          if self.grid[x % self.number_columns][y % self.number_rows] % self.number_columns.is_occupied: # if one 'pixel' is occupied then it returns False
            return False
          else:pass
      # If after the checking of all the space where the action will take place, no unit is occupied it returns True
      return True


  def SpaceMvt(self, x_list: np.array, y_list: np.array, movement: tuple) -> None:
    """ Removes an entity from it's actual location in the environment grid and adds it next location in the environment grid.

    Args:
      x_list (np.array): array containing every coordinates on the environment grid of an entity along the x axis 
      y_list (np.array): array containing every coordinates on the environment grid of an entity along the y axis 
      movement (tuple): tuple of movement 'length' along x and y axes such as (xm,ym)
    """
    # Maximisation of the movement because it has to be an integer in order to be casted in the environment grid
    if movement[0] > 0:
      xm = math.ceil(movement[0])
    else:
      xm = math.floor(movement[0])
    if movement[1] > 0:
      ym = math.ceil(movement[1])
    else:
      ym = math.floor(movement[1])

    xstart, ystart, xend, yend = x_list[0], y_list[0], x_list[-1], y_list[-1]
    # Increments for the for loops because we need only to go from an unit to another
    x_i, y_i = EnvironmentalUnit.width, EnvironmentalUnit.length 

    # 8 cases in total
    # Case 1
    if xm > 0 and ym == 0:
      # Loop to 'remove' the entity of the environment grid after the movement
      for x in range(xstart, xstart+xm, x_i):
        for y in y_list:
          self.grid[x % self.number_columns][y % self.number_rows].is_occupied = False
      # Loop to 'add' the entity of the environment grid after the movement
      for x in range(xend, xend+xm, x_i):
        for y in y_list:
          self.grid[x % self.number_columns][y % self.number_rows].is_occupied = True
    
    # Case 2 
    elif xm < 0 and ym == 0:
      # Loop to 'remove' the entity of the environment grid after the movement
      for x in range(xend+xm, xend, x_i):
        for y in y_list:
          self.grid[x % self.number_columns][y % self.number_rows].is_occupied = False
      # Loop to 'add' the entity of the environment grid after the movement
      for x in range(xstart+xm, xstart, x_i):
        for y in y_list:
          self.grid[x % self.number_columns][y % self.number_rows].is_occupied = True
    
    # Case 3
    elif xm == 0 and ym > 0:
      # Loop to 'remove' the entity of the environment grid after the movement
      for x in x_list:
        for y in range(ystart, ystart+ym, y_i):
          self.grid[x % self.number_columns][y % self.number_rows].is_occupied = False
      # Loop to 'add' the entity of the environment grid after the movement
      for x in x_list:
        for y in range(yend, yend+ym, y_i):
          self.grid[x % self.number_columns][y % self.number_rows].is_occupied = True

    # Case 4
    elif xm == 0 and ym < 0:
      # Loop to 'remove' the entity of the environment grid after the movement
      for x in x_list:
        for y in range(yend+ym, yend, y_i):
          self.grid[x % self.number_columns][y % self.number_rows].is_occupied = False
      # Loop to 'add' the entity of the environment grid after the movement
      for x in x_list:
        for y in range(ystart+ym, ystart, y_i):
          self.grid[x % self.number_columns][y % self.number_rows].is_occupied = True

    # Case 5
    elif xm > 0 and ym > 0:
      # Loops to 'remove' the entity of the environment grid after the movement
      for x in range(xstart, xend, x_i):
        for y in range(ystart, ystart+ym, y_i):
          self.grid[x % self.number_columns][y % self.number_rows].is_occupied = False
      for x in range(xstart, xstart+xm, x_i):
        for y in range(ystart+ym, yend, y_i):
          self.grid[x % self.number_columns][y % self.number_rows].is_occupied = False
      # Loops to 'add' the entity of the environment grid after the movement
      for x in range(xend, xend+xm, x_i):
        for y in range(ystart+ym, yend+ym, y_i):
          self.grid[x % self.number_columns][y % self.number_rows].is_occupied = True
      for x in range(xstart+xm, xend, x_i):
        for y in range(yend, yend+ym, y_i):
          self.grid[x % self.number_columns][y % self.number_rows].is_occupied = True
    
    # Case 6
    elif xm > 0 and ym < 0:
      # Loops to 'remove' the entity of the environment grid after the movement
      for x in range(xstart, xstart+xm, x_i):
        for y in range(ystart, yend, y_i):
          self.grid[x % self.number_columns][y % self.number_rows].is_occupied = False
      for x in range(xstart+xm, xend, x_i):
        for y in range(ystart+ym, ystart, y_i):
          self.grid[x % self.number_columns][y % self.number_rows].is_occupied = False
      # Loops to 'add' the entity of the environment grid after the movement
      for x in range(xstart+xm, xend+xm, x_i):
        for y in range(ystart+ym, ystart, y_i):
          self.grid[x % self.number_columns][y % self.number_rows].is_occupied = True
      for x in range(xend, xend+xm, x_i):
        for y in range(ystart, yend+ym, y_i):
          self.grid[x % self.number_columns][y % self.number_rows].is_occupied = True

    # Case 7
    elif xm < 0 and ym > 0:
      # Loops to 'remove' the entity of the environment grid after the movement
      for x in range(xstart, xend, x_i):
        for y in range(ystart, ystart+ym, y_i):
          self.grid[x % self.number_columns][y % self.number_rows].is_occupied = False
      for x in range(xend+xm, xend, x_i):
        for y in range(ystart+ym, yend, y_i):
          self.grid[x % self.number_columns][y % self.number_rows].is_occupied = False
      # Loops to 'add' the entity of the environment grid after the movement
      for x in range(xstart+xm, xstart, x_i):
        for y in range(ystart+ym, yend+ym, y_i):
          self.grid[x % self.number_columns][y % self.number_rows].is_occupied = True
      for x in range(xstart, xend+xm, x_i):
        for y in range(yend, yend+ym, y_i):
          self.grid[x % self.number_columns][y % self.number_rows].is_occupied = True
    
    # Case 8
    elif xm < 0 and ym < 0:
      # Loops to 'remove' the entity of the environment grid after the movement
      for x in range(xstart, xend, x_i):
        for y in range(yend+ym, yend, y_i):
          self.grid[x % self.number_columns][y % self.number_rows].is_occupied = False
      for x in range(xend+xm, xend, x_i):
        for y in range(ystart, yend+ym, y_i):
          self.grid[x % self.number_columns][y % self.number_rows].is_occupied = False
      # Loops to 'add' the entity of the environment grid after the movement
      for x in range(xstart+xm, xend+xm, x_i):
        for y in range(ystart+ym, ystart, y_i):
          self.grid[x % self.number_columns][y % self.number_rows].is_occupied = True
      for x in range(xstart+x, xstart, x_i):
        for y in range(ystart, yend+ym, y_i):
          self.grid[x % self.number_columns][y % self.number_rows].is_occupied = True.is_occupied


#############
# MAIN CODE #
#############
if __name__ == "__main__":
  env = Environment(100,100)
  print(len(env.grid))
  blobby = Cell(40,40)
  print(blobby.occupied_x_coord)
  for i in range(100):
    print(blobby)
    blobby.Moving(enviro=env)
  print(env)

