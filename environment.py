###########
# MODULES #
###########
from cell import Cell
import environment_unit

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
        self.number_columns: int = round(
            self.width / environment_unit.EnvironmentalUnit.width
        )
        self.number_rows: int = round(
            self.length / environment_unit.EnvironmentalUnit.length
        )
        # Create a grid with an EnvironmentalUnit object for each columns
        #                                         and that for each rows
        self.grid: list = [
            [environment_unit.EnvironmentalUnit(x * environment_unit.EnvironmentalUnit.width,y * environment_unit.EnvironmentalUnit.length,)
            for x in range(self.number_columns)]
            for y in range(self.number_rows)
        ]

    ###########
    # METHODS #
    ########### 
    def CellUsingSpace(self, occupied_x_coord: list, occupied_y_coord: list) -> None:
        """
        This method go through all the coordinates stored in cell.occupied_x_coordinates (same for y) with an increment depending of the size of 
        an environment_unit and sets all environment_units to 'occupied'.
        Args:
            occupied_x_coord (list): all the x coordinates occupied by the square of a cell
            occupied_y_coord (list): all the y coordinates occupied by the square of a cell
        """            
        for x in range(occupied_x_coord[0], occupied_x_coord[-1], environment_unit.EnvironmentalUnit.width):
            for y in (occupied_y_coord[0], occupied_y_coord[-1], environment_unit.EnvironmentalUnit.length):
                (self.grid[x][y]).is_occupied = True
        return None


    def IsSpaceForMoving(self,cell: Cell, direction : tuple) -> bool:
        """
        This method checks if the movement of the cell is possible and returns True if the environment unit in the direction of the movement 
        aren't occupied.
        Args :
            cell (Cell): cell object
            direction (tuple): a tuple given by the Direction.get_random_direction() method
        """
        

