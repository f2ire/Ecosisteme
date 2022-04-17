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
  # This number is chosen randomly between 6000 and 10000 for diversity
  max_age: int = random.randint(4000, 6000)
  # Square in the Environment grid used by the cell -> using np to fasten the computations
  occupied_x_coord: np.array = np.empty(shape=(width,length))
  occupied_y_coord: np.array = np.empty(shape=(width,length))


  def __init__(self, pos_x: int = 0, pos_y: int = 0):
    # The starting position of the cell
    self.x: int = pos_x
    self.y: int = pos_y
    
    # Initialization of the space used by the cell
    self.occupied_x_coord = np.array([x for x in range(math.floor(self.x), math.ceil(self.x + self.width))])
    self.occupied_y_coord = np.array([y for y in range(math.floor(self.y), math.ceil(self.y + self.length))])
    
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
    
    if enviro.IsSpaceForMoving(self,movement_size): # checking in the direction of the movement if the cell has space to move
      self.x = (self.x + movement_size[0]) % enviro.width
      self.y = (self.y + movement_size[1]) % enviro.length
      self.attributes = (self.x, self.y, self.length, self.width)
      self.UpdateSpace(enviro,movement_size)
    else: pass # The cell don't move if the space is occupied
    return None

  
  def UpdateSpace(self, enviro ,movement: tuple) -> None:
    """
    A cell is using a certain surface of the terrain -> width x length square
    The method updates the surface used by the cell in the environment grid by adding the movement to the occupied_x&y_coord arrays.
    Args : 
      enviro (Environment): an object of the instance Environment of environment.py 
      movement (tuple): a tuple of 2 float number giving the direction and the number of pixels a cell has to move -> (x_mvt, y_mvt)
    """
    # Updates the environmental units status, setting environmental units to occupied or inoccupied depending of the movement
    enviro.CellUsingSpace(self, movement)  
    
    self.occupied_x_coord = (self.occupied_x_coord + math.ceil(movement[0])) % enviro.width
    self.occupied_y_coord = (self.occupied_y_coord + math.ceil(movement[1])) % enviro.length
    
    return None


  def Die(self):
    self.unit_pos.cell_list.remove(self)
    return None


  def IsReplicating(self) -> bool:
    """
    Returns True if the cell replicates itself based on its growth_rate
    """
    is_replicating = random.random() <= self.growth_rate
    return is_replicating


  def Replication(self, enviro):
    """
    The cell makes a copy of itself in one direction accessible around it,
    this method returns the daughter cell.
    Args :
      enviro (Environment): an object of the instance Environment of environment.py
    """
    random_direction = Direction.get_random_direction()
    new_x = self.x + self.width * random_direction[0]
    new_y = self.y + self.length * random_direction[1]
    daughter_cell = Cell(new_x, new_y)
    daughter_cell.Moving(enviro)
    enviro.InitCellOnGrid(daughter_cell)
    return daughter_cell


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

