import math

if __name__ == "__main__":
    import os
    import sys

    currentdir = os.path.dirname(os.path.realpath(__file__))
    parentdir = os.path.dirname(currentdir)
    grandparentdir = os.path.dirname(parentdir)
    sys.path.append(grandparentdir)

from environment.unit.EnvironmentUnit import EnvironmentUnit


class EnvironmentGrid:
    """This class represents a units_on_width x units_on_length grid where an
    environmental unit is stored at each coordinates.
    The x axis goes from left to right. The y axis goes from top to bottom.

    Attributes :
        units_on_width (int): the number of columns, or environmental units along
            the x axis.
        units_on_length (int): the number of rows, or environmental units along the y axis.
        width (float): width of the environment grid, in meters
        length (float): length of the environment grid, in meters
        environment_units_list (list): list containing the environmental units
    """

    units_on_width: int
    units_on_length: int

    width: int  # pixels
    length: int  # pixels

    calculus_width: float  # m
    calculus_length: float  # m

    environment_units_list: list[list[EnvironmentUnit]]

    def __init__(self, nb_units_width: int, nb_units_length: int) -> None:
        self.units_on_width, self.units_on_length = nb_units_width, nb_units_length

        self.calculus_width = self.units_on_width * EnvironmentUnit.calculus_width
        self.calculus_length = self.units_on_length * EnvironmentUnit.calculus_length

        self.width = self.units_on_width * EnvironmentUnit.width
        self.length = self.units_on_length * EnvironmentUnit.length

        self.environment_units_list = [
            [EnvironmentUnit() for i in range(self.units_on_width)]
            for j in range(self.units_on_length)
        ]

    def __str__(self) -> str:
        index = 0
        string = f"Environment grid dimensions : {self.units_on_width} x {self.units_on_length} units\n"
        # Representing the environment grid with an X when the environmental unit is occupied and with . when it is not.
        string += "["
        for n in range(0, self.units_on_width - 1):
            string += f"{n},"
        string += f"{self.units_on_width-1}]\n"
        for row in self.environment_units_list:
            string += "["
            for unit in row:
                if unit.is_occupied:
                    string += "X "
                else:
                    string += ". "
            string += f"]{str(index)}\n"
            index += 1

        return string

    def getEnvironmentUnit(
        self, position_x: float, position_y: float
    ) -> EnvironmentUnit:
        """Returns the environment unit at the wanted wanted position.
        Coordinates are converted to integers.
        Coordinates are congruents to the number of columns and rows because the environment is a topological 2-Sphere.

        Args:
          position_x (float): coordinates along x axis of the wanted environmental unit
          position_y (float): coordinates along y axis of the wanted environmental unit

        Returns:
          EnvironmentUnit: object of class EnvironmentUnit
        """
        return self.environment_units_list[
            position_x // EnvironmentUnit.width % self.units_on_width
        ][position_y // EnvironmentUnit.length % self.units_on_length]

    def changeMultipleOccupationStates(
        self,
        starting_coor: tuple,
        ending_coor: tuple,
        occupation_state: bool,
    ) -> None:
        """Sets the environmental units between the starting and ending coordinates
        on the value of occupation_state.

        Args:
            starting_coor (tuple): contains the (x, y) coordinates of an entity
            ending_coor (tuple): contains the (ending_x, ending_y) coordinates of and entity
            occupation_state (bool): the final value of the is_occupied attribute of the concerned environmental units
        """
        for x in range(
            math.floor(starting_coor[0]),
            math.ceil(ending_coor[0]),
            EnvironmentUnit.width,
        ):
            for y in range(
                math.floor(starting_coor[1]),
                math.ceil(ending_coor[1]),
                EnvironmentUnit.length,
            ):
                self.getEnvironmentUnit(x, y).changeOccupationState(occupation_state)

    def areAllUnitsNotOccupied(
        self,
        starting_coor: tuple,
        ending_coor: tuple,
    ) -> bool:
        """Navigates through all the environmental units of the environment grid between the starting x and y coordinates
        and the ending x and y.
        For each environmental unit encountered, it checks its is_occupied attribute.
        If one is set on True, then the function returns False.
        The function returns True if and only if every environmental units have their is_occupied attribute sets on False.

        Args:
            starting_coor (tuple): x and y coordinates of the environment grid where to begin the navigation
            ending_coor (tuple): x and y coordinates of the environment grid where to end the navigation

        Returns:
            bool: True if every environmental units have their is_occupied attribute set on False, False otherwise.
        """
        for x in range(
            math.floor(starting_coor[0]),
            math.ceil(ending_coor[0]),
            EnvironmentUnit.width,
        ):
            for y in range(
                math.floor(starting_coor[1]),
                math.ceil(ending_coor[1]),
                EnvironmentUnit.length,
            ):
                if self.getEnvironmentUnit(x, y).is_occupied:
                    return False
                else:
                    pass
        return True

    def isSpace(
        self, starting_coor: tuple, ending_coor: tuple, max_action_range: tuple
    ) -> bool:
        """Checks if the environment units in a certain max_action_range are available for the entity to move or replicate.

        Args:
            starting_coor (tuple): x and y coordinates of the environment grid where to begin the navigation
            ending_coor (tuple): x and y coordinates of the environment grid where to end the navigation
            max_action_range (tuple): tuple of the coordinates until which environmental units' is_occupied attribute are checked.

        Returns:
            bool: True if no environmental unit are occupied between the coordinates in the x and y lists and the coordinates in the max_action_range tuple
        """
        # Maximisation of the movement because it has to be an integer in order to be casted in the environment environment_grid

        if max_action_range[0] > 0:
            xm = math.ceil(max_action_range[0])
        else:
            xm = math.floor(2 * max_action_range[0])
        if max_action_range[1] > 0:
            ym = math.ceil(max_action_range[1])
        else:
            ym = math.floor(2 * max_action_range[1])

        xstart, ystart, xend, yend = (
            starting_coor[0],
            starting_coor[1],
            ending_coor[0],
            ending_coor[1],
        )
        # print(xstart,xend,xm,";",ystart,yend,ym)

        if xm >= 0 and ym >= 0:
            if self.areAllUnitsNotOccupied((xend, ystart + ym), (xend + xm, yend + ym)):
                if self.areAllUnitsNotOccupied((xstart + xm, xend), (yend, yend + ym)):
                    return True
            return False

        elif xm >= 0 and ym <= 0:
            if self.areAllUnitsNotOccupied((xend, ystart + ym), (xend + xm, yend + ym)):
                if self.areAllUnitsNotOccupied(
                    (xstart + xm, ystart + ym), (xend, ystart)
                ):
                    return True
            return False

        elif xm <= 0 and ym >= 0:
            if self.areAllUnitsNotOccupied(
                (xstart + xm, ystart + ym), (xstart, yend + ym)
            ):
                if self.areAllUnitsNotOccupied((xstart, yend), (xend + xm, yend + ym)):
                    return True
            return False

        else:
            if self.areAllUnitsNotOccupied(
                (xstart + xm, ystart + ym), (xstart, yend + ym)
            ):
                if self.areAllUnitsNotOccupied(
                    (xstart, ystart + ym), (xend + xm, ystart)
                ):
                    return True
            return False


if __name__ == "__main__":
    environment_grid = EnvironmentGrid(10, 10)

    # Print test
    print(environment_grid)  # OK

    # Changing is_occupied tests
    environment_grid.changeMultipleOccupationStates((3, 3), (6, 6), True)  # OK
    print(
        environment_grid
    )  # print test : axes x and y are inverted for the printing of is_occupied
    environment_grid.changeMultipleOccupationStates(
        (7.68, 6.15), (9.36, 8.77), True
    )  # OK
    print(environment_grid)

    # Occupation tests
    # print(environment_grid.areAllUnitsNotOccupied(0,10,0,10) == False) # OK
    # print(environment_grid.areAllUnitsNotOccupied(3,4,3,4) == True) # OK
    # print(environment_grid.areAllUnitsNotOccupied(4,7,4,7) == False) # OK
