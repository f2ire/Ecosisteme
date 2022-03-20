###########
# MODULES # 
###########





####################
# CLASS DEFINITION #
####################
class environmental_unit:
  """
  This class provides the smallest element of our environment -> a white 1x1 square
  This element is just storing environmental parameters such as temperature, pression etc.
  This element remembers if it is emppty or occupied
  """
  # Dimensions and color of the unit
  (length, width) = (1,1)
  color = (255,255,255)
  
  # Boolean attribute telling if the unit is occupied by another element of the ecosystem or not
  is_occupied = False
  
  
  # FONDAMENTAL METHODS
  def __init__(self,posx,posy):
    # Initialization of the position
    self.x = posx
    self.y = posy
    
    # Attributes is in this rectangle tuple format to fit to the pygame.fill() method which fills rectangle objects 
    self.attributes = (self.x,self.y,self.length,self.width)
    






#############
# MAIN CODE #
#############