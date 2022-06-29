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
    # Representing the environment environment_grid with 1 when the 'pixel' is occupied and 0 when it is not.
    string += "["
    for n in range(self.colum_number):
      string += f"{n}"
    string += " ]\n"
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


############
# MAIN CODE #
#############
if __name__ == "__main__":
  environment_grid1 = EnvironmentGrid(5,5,300)
  print(str(environment_grid1))