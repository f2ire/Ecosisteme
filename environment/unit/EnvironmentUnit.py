if __name__ == "__main__":
    import os
    import sys

    currentdir = os.path.dirname(os.path.realpath(__file__))
    parentdir = os.path.dirname(currentdir)
    grandparentdir = os.path.dirname(parentdir)
    sys.path.append(grandparentdir)

import environment.physical_data as phy


class EnvironmentUnit:
    """The fondamental unit of the environment represented by a cube of
    shape width x length x height.
    This class is used to keep tracks of the position of entities in the environment.
    This class is also used to defined other units that will store essential data
    for the environment.
    This class contains attributes shared by all the subclasses.
    For the calculus, an unit is represented as a cube of water.

    Attributes :
        width (int): the size of one side of the unit, in m
        length (int): the size of one side of the unit, in m
        height (int): the size of one side of the unit, in m
        surface (float): surface of one unit, in m²
        volume (float): volume of one unit, in m³
        mass (float): total mass of one unit, calculated as it's a cube of water
        width (int): width of the unit on the display windows in pixels
        length (int): length of the unit on the display windows in pixels
        is_occupied (bool): True if the unit is occupated by an entity of the environment,
            False if nothing lays in it
    """

    side_length: int = 5  # in pixels

    side_length_calculus: float = phy.convertPixelsToMeters(side_length) * 10**6  # um

    surface: float = side_length**2  # um²
    volume: float = side_length**3  # um³
    mass: float = volume * phy.WATER_DENSITY  # ug

    is_occupied: bool = False

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        string = f"Unit of volume {self.volume}m³\n"
        string += f"Dimensions : {self.side_length_calculus}m x {self.side_length_calculus}m x {self.side_length_calculus}m\n"
        string += f"is_occupied : {self.is_occupied}\n"
        return string

    def changeOccupationState(self, new_occupation_state: bool) -> None:
        """Change the is_occupied attribute with the value of new_occupation_state.

        Args:
            new_occupation_state (bool): True if the unit becomes occupied, False otherwise
        """
        self.is_occupied = new_occupation_state


if __name__ == "__main__":
    test_occupation_unit = EnvironmentUnit()
    # Print tests
    print(test_occupation_unit)  # OK

    # Display parameters verification
    print(test_occupation_unit.side_length == 2.5)
    print(test_occupation_unit.side_length == 2.5)
