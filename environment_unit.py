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
    This element is just storing all the cells according to their coordonate
    Furthermore, it store environmental parameters such as temperature,
    pression etc.

    Attribute
    -------
    xlist : list
        List of all int x in the object
    ylist : list
        List of all int y in the object
    cell_list : list
        List of all Cell object in the coordinates of the object
    attributes : tuple
        Tuple with all attribate to draw a square

    Method
    -------
    is_cell_coord_are_inside(self, cell : Cell) -> bool
        Return True if cell's coordinates are in self.ylist and self.xlist
    cell_insert(self, cell : Cell) -> None
        Add new cell in self.cell_list if cell is not in cell_list, but
        if his coordinate are in self.ylist and self.xlist
    cell_del(self, cell : Cell) -> None
        Del current cell from self.cell_list if his coordinate are not in
        self.ylist and self.xlist
    isOcuppied(self) -> bool
        Return True if there are Cell in self.cell_list, else False
    """

    # Dimensions
    length = 10
    width = 10

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
        self.cell_list = []
        # Attributes is in this rectangle tuple format to fit
        # to the pygame.fill() method which fills rectangle objects
        self.attributes = (
            self.xlist[0],
            self.ylist[0],
            self.length,
            self.width,
        )

    # OTHER METHODS
    def is_cell_coord_are_inside(self, cell):
        return (
            math.floor(cell.x) in self.xlist
            and math.floor(cell.y) in self.ylist
        )

    def cell_insert(self, cell):
        if self.is_cell_coord_are_inside(cell) and cell not in self.cell_list:
            self.cell_list.append(cell)

    def cell_del(self, cell):
        if not self.is_cell_coord_are_inside(cell) and cell in self.cell_list:
            self.cell_list.remove(cell)

    def isOccupied(self):
        if len(self.cell_list) != 0:
            self.is_occupied = True


#############
# MAIN CODE #
#############
