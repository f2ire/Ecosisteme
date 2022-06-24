###########
# MODULES #
###########
import math
import random
import numpy as np
from tools.direction import Direction

####################
# CLASS DEFINITION #
####################
class Cell:
  """
  Cell object is the fondamental unit of life
  Cells should be capable of moving towards energy&food sources
  and replicate itself. It has some basic attributes
  A cell is represented by a small square in the environment
  localized by its (x,y) coordinates
  """
  # Visual caracteristic
  width, length = (10,10)
  birth_color: tuple = (0, 12, 255)
  death_color: tuple = (0, 0, 0)
  # Cell parameter
  mvmt_speed: float = 1
  # The number of times the cell replicates itself in one iteration of the game loop
  replication_rate: float = 1 / 1000
  
  max_age: int = 6000 # number of time of the game loop the cell is going to survive

  x,y = (0,0) 
  
  # Square in the Environment grid used by the cell -> using np to fasten the computations
  occupied_x_coord: np.array = np.empty(shape=(width,length))
  occupied_y_coord: np.array = np.empty(shape=(width,length))


  def __init__(self, environment, pos_x: int = 0, pos_y: int = 0):
    # The starting position of the cell
    self.x: int = pos_x
    self.y: int = pos_y
    
    # Initialization of the space used by the cell in the environment grid 
    self.occupied_x_coord = np.array([x for x in range(math.floor(self.x), math.floor(self.x) + self.width)])#, EnvironmentalUnit.width)])
    self.occupied_y_coord = np.array([y for y in range(math.floor(self.y), math.floor(self.y) + self.length)])#, EnvironmentalUnit.length)])
    environment.usedSpace(self, self.occupied_x_coord, self.occupied_y_coord)

    # Attributes is in this rectangle tuple format to fit to the pygame.fill() method which fills rectangle objects
    self.attributes = (self.x, self.y, self.width, self.length)
    # When a cell is created, it age is set on 0. The cell is aging over time and it color is changing with it age
    self.age = 0
    self.color = Cell.birth_color


  def __repr__(self) -> str:
    return f"Cell at ({self.x}, {self.y})"
  
  
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

    environment.usedSpace(self, self.occupied_x_coord, self.occupied_y_coord, True) # delete the space used by the cell
    x_movment, y_movement = self.mvmt_speed * direction[0], self.mvmt_speed * direction[1] # Computes the potential coordinates of the cell

    is_space_for_moving = environment.isSpace(self.occupied_x_coord, self.occupied_y_coord, (x_movment,y_movement))
    #print(enviro.IsSpace(self.occupied_x_coord, self.occupied_y_coord, (xm,ym)))
    if is_space_for_moving:
      self.updateCoordinates(environment, (x_movment,y_movement))
    else : pass
    environment.usedSpace(self, self.occupied_x_coord, self.occupied_y_coord)
    return None


  def replicating(self, environment, cells_list: list) -> None:
    """
    Add a new cell to cells_list if their is enough space to create it. 
    Args :
      environment (Environment): an object of the instance Environment from the environment.py module
      cells_list (list): the list of all the cells of our environment
    """
    if self.isReplicationPossible():
      random_direction = Direction.getRandomReplicationDirection()
      #print("rdm dir :",random_direction)
      needed_replication_space = (self.width*random_direction[0], self.length*random_direction[1])
      is_space_for_replication = environment.isSpace(self.occupied_x_coord, self.occupied_y_coord, needed_replication_space)
      #print("is_space :",is_space)
      if is_space_for_replication:
        daughter_cell = Cell(environment,self.x + self.width * random_direction[0], self.y + self.length * random_direction[1])
        environment.usedSpace(daughter_cell, daughter_cell.occupied_x_coord, daughter_cell.occupied_y_coord) # initialise the space occupied by the daughter cell on the environment grid
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

  def isReplicationPossible(self) -> bool:
    """Takes a random number between 0 and 1 and checks if it is lower than the replication rate of the cell

    Returns:
      bool: True if the cell is randomly capable of replicating itself
    """
    return random.random() <= self.replication_rate


  def updateCoordinates(self,environment ,movement: tuple) -> None:
    """

    Args:
        environment (Environment): an object of the instance Environment from the environment.py module
        movement (tuple): _description_
    """
    self.x = (self.x + movement[0]) % environment.width
    self.y = (self.y + movement[1]) % environment.length
    
    # Updating coordinates on the environmental grid.
    self.occupied_x_coord = self.occupied_x_coord + movement[0]
    self.occupied_y_coord = self.occupied_y_coord + movement[1]
    
    self.attributes = (self.x, self.y, self.length, self.width)


#############
# MAIN CODE #
#############
if __name__ == "__main__":
  blob = Cell(30,78)
  print("x coordonates : ",blob.occupied_x_coord, "\n y coordonates : ", blob.occupied_y_coord)
  movement = (5,5)
  blob.UpdateSpace(movement)
  print("x coordonates : ",blob.occupied_x_coord, "\n y coordonates : ", blob.occupied_y_coord)