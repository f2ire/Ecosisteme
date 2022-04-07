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
        self.number_columns: int = round(
            self.width / EnvironmentalUnit.width
        )
        self.number_rows: int = round(
            self.length / EnvironmentalUnit.length
        )
        # Create a grid with an EnvironmentalUnit object in each columns 
        #                                         and that for each rows
        self.grid: list = [
            [EnvironmentalUnit(x * EnvironmentalUnit.width, y * EnvironmentalUnit.length,)
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
        for x in range(occupied_x_coord[0], occupied_x_coord[-1], EnvironmentalUnit.width):
            for y in range(occupied_y_coord[0], occupied_y_coord[-1], EnvironmentalUnit.length):
                (self.grid[x][y]).is_occupied = True
        return None


    def IsSpaceForMoving(self,cell: Cell, movement : tuple) -> bool:
        """
        This method checks if the movement of the cell is possible and returns True if the environment unit in the direction of the movement 
        aren't occupied. 
        It browses all the the space that will be occupied by the cell (after it movement) and check if environment units aren't occupied.
        Args :
            cell (Cell): cell object
            movement (tuple): a tuple of 2 float number giving the direction and the number of pixels a cell has to move -> (x_mvt, y_mvt)
        """
        print(movement)
        x_mvt, y_mvt = movement[0], movement[1] # to make the code more human readable
        for x_coo in range(math.floor((cell.x + x_mvt) % self.width), math.ceil((cell.x + cell.width + x_mvt) % self.width), EnvironmentalUnit.width):
            for y_coo in range(math.floor((cell.y + y_mvt) % self.length), math.ceil((cell.y + cell.length + y_mvt) % self.length), EnvironmentalUnit.length):
                if self.grid[x_coo][y_coo].is_occupied:
                    return False                
                else:pass
        return True


#############
# MAIN CODE #
#############
if __name__ == "__main__":
    env = Environment(100,100)
    blobby = Cell(2,7)
    blobou = Cell(5,3)
    blobby.InitiatePosition(enviro=env)
    blobou.InitiatePosition(enviro=env)
    for i in range(50):
        print(blobby)
        blobby.Moving(enviro=env)

