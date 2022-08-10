###########
# MODULES #
###########
import math
import random
import time
import numpy as np
from environment.environment_grids import *
from tools.direction import Direction
import environment.physical_data as phy

####################
# CLASS DEFINITION #
####################
class Cell:
  """Class reprensenting a cellular individual as a colored cube, capable of movement and replication.
  The cell's color is changing along with its age.
  
  Attributes:
  width (float) : size of the width of the cell in meters
  length (float): size of the length of the cell in meters
  height (float): size of the heigth of the cell in meters
  surface (float): surface of one face of the cell in m²
  volume (float) : volume of the cell in m³
  nb_unit_width (int) : total number of environment units contained in the width of the cell
  nb_unit_length (int): total number of environment units contained in the length of the cell
  x (int): coordinates along the x axis of the cell
  y (int): coordinates along the y axis of the cell
  birth_color (tuple): RGB tuple of the starting color of the cell, when the cell's age is 0
  color (tuple): actual RBG tuple of the cell's color
  death_color (tuple): RGB tuple the cell is closing by when it's aging
  display_width (int): size of the width of the cell in the pygame window in pixels 
  display_length (int) : size of the length of the cell in the pygame window in pixels 
  display_tuple (tuple): contains the information for a cell to be displayed on a pygame window, 
    in this format ; (x, y, display_width, display_length)
  speed (float): speed of the cell in meters by seconds
  replication_rate (float): probability of the cell to replicate in one iteration of the game loop
  age (int): actual age of the cell or the number of loops it has been living
  max_age (int): maximal age the cell can be
  occupied_x_coord (np.array): contains every coordinates along the x axis of the environmental units occupied by the cell  
  occupied_y_coord (np.array): contains every coordinates along the y axis of the environmental units occupied by the cell 
  """
  width: float = 1 * 10**(-6) # m
  length: float = 1 * 10**(-6) # m
  heigth: float = 1 * 10**(-6) # m
  surface: float = 6 * width * length # m²
  volume: float = width * length * heigth # m³
  
  nb_unit_width : int = round(width / EnvironmentUnit.width) # 4x4 units in a single cell
  nb_unit_length: int = round(length / EnvironmentUnit.length)

  x: int
  y: int

  birth_color: tuple = (0, 12, 255)
  color: tuple = birth_color
  death_color: tuple = (0, 0, 0)

  display_width : int  = 20 # pixels
  display_length: int = 20 # pixels
  display_tuple: tuple

  speed: float = 10**(-5) # m/s
  
  replication_rate: float = 1 / 1000
  
  age: int = 0
  max_age: int = 6000
  
  # Square in the Environment grid used by the cell -> using np to fasten the computations
  occupied_x_coord: np.array = np.empty(shape=(nb_unit_width, nb_unit_length))
  occupied_y_coord: np.array = np.empty(shape=(nb_unit_width, nb_unit_length))

  def __init__(self, environment: EnvironmentGrid, pos_x: int = 0, pos_y: int = 0):
    # The starting position of the cell
    self.x = pos_x
    self.y = pos_y
    
    # Initialization of the space used by the cell in the environment grid 
    self.occupied_x_coord = np.array([x for x in range(math.floor(self.x), math.floor(self.x) + self.nb_unit_width)])
    self.occupied_y_coord = np.array([y for y in range(math.floor(self.y), math.floor(self.y) + self.nb_unit_length)])
    environment.changeMultipleOccupationStates(self.occupied_x_coord, self.occupied_y_coord, True)

    self.display_tuple = (self.x, self.y, self.display_width, self.display_length)

  def __repr__(self) -> str:
    string = f"Cell at ({self.x}, {self.y})\n"
    string += f"Its age is : {self.age} loops"
    return 
  
  
  ###########
  # METHODS #
  ###########
  def moving(self, environment, direction: tuple = ()) -> None:
    """
    This method makes the cell move in a random direction, after checking if the environment in the direction isn't occupied by others cells
    The new coordinates are changed directly using UpdateSpace()
    Args :
      environment (Environment): an object of the instance Environment from the environment.py module
      direction (tuple): tuple containing the x and y coordinates of the movement
    """
    
    if direction == ():
      direction = Direction.getRandomDirection()
    else:pass
    #print(direction)

    environment.changeMultipleOccupationStates(self.occupied_x_coord, self.occupied_y_coord, False) # delete the space used by the cell
    x_movement = self.speed * phy.TIME_ITERATION * direction[0] # Computes the potential coordinates of the cell
    y_movement = self.speed * phy.TIME_ITERATION * direction[1]

    is_space_for_moving = environment.isSpace(self.occupied_x_coord, self.occupied_y_coord, (x_movement,y_movement))
    print("The cell is moving : ", is_space_for_moving)
    
    if is_space_for_moving:
      self.updateCoordinates(environment, (x_movement, y_movement))
    else : pass
    environment.changeMultipleOccupationStates(self.occupied_x_coord, self.occupied_y_coord, True)
    return None


  def replicating(self, environment: EnvironmentGrid, cells_list: list) -> None:
    """
    Add a new cell to cells_list if their is enough space to create it. 
    Args :
      environment (EnvironmentGrid): an object of the instance Environment from the environment.py module
      cells_list (list): the list of all the cells of our environment
    """
    if self.isReplicationPossible():
      random_direction = Direction.getRandomReplicationDirection()
      #print("rdm dir :",random_direction)
      needed_replication_space = (self.width*random_direction[0], self.length*random_direction[1])
      is_space_for_replication = environment.isSpace(self.occupied_x_coord, self.occupied_y_coord, needed_replication_space)
      #print("is_space :",is_space)
      if is_space_for_replication:
        daughter_cell = Cell(environment, self.x + self.width*random_direction[0], self.y + self.length*random_direction[1])
        # initialise the space occupied by the daughter cell on the environment grid
        environment.changeMultipleOccupationStates(daughter_cell.occupied_x_coord, daughter_cell.occupied_y_coord, True) 
        cells_list.append(daughter_cell)
      else : pass
    else : pass
    return None


  def isTooOld(self) -> bool:
    """
    Returns True if the cell's age is superior to its max_age
    """
    if self.age > self.max_age:
      return True
    else:
      return False


  def isReplicationPossible(self) -> bool:
    """Takes a random number between 0 and 1 and checks if it is lower than the replication rate of the cell

    Returns:
      bool: True if the cell is randomly capable of replicating itself
    """
    return random.random() <= self.replication_rate


  def updateCoordinates(self, environment: EnvironmentGrid, movement: tuple) -> None:
    """Adds the coordinates inside the movement tuple to the actual coordinates of the cell.
    Updates the display_tuple attribute and the occupied lists.

    Args:
      environment (Environment): an object of the instance Environment from the environment.py module
      movement (tuple): _description_
    """
    print(f"Tuple's movement : {movement}")
    self.x = (self.x + movement[0]) % environment.column_number
    self.y = (self.y + movement[1]) % environment.row_number
    
    # Updating coordinates on the environmental grid.
    self.occupied_x_coord = self.occupied_x_coord + movement[0]
    self.occupied_y_coord = self.occupied_y_coord + movement[1]
    
    self.display_tuple = (self.x, self.y, self.length, self.width)


  def adaptColor(self) -> None:
    """
    Linear interpolation to determine the cell's color depending of its age
    """
    alpha = self.age / self.max_age
    self.color = (
      (1 - alpha) * self.birth_color[0] + alpha * self.death_color[0],
      (1 - alpha) * self.birth_color[1] + alpha * self.death_color[1],
      (1 - alpha) * self.birth_color[2] + alpha * self.death_color[2],
    )
    return None
    

#############
# MAIN CODE #
#############
if __name__ == "__main__":
  enviro = EnvironmentGrid(2.5*10**(-6), 2.5*10**(-6))
  cell1 = Cell(enviro)
  print(enviro) # OK

  for i in range(10):
    cell1.moving(enviro)
    print(enviro)
    time.sleep(1)