if __name__ == "__main__":
    import os
    import sys

    currentdir = os.path.dirname(os.path.realpath(__file__))
    parentdir = os.path.dirname(currentdir)
    grandparentdir = os.path.dirname(parentdir)
    sys.path.append(grandparentdir)

import math
from environment.unit.GlucoseUnit import EnvironmentUnit, GlucoseUnit
import environment.physical_data as phy


class GlucoseGrid:
    """This class represents a units_on_width x units_on_length grid where an glucose unit is stored at each coordinates.
    The x axis goes from left to right. The y axis goes from top to bottom.

    Attributes :
      units_on_width (int): the number of columns, or environmental units along the x axis.
      units_on_length (int): the number of rows, or environmental units along the y axis.
      width (float): width of the environment grid, in meters
      length (float): length of the environment grid, in meters
      glucose_units_list (list): list containing the glucose units
    """

    units_on_width: int
    units_on_length: int

    width: float  # m
    length: float  # m

    glucose_units_list: list[list[GlucoseUnit]]

    def __init__(self, col_nb: int, row_nb: int, initial_glucose: float = 0) -> None:
        self.units_on_width, self.units_on_length = col_nb, row_nb
        self.width = self.units_on_width * EnvironmentUnit.side_length
        self.length = self.units_on_length * EnvironmentUnit.side_length

        self.glucose_units_list = [
            [GlucoseUnit(initial_glucose) for i in range(self.units_on_width)]
            for j in range(self.units_on_length)
        ]

    def __str__(self) -> str:
        index = 0
        string = f"Glucose grid dimensions : {self.width}m x {self.length}m\n"
        string += "["
        for n in range(0, self.units_on_width - 1):
            string += f"{n},"
        string += f"{self.units_on_width-1}]\n"
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
        return self.glucose_units_list[
            position_x // EnvironmentUnit.side_length % self.units_on_width
        ][position_y // EnvironmentUnit.side_length % self.units_on_length]

    def changeMultipleGlucoseConcentration(
        self, xlist, ylist, new_glucose_concentration: float
    ) -> None:
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
                self.getGlucoseUnit(x, y).changeGlucoseConcentration(
                    new_glucose_concentration
                )

    def computeAllGlucoseColor(self) -> None:
        """Adapt the color of every glucose units in the grid using their adaptGlucoseColor function"""
        for row in self.glucose_units_list:
            for glu_unit in row:
                glu_unit.adaptGlucoseColor()

    def computeTotalGlucoseQuantity(
        self, starting_coor: tuple, ending_coor: tuple
    ) -> float:
        """Returns the total mass of glucose contained in the glucose units between
        the starting and ending coordinates of the grid.

        Args:
            starting_coor (tuple): contains the (x, y) coordinates of an entity
            ending_coor (tuple): contains the (ending_x, ending_y) coordinates of and entity

        Returns:
            float: mass of glucose, in kg, contained in all the glucose units
        """
        glucose_total_mass = 0
        for x in range(
            math.floor(starting_coor[0]),
            math.ceil(ending_coor[0]),
            GlucoseUnit.side_length,
        ):
            for y in range(
                math.floor(starting_coor[1]),
                math.ceil(ending_coor[1]),
                GlucoseUnit.side_length,
            ):
                glucose_total_mass += self.getGlucoseUnit(x, y).computeGlucoseQuantity()
        return glucose_total_mass

    def makeGlucoseDiffuse(self) -> None:
        """Cross every glucose unit in the glucose grid and diffuses the glucose.
        For each glucose unit, it computes 4 massic flux, one for each glucose units around it,
        and modifies the glucose concentration in the glucose unit in consequence.
        """
        for x in range(self.units_on_width):
            for y in range(self.units_on_length):
                print(f"coor : ({x},{y})")
                leftward_flux = phy.computeGlucoseFlux(
                    self.getGlucoseUnit(x, y).glucose_concentration,
                    self.getGlucoseUnit(x - 1, y).glucose_concentration,
                )
                rigthward_flux = phy.computeGlucoseFlux(
                    self.getGlucoseUnit(x, y).glucose_concentration,
                    self.getGlucoseUnit(x + 1, y).glucose_concentration,
                )
                upward_flux = phy.computeGlucoseFlux(
                    self.getGlucoseUnit(x, y).glucose_concentration,
                    self.getGlucoseUnit(x, y - 1).glucose_concentration,
                )
                downward_flux = phy.computeGlucoseFlux(
                    self.getGlucoseUnit(x, y).glucose_concentration,
                    self.getGlucoseUnit(x, y + 1).glucose_concentration,
                )
                print(
                    f"Total flux : {leftward_flux+rigthward_flux+upward_flux+downward_flux}"
                )
                self.getGlucoseUnit(x, y).changeGlucoseConcentrationFromFlux(
                    leftward_flux + rigthward_flux + upward_flux + downward_flux
                )


if __name__ == "__main__":
    # Printing GlucoseUnit test
    gluc_grid = GlucoseGrid(3, 3, 5 * 10 ** (-3))  # OK
    print(gluc_grid)  # OK

    # Changing glucose concentration test
    print(gluc_grid.getGlucoseUnit(1, 1))
    gluc_grid.changeMultipleGlucoseConcentration([1], [1], 7 * 10 ** (-3))
    print(gluc_grid)  # OK

    # Computing every color adapation test
    gluc_grid.computeAllGlucoseColor()  # OK
    print(gluc_grid.getGlucoseUnit(1, 1))

    # Glucose diffusion test
    # gluc_grid.makeGlucoseDiffuse()
    # print(gluc_grid)

    # while gluc_grid.getGlucoseUnit(0,1).glucose_concentration != gluc_grid.getGlucoseUnit(1,1).glucose_concentration:
    #  gluc_grid.makeGlucoseDiffuse()
    #  print(gluc_grid) # OK
