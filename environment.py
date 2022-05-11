###########
# MODULES #
###########
import math
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
    self.number_rows: int = round(self.length / EnvironmentalUnit.length
    )
    # Create a grid with an EnvironmentalUnit object in each columns 
    #              pass                           and that for each rows
    self.grid: list = [
      [EnvironmentalUnit(x * EnvironmentalUnit.width, y * EnvironmentalUnit.length,)
      for x in range(self.number_columns)]
      for y in range(self.number_rows)
    ]
    return None
  
  def __str__(self) -> str:
    string = f"Evironment dimension ({self.width}{self.length}) \n"
    for row in self.grid:
      for unit in row:
        string += f"{str(unit)}\n"
    
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
          self.grid[x][y].is_occupied = True
        else :
          self.grid[x][y].is_occupied = False
    
    return None
    

  def IsSpaceForMoving(self, cell: Cell, movement : tuple) -> bool:
    """
    This method checks if the movement of the cell is possible and returns True if the environment unit in the direction of the movement 
    aren't occupied. 
    It browses all the the space that will be occupied by the cell (after it movement) and check if environment units aren't occupied.
    Args :
        cell (Cell): cell object
        movement (tuple): a tuple of 2 float number giving the direction and the number of pixels a cell has to move -> (2*x_mvt, 2*y_mvt)
    """
    x_mvt, y_mvt = movement[0], movement[1]

    # to make the code more human readable
    x_start = math.ceil((cell.x + 2*x_mvt ) / EnvironmentalUnit.width) % self.width
    y_start = math.ceil((cell.y + 2*y_mvt) / EnvironmentalUnit.length) % self.length
    x_end = math.floor((cell.x + cell.width + 2*x_mvt ) / EnvironmentalUnit.width) % self.width  
    y_end = math.floor((cell.y + cell.length + 2*y_mvt ) / EnvironmentalUnit.length) % self.length

    # Loop parsing every environmental units' coordinates and checking wether they are occupied or not
    for x_coo in range(x_start, x_end, EnvironmentalUnit.width):
      for y_coo in range(y_start, y_end, EnvironmentalUnit.length):
        # If x_coo and y_coo aren't in the previous space of the cell, it looks if there is space in the environmental_unit of coor (x_coo,y_coo)
        if not (x_coo in cell.occupied_x_coord and y_coo in cell.occupied_y_coord):
          if self.grid[x_coo][y_coo].is_occupied:
            return False       
          else:pass

    return True

  
  def IsSpaceForReplication(self, direction: tuple, cell: Cell):
    """
    This method checks if their is space available for the replication of a cell.
    Their must be a space of width x length available in the specified direction so the replication can be performed
    Args :
      cell (Cell): cell object
      direction (tuple): contains 2 coordinates telling in which direction the replication is supposed to happen.
    """
    x_dir, y_dir = direction[0], direction[1]
    x_start = math.ceil(cell.x + cell.width * x_dir)
    y_start = math.ceil(cell.y + cell.length * y_dir)
    x_end = math.floor(cell.x + 2 * cell.width * x_dir)
    y_end = math.floor(cell.y + 2 * cell.length * y_dir)

    for x in range(x_start, x_end, EnvironmentalUnit.width):
      for y in range(y_start, y_end, EnvironmentalUnit.length):
        if self.grid[x][y].is_occupied:
          return False
    return True


#############
# MAIN CODE #
#############
if __name__ == "__main__":
  env = Environment(100,100)
  print(len(env.grid))
  blobby = Cell(47,47)
  blobou = Cell(35,35)
  print("x:",blobou.occupied_x_coord,", y:",blobou.occupied_y_coord)
  env.InitCellOnGrid(blobby)
  env.InitCellOnGrid(blobou)
  for i in range(100):
    print(blobby)
    blobby.Moving(enviro=env)

