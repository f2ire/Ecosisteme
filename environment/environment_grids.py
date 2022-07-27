###########
# MODULES #
###########
import math
from environment_units import * 
import physical_data as phy

####################
# CLASS DEFINITION #
####################
class EnvironmentGrid:
  """This class represents a column_number x row_number grid where an environmental unit is stored at each coordinates.
  The x axis goes from left to right. The y axis goes from top to bottom.

  Attributes :
    column_number (int): the number of columns, or environmental units along the x axis.
    row_number (int): the number of rows, or environmental units along the y axis.
    environment_units_list (list): list containing the environmental units

  Functions :
    getEnvironmentUnit
    areAllUnitsNotOccupied
    changeMultipleOccupationStates
    isSpace
  """
  column_number: int
  row_number: int

  environment_units_list: list

  def __init__(self, col_nb: int, row_nb: int) -> None:
    self.column_number, self.row_number = col_nb, row_nb

    self.environment_units_list = [
      [EnvironmentUnit() for i in range(self.column_number)] for j in range(self.row_number)] 

  def __str__(self) -> str:
    index = 0
    string = f"Grid dimensions : ({self.column_number},{self.row_number}) \n"
    # Representing the environment grid with an X when the environmental unit is occupied and with . when it is not.
    string += "["
    for n in range(0,self.column_number-1):
      string += f"{n},"
    string += f"{self.column_number-1}]\n"
    for row in self.environment_units_list:
      string += "["
      for unit in row:
        if unit.is_occupied:
          string += "X "
        else :
          string += ". "
      string += f"]{str(index)}\n"
      index += 1
    
    return string
  
  def getEnvironmentUnit(self, position_x: int, position_y: int) -> EnvironmentUnit:
    """Returns the environment unit at the wanted wanted position.
    Coordinates are converted to integers. 
    Coordinates are congruents to the number of columns and rows because the environment is a topological 2-Sphere.

    Args:
      position_x (int): position along x axis of the wanted environmental unit
      position_y (int): position along y axis of the wanted environmental unit

    Returns:
      EnvironmentUnit: object of class EnvironmentUnit
    """
    return self.environment_units_list[math.floor(position_x) % self.column_number][math.floor(position_y) % self.row_number]

  def changeMultipleOccupationStates(self, xlist, ylist, occupation_state: bool) -> None:
    """Sets the environmental units concerned by the x and y lists to the value of occupation_state.
    
    Args:
      xlist (np.array): numpy array containing the x coordinates of the environmental units to be affected by the change of occupation state 
      ylist (np.array): numpy array containing the y coordinates of the environmental units to be affected by the change of occupation state 
      occupation_state (bool): the final value of the is_occupied attribute of the concerned environmental units
    """
    for x in xlist:
      for y in ylist:
        self.getEnvironmentUnit(x, y).changeOccupationState(occupation_state)

  def areAllUnitsNotOccupied(self, starting_x: int, ending_x: int, starting_y: int, ending_y: int) -> bool:
    """Navigates through all the environmental units of the environment grid between the starting x and y coordinates 
    and the ending x and y. 
    For each environmental unit encountered, it checks its is_occupied attribute. 
    If one is set on True, then the function returns False.
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
        if self.getEnvironmentUnit(x, y).is_occupied:
          return False
        else:pass
    return True

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


class TemperatureGrid:
  """This class represents a column_number x row_number grid where an temperature unit is stored at each coordinates.
  The x axis goes from left to right. The y axis goes from top to bottom.

  Attributes :
    column_number (int): the number of columns, or environmental units along the x axis.
    row_number (int): the number of rows, or environmental units along the y axis.
    temperature_units_list (list): list containing the temperature units
  """
  column_number: int
  row_number: int

  temperature_units_list: list

  def __init__(self, nbCol: int, nbRows: int, initial_temperature: float = 298.15) -> None:
    self.column_number, self.row_number = nbCol, nbRows
    self.temperature_units_list = [
      [TemperatureUnit(initial_temperature)for i in range(self.column_number)]
    for j in range(self.row_number)]

  def __str__(self) -> str:
    index = 0
    string = f"Grid dimensions : ({self.column_number},{self.row_number}) \n"
    
    string += "["
    for n in range(0,self.column_number-1):
      string += f"{n},"
    string += f"{self.column_number-1}]\n"
    for row in self.temperature_units_list:
      string += "["
      for unit in row:
        string += f"{unit.temperature:.0f} "
      string += f"]{str(index)}\n"
      index += 1
    
    return string

  def getTemperatureUnit(self, position_x: int, position_y: int) -> TemperatureUnit:
    """Returns the temperature unit at the wanted wanted position

    Args:
      position_x (int): position along x axis of the wanted temperature unit
      position_y (int): position along y axis of the wanted temperature unit

    Returns:
      TemperatureUnit: object of class TemperatureUnit
    """
    return self.temperature_units_list[math.floor(position_x) % self.column_number][math.floor(position_y) % self.row_number]

  def changeMultipleTemperature(self, xlist, ylist, new_temperature: float) -> None:
    """Sets the concerned temperature units's temperature on new_temperature.

    Args:
      xlist (np.array): numpy array containing the x coordinates of the temperature units 
      to be affected by the change of temperature
      ylist (np.array): numpy array containing the y coordinates of the temperature units 
      to be affected by the change of temperature
      new_temperature (float): new temperature to be set in Kelvin
    """
    for x in xlist:
      for y in ylist:
        self.getTemperatureUnit(x,y).changeTemperature(new_temperature)

  def makeTemperatureDiffuse(self) -> None:
    """Cross every temperature unit and diffuses the temperature by thermal conduction.
    """
    for x in range(self.column_number):
      for y in range(self.row_number):
        leftward_flux  = phy.computeThermalFlux(self.getTemperatureUnit(x,y).temperature, self.getTemperatureUnit(x-1,y).temperature)
        rigthward_flux = phy.computeThermalFlux(self.getTemperatureUnit(x,y).temperature, self.getTemperatureUnit(x+1,y).temperature)
        upward_flux    = phy.computeThermalFlux(self.getTemperatureUnit(x,y).temperature, self.getTemperatureUnit(x,y-1).temperature)
        downward_flux  = phy.computeThermalFlux(self.getTemperatureUnit(x,y).temperature, self.getTemperatureUnit(x,y+1).temperature)
        self.getTemperatureUnit(x,y).changeTemperatureFromFlux(leftward_flux+rigthward_flux+upward_flux+downward_flux)


class GlucoseGrid:
  """This class represents a column_number x row_number grid where an glucose unit is stored at each coordinates.
  The x axis goes from left to right. The y axis goes from top to bottom.

  Attributes :
    column_number (int): the number of columns, or environmental units along the x axis.
    row_number (int): the number of rows, or environmental units along the y axis.
    glucose_units_list (list): list containing the glucose units
  """
  column_number: int
  row_number: int

  glucose_units_list: list

  def __init__(self, nbCol: int, nbRows: int, initial_glucose: float = 0) -> None:
    self.column_number, self.row_number = nbCol, nbRows
    self.glucose_units_list = [
      [GlucoseUnit(initial_glucose)for i in range(self.column_number)]
    for j in range(self.row_number)]

  def __str__(self) -> str:
    index = 0
    string = f"Grid dimensions : ({self.column_number},{self.row_number}) \n"
    
    string += "["
    for n in range(0,self.column_number-1):
      string += f"{n},"
    string += f"{self.column_number-1}]\n"
    for row in self.glucose_units_list:
      string += "["
      for unit in row:
        string += f"{unit.glucose_concentration:.2e} "
      string += f"]{str(index)}\n"
      index += 1
    
    return string

  def getGlucoseUnit(self, position_x: int, position_y: int) -> GlucoseUnit:
    """Returns the temperature unit at the specified position

    Args:
      position_x (int): position along x axis of the wanted temperature unit
      position_y (int): position along y axis of the wanted temperature unit

    Returns:
      GlucoseUnit: object of class GlucoseUnit
    """
    return self.glucose_units_list[math.floor(position_x) % self.column_number][math.floor(position_y) % self.row_number]

  def changeMultipleGlucoseConcentration(self, xlist, ylist, new_glucose_concentration: float) -> None:
    """Sets the concerned temperature units's temperature on new_temperature.

    Args:
      xlist (np.array): numpy array containing the x coordinates of the temperature units 
      to be affected by the change of glucose concentration
      ylist (np.array): numpy array containing the y coordinates of the temperature units 
      to be affected by the change of glucose concentration
      new_concentration (float): new glucose concentration to be set in Kelvin
    """
    for x in xlist:
      for y in ylist:
        self.getGlucoseUnit(x,y).changeGlucoseConcentration(new_glucose_concentration)

  def makeGlucoseDiffuse(self) -> None:
    """Cross every glucose unit in the glucose grid and diffuses the glucose. 
    For each glucose unit, it computes 4 massic flux, one for each glucose units around it, 
    and modifies the glucose concentration in the glucose unit in consequence.
    """
    for x in range(self.column_number):
      for y in range(self.row_number):
        print(f"coor : ({x},{y})")
        leftward_flux  = phy.computeGlucoseFlux(self.getGlucoseUnit(x,y).glucose_concentration,self.getGlucoseUnit(x-1,y).glucose_concentration)
        rigthward_flux = phy.computeGlucoseFlux(self.getGlucoseUnit(x,y).glucose_concentration,self.getGlucoseUnit(x+1,y).glucose_concentration)
        upward_flux    = phy.computeGlucoseFlux(self.getGlucoseUnit(x,y).glucose_concentration,self.getGlucoseUnit(x,y-1).glucose_concentration)
        downward_flux  = phy.computeGlucoseFlux(self.getGlucoseUnit(x,y).glucose_concentration,self.getGlucoseUnit(x,y+1).glucose_concentration)
        print(f"Total flux : {leftward_flux+rigthward_flux+upward_flux+downward_flux}")
        self.getGlucoseUnit(x,y).changeGlucoseConcentrationFromFlux(leftward_flux+rigthward_flux+upward_flux+downward_flux)

############
# MAIN CODE #
#############
if __name__ == "__main__":
  environment_grid = EnvironmentGrid(3,3)

  # Print test
  print(environment_grid) # OK

  # Changing is_occupied tests
  #environment_grid.changeMultipleOccupationStates(list(range(4,8)), list(range(4,8)), occupation_state=True)
  #environment_grid.changeMultipleOccupationStates([1], [1], occupation_state=True)
  #environment_grid.changeMultipleOccupationStates([2], [2], occupation_state=True)
  #print(environment_grid) # print test : axes x and y are inverted for the printing of is_occupied

  # Occupation tests
  #print(environment_grid.areAllUnitsNotOccupied(0,10,0,10) == False) # OK
  #print(environment_grid.areAllUnitsNotOccupied(3,4,3,4) == True) # OK
  #print(environment_grid.areAllUnitsNotOccupied(4,7,4,7) == False) # OK

  # Collision tests
  #print(environment_grid.isSpace(list(range(4,8)), list(range(4,8)), (0,-3)) == False) # OK
  #print(environment_grid.isSpace(list(range(4,8)), list(range(4,8)), (-2,0)) == False) # OK

  # Printing TemperatureUnit tests
  #temp_grid = TemperatureGrid(4,4,300.047897)
  #print(temp_grid) # OK -> possible de faire qqch pour bien aligner les index du haut cependant

  # Changing temperature test
  #temp_grid.changeMultipleTemperature([1,2],[1,2],400) # OK
  #print(temp_grid)

  # Diffusing temperature test
  #temp_grid.makeTemperatureDiffuse() # OK 
  #print(temp_grid)

  # Printing GlucoseUnit test
  gluc_grid = GlucoseGrid(3,3,5*10**(-3)) # OK
  print(gluc_grid) # OK

  # Changing glucose concentration test
  gluc_grid.changeMultipleGlucoseConcentration([1],[1],7*10**(-3))
  print(gluc_grid) # OK

  # Glucose diffusion test
  gluc_grid.makeGlucoseDiffuse()
  print(gluc_grid)

  while gluc_grid.getGlucoseUnit(0,1).glucose_concentration != gluc_grid.getGlucoseUnit(1,1).glucose_concentration:
    gluc_grid.makeGlucoseDiffuse()
    print(gluc_grid)