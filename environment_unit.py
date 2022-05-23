###########
# MODULES #
###########
import math

####################
# CLASS DEFINITION #
####################
class EnvironmentalUnit:
  """This class provides the smallest element of our environment
  Object of a square of length x width.
  This element is capable of welcoming only a single living individuals in it's surface
  Furthermore, it store environmental parameters such as temperature, pression, height etc.
  Attribute
  -------
  xlist : list
    List of all int x in the object
  ylist : list
    List of all int y in the object
  Method
  -------
  """
  # Dimensions
  length: int = 2
  width: int = 2
  # Attributes telling if it is occupied or not
  is_occupied: bool = False
  contained_entity: list = []
  
  # FONDAMENTAL METHODS
  def __init__(self, posx: int, posy: int):
    """
    Unit of a object Environment.
    Args:
      posx (int): positions on x axis
      posy (int): positions on y axis
    """
    # Initialization of the position
    self.xlist: list = list(range(posx, posx + self.length))
    self.ylist: list = list(range(posy, posy + self.width))
  
  def __str__(self) -> str:
    return f"Unit at ({self.xlist[0]}, {self.ylist[0]})"

  
  # OTHER METHODS
  def IsInside(self, posx: float, posy: float)-> bool:
    """True if the given coordinates are contained between the thresholds of xlist and ylist, False if not.

    Args:
      posx (float): coordinates of an entity along the x axis
      posy (float): coordinates of an entity along the y axis

    Returns:
      bool: True if the given coordinates are contained between the thresholds of xlist and ylist, False if not.
    """
    if posx < self.xlist[-1] and posx > self.xlist[0] and posy < self.ylist[-1] and posy > self.ylist[0]:
      return True
    else : return False
############
# MAIN CODE #
#############
