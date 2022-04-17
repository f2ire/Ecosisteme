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
  length = 2
  width = 2
  is_occupied = False
  
  # FONDAMENTAL METHODS
  def __init__(self, posx: int, posy: int):
    """
    Unit of a object Environment.
    Args:
        posx (int): positions on x axis
        posy (int): positions on y axis
    """
    # Initialization of the position
    self.xlist = list(range(posx, posx + self.length))
    self.ylist = list(range(posy, posy + self.width))
  def __str__(self) -> str:
    return f"Unit at ({self.xlist[0]}, {self.ylist[0]})"
  
############
# MAIN CODE #
#############
