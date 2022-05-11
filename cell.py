###########
# MODULES #
###########
import math
import random
import numpy as np
from tools.direction import Direction
from environment_unit import EnvironmentalUnit

####################
# CLASS DEFINITION #
####################
class Cell:
  """
  Cell object is the fondamental unit of life
  Cells should be capable of moving towards energy&food sources
  and replicate itself. It has some basic attributs
  A cell is represented as a small square in the environment
  localized by his coordonates
  """
  # Visual caracteristic
  width, length = (10,10)
  birth_color: tuple = (255, 102, 0)
  death_color: tuple = (0, 12, 255)
  # Cell parameter
  mvmt_speed: float = 1
  # The number of times the cell replicates itself in one iteration of the game loop
  growth_rate: float = 1 / 3500
  
  max_age: int = 6000 
  # Square in the Environment grid used by the cell -> using np to fasten the computations
  occupied_x_coord: np.array = np.empty(shape=(width,length))
  occupied_y_coord: np.array = np.empty(shape=(width,length))


  def __init__(self, pos_x: int = 0, pos_y: int = 0):
    # The starting position of the cell
    self.x: int = pos_x
    self.y: int = pos_y
    
    # Initialization of the space used by the cell in the environment grid 
    self.occupied_x_coord = np.array([x for x in range(math.floor(self.x), math.ceil(self.x + self.width), EnvironmentalUnit.width)])
    self.occupied_y_coord = np.array([y for y in range(math.floor(self.y), math.ceil(self.y + self.length), EnvironmentalUnit.length)])
    
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
  def Moving(self, enviro) -> None:
    """
    This method makes the cell move in a random direction, after checking if the environment in the direction isn't occupied by others cells
    The new coordinates are changed directly using UpdateSpace()
    Args :
      enviro (Environment): an object of the instance Environment of environment.py 
    """
    # Computes the potential coordonates of the cell
    random_direction = Direction.get_random_direction()
    movement_size: tuple = ((self.mvmt_speed * random_direction[0]), (self.mvmt_speed * random_direction[1]))
    # Length of the movement is doubled to prevent cells from superposing if they both go in the same direction
    predict_mvt = (2*movement_size[0], 2*movement_size[1])
    print(enviro.IsSpace(self.occupied_x_coord, self.occupied_y_coord, predict_mvt))
    if enviro.IsSpace(self.occupied_x_coord, self.occupied_y_coord, predict_mvt): # checking in the direction of the movement if the cell has space to move
      enviro.SpaceMvt(self.occupied_x_coord, self.occupied_y_coord, movement_size) # updating occupied space by the cell on the grid
      self.x = (self.x + movement_size[0]) % enviro.width
      self.y = (self.y + movement_size[1]) % enviro.length
      # Updating the lists storing the coordinates of the cell on the environment gridd
      self.occupied_x_coord = (self.occupied_x_coord + math.ceil(movement_size[0])) % enviro.width
      self.occupied_y_coord = (self.occupied_y_coord + math.ceil(movement_size[1])) % enviro.length
      self.attributes = (self.x, self.y, self.length, self.width)
    else: pass # The cell don't move if the space is occupied
    return None


  def Replicating(self, enviro, cells_list: list) -> None:
    """
    Add a new cell to cells_list if their is enough space to create it. 
    Args :
      enviro (Environment): an object of the instance Environment of environment.py
      cells_list (list): the list of all the cells of our environment
    """
    is_replicating = random.random() <= self.growth_rate # boolean checking if the cell will replicate itself based on it division probability 
    if is_replicating:
      random_direction = Direction.GetRandomReplicationDirection()
      replication_range = (self.width*random_direction[0], self.length*random_direction[1])
      if enviro.IsSpace(self.occupied_x_coord, self.occupied_y_coord, replication_range):
        daughter_cell = Cell(self.x + self.width * random_direction[0], self.y + self.length * random_direction[1])
        enviro.UsedSpace(daughter_cell.occupied_x_coord, daughter_cell.occupied_y_coord) # initialise the space occupied by the daughter cell on the environment grid
        cells_list.append(daughter_cell)
      else : pass
    else : pass
    return None


  def IsTooOld(self) -> bool:
    """
    Returns True if the cell's age is superior to its max_age
    """
    if self.age > self.max_age:
      return True
    else:
      return False


  def AdaptColor(self) -> None:
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
  blob = Cell(30,78)
  print("x coordonates : ",blob.occupied_x_coord, "\n y coordonates : ", blob.occupied_y_coord)
  movement = (5,5)
  blob.UpdateSpace(movement)
  print("x coordonates : ",blob.occupied_x_coord, "\n y coordonates : ", blob.occupied_y_coord)

