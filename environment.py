###########
# MODULES #
###########
import math
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
  def InitCellOnGrid(self, cell: Cell) -> None:
    """
    Method only used to initiates the cell on the environment grid -
    > sets all the environment units sharing the same coordinates as the cell to occupied
    """
    for x in range(math.ceil(cell.occupied_x_coord[0] / EnvironmentalUnit.width), math.floor(cell.occupied_x_coord[-1] / EnvironmentalUnit.width), EnvironmentalUnit.width):
      for y in range(math.ceil(cell.occupied_y_coord[0] / EnvironmentalUnit.length), math.floor(cell.occupied_y_coord[-1] / EnvironmentalUnit.length), EnvironmentalUnit.length):
        (self.grid[x][y]).is_occupied = True
    
    return None


  def SuppressCell(self, cell: Cell):
    """
    Sets all the environmental units of a cell to "not occupied"
    Args:
        cell (Cell): cell object
    """
    for x in range(math.ceil(cell.occupied_x_coord[0] / EnvironmentalUnit.width), math.floor(cell.occupied_x_coord[-1] / EnvironmentalUnit.width), EnvironmentalUnit.width):
      for y in range(math.ceil(cell.occupied_y_coord[0] / EnvironmentalUnit.length), math.floor(cell.occupied_y_coord[-1] / EnvironmentalUnit.length), EnvironmentalUnit.length):
        (self.grid[x][y]).is_occupied = False


  def CellUsingSpace(self, cell: Cell, movement: tuple) -> None:
    """
    This method sets the newly used environmental units on 'occupied' and the no longer used environmental units are set up on 'not occupied'
    according to the movement of the cell
    go through all the coordinates stored in cell.occupied_x_coordinates (same for y) with an increment depending of the size of 
    an environment_unit and sets all environment_units to 'occupied'. 
    Args:
        cell (Cell): cell object
        movement (tuple): a tuple of 2 float number giving the direction and the number of pixels a cell has to move -> (2*x_mvt, 2*y_mvt)
    """
    x_mvt, y_mvt = movement[0], movement[1]

    self.SuppressCell(cell)
   
    # Make the code more readable
    x_start = math.ceil((cell.x + 2*x_mvt ) / EnvironmentalUnit.width) % self.width
    y_start = math.ceil((cell.x + cell.width + 2*x_mvt ) / EnvironmentalUnit.width) % self.length
    x_end = math.floor((cell.y + 2*y_mvt) / EnvironmentalUnit.length) % self.width
    y_end = math.floor((cell.y + cell.length + 2*y_mvt ) / EnvironmentalUnit.length) % self.length

    # Second loop setting all the new coordinates of the cell to occupied
    for x in range(x_start, x_end, EnvironmentalUnit.width):
      for y in range(y_start,y_end, EnvironmentalUnit.length):
        (self.grid[x][y]).is_occupied = True

    return None
    """" Ideas for complexity optimisation
    # starting_xT is the starting x coordinates from which to set is_occupied to True. Same for starting_yT.
    starting_xT, starting_yT = min(cell.x + cell.width, cell.x + cell.width + x_mov), min(cell.y, cell.y + y_mov)
    # ending_xT is the ending x coordinates to which set is_occupied to True.
    ending_xT, ending_yT = max(cell.x + cell.width, cell.x + cell.width + x_mov), max(cell.y, cell.y + y_mov)
    
    # Same here
    starting_xF, starting_yF = min(cell.x, cell.x + x_mov), min(cell.y + cell.length, cell.y + cell.length + y_mov)      
    ending_xF, ending_yF = max(cell.x, cell.x + x_mov), max(cell.y + cell.length, cell.y + cell.length + y_mov)
    # Boolean telling if we have to set the unit to True or False depending of the direction of the movement
    dir_bool = 
    # Loop setting the units back to inoccupied
    for x in range(starting_xF, ending_xF, EnvironmentalUnit.width):
        for y in range(starting_yF, ending_yF, EnvironmentalUnit.length):
            (self.grid[x][y]).is_occupied = 
    # Loop setting the newly occupied units's is_occupied to True
    for x in range(starting_xT, ending_xT, EnvironmentalUnit.width):
        for y in range(starting_yT, ending_yT, EnvironmentalUnit.length):
            (self.grid[x][y]).is_occupied = True
    """


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

