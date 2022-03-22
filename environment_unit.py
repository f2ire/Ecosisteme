###########
# MODULES #
###########
import math

####################
# CLASS DEFINITION #
####################


class EnvironmentalUnit:
    """
    This class provides the smallest element of our environment ->
    a white 1x1 square
    This element is just storing environmental parameters such as temperature
    pression etc.
    This element remembers if it is emppty or occupied
    """

    # Dimensions and color of the unit
    (length, width) = (10, 10)  # 1x1 square

    # Boolean attribute telling if the unit is occupied by another element
    # of the ecosystem or not

    # FONDAMENTAL METHODS
    def __init__(self, posx, posy):
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
