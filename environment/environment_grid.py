###########
# MODULES #
###########
from environment_unit import EnvironmentalUnit
import math

####################
# CLASS DEFINITION #
####################
class EnvironmentGrid:

  colum_number: int
  row_number: int

  environmental_units_list: list

  def __init__(self, col_nb: int, row_nb: int, init_temperature: float) -> None:
    self.colum_number, self.row_number = col_nb, row_nb

    self.environmental_units_list = [
      [EnvironmentalUnit(x * EnvironmentalUnit.width, y * EnvironmentalUnit.length, init_temperature)
      for x in range(self.colum_number)]
      for y in range(self.row_number)
    ]
    return None


  def __str__(self) -> str:
    index = 0
    string = f"Grid dimensions : ({self.colum_number},{self.row_number}) \n"
    # Representing the environment grid with an X when the environmental unit is occupied and with . when it is not.
    string += "["
    for n in range(0,self.colum_number-1):
      string += f"{n},"
    string += f"{self.colum_number-1}]\n"
    for row in self.environmental_units_list:
      string += "["
      for unit in row:
        if unit.is_occupied:
          string += "X "
        else :
          string += ". "
      string += f"]{str(index)}\n"
      index += 1
    
    return string

  
  def getEnvironmentalUnit(self, position_x: int, position_y: int) -> EnvironmentalUnit:
    return self.environmental_units_list[position_x][position_y]

  def areAllUnitsNotOccupied(self, starting_x: int, ending_x: int, starting_y: int, ending_y: int) -> bool:
    """Navigates through all the environmental units of the environment grid between the starting x and y coordinates and the ending x and y. 
    For each environmental unit encountered, it checks its is_occupied attribute. If one is set on True, then the function returns False.
    The function returns True if and only if every environmental units have their is_occupied attribute sets on False.

    Args:
      starting_x (int): x coordinates of the environment grid where to begin the navigation 
      ending_x (int): x coordinates of the environment grid where to end the navigation
      starting_y (int): y coordinates of the environment grid where to begin the navigation 
      ending_y (int): y coordinates of the environment grid where to end the navigation

    Returns:
      bool: True if every environmental units have their is_occupied attribute set on False, False otherwise.
    """
    for x in range(starting_x, ending_x):
      for y in range(starting_y, ending_y):
        if self.getEnvironmentalUnit(x % self.colum_number, y % self.row_number).is_occupied:
          return False
        else:pass
    return True

  def changeMultipleOccupationStates(self, xlist, ylist, occupation_state: bool) -> None:
    """ Sets the environmental units concerned by the x and y lists to the value of occupation_state.
    Coordinates are converted to integers. 
    Coordinates are congruents to the number of columns and rows because the environment is a topological 2-Sphere.
    
    Args:
      xlist (np.array): numpy array containing the x coordinates of the environmental units to be affected by the change of occupation state 
      ylist (np.array): numpy array containing the y coordinates of the environmental units to be affected by the change of occupation state 
      occupation_state (bool): the final value of the is_occupied attribute of the concerned environmental units
    """
    for x in xlist:
      for y in ylist:
        self.getEnvironmentalUnit(math.floor(x) % self.colum_number, math.floor(y) % self.row_number).is_occupied = occupation_state
    return None

  def isSpace(self, xlist, ylist, max_action_range: tuple) -> bool:
    """ Checks if the environment units in a certain max_action_range are available for the entity to move or replicate.

    Args:
      xlist (np.array): numpy array containing the x coordinates of the environmental units that are already occupied by an entity (cell ...) 
      ylist (np.array): numpy array containing the y coordinates of the environmental units that are already occupied by an entity (cell ...) 
      max_action_range (tuple): tuple of the coordinates until which environmental units' is_occupied attribute are checked.

    Returns:
      bool: True if no environmental unit are occupied between the coordinates in the x and y lists and the coordinates in the max_action_range tuple
    """
    # Maximisation of the movement because it has to be an integer in order to be casted in the environment environment_grid
    # Multiplication by 2 or else the checking happens only on the surface of the actual entity
    if max_action_range[0] > 0:
      xm = 2*math.ceil(max_action_range[0])
    else:
      xm = math.floor(2*max_action_range[0])
    if max_action_range[1] > 0:
      ym = 2*math.ceil(max_action_range[1])
    else:
      ym = math.floor(2*max_action_range[1])

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


############
# MAIN CODE #
#############
if __name__ == "__main__":
  environment_grid1 = EnvironmentGrid(10,10,300)
  environment_grid2 = EnvironmentGrid(8,14,150)
  # Print test
  print(environment_grid1) # OK
  print(environment_grid2) # OK

  # Occupation tests
  print(environment_grid1.areAllUnitsNotOccupied(0,10,0,10) == True) # OK
  print(environment_grid1.areAllUnitsNotOccupied(0,10,0,10) == False) # OK
  print(environment_grid1.areAllUnitsNotOccupied(3,4,3,4) == True) # OK
  print(environment_grid1.areAllUnitsNotOccupied(4,7,4,7) == False) # OK

  # Changing is_occupied tests
  environment_grid1.changeMultipleOccupationStates(list(range(4,8)), list(range(4,8)), occupation_state=True)
  environment_grid1.changeMultipleOccupationStates([6], [1], occupation_state=True)
  environment_grid1.changeMultipleOccupationStates([2], [5], occupation_state=True)
  print(environment_grid1) # print test : axes x and y are inverted for the printing of is_occupied

  # Collision tests
  print(environment_grid1.isSpace(list(range(4,8)), list(range(4,8)), (0,-3)) == False) # OK
  print(environment_grid1.isSpace(list(range(4,8)), list(range(4,8)), (-2,0)) == False) # OK
