if __name__ == "__main__":
    import os
    import sys

    currentdir = os.path.dirname(os.path.realpath(__file__))
    parentdir = os.path.dirname(currentdir)
    sys.path.append(parentdir)
from unit.TemperatureUnit import EnvironmentUnit, TemperatureUnit, math, phy


class TemperatureGrid:
    """This class represents a units_on_width x units_on_length grid where an temperature unit is stored at each coordinates.
    The x axis goes from left to right. The y axis goes from top to bottom.

    Attributes :
      units_on_width (int): the number of columns, or environmental units along the x axis.
      units_on_length (int): the number of rows, or environmental units along the y axis.
      width (float): width of the environment grid, in meters
      length (float): length of the environment grid, in meters
      temperature_units_list (list): list containing the temperature units
    """

    units_on_width: int
    units_on_length: int

    width: float  # m
    length: float  # m

    temperature_units_list: list[list[TemperatureUnit]]

    def __init__(
        self, col_nb: int, row_nb: int, initial_temperature: float = 298.15
    ) -> None:
        self.units_on_width, self.units_on_length = col_nb, row_nb
        self.width = self.units_on_width * EnvironmentUnit.width
        self.length = self.units_on_length * EnvironmentUnit.length

        self.temperature_units_list = [
            [TemperatureUnit(initial_temperature) for i in range(self.units_on_width)]
            for j in range(self.units_on_length)
        ]

    def __str__(self) -> str:
        index = 0
        string = f"Temperature grid dimensions : {self.width}m x {self.length}m\n"

        string += "["
        for n in range(0, self.units_on_width - 1):
            string += f"{n},"
        string += f"{self.units_on_width-1}]\n"
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
        return self.temperature_units_list[math.floor(position_x) % self.units_on_width][
            math.floor(position_y) % self.units_on_length
        ]

    def computeAllTemperatureColors(self) -> None:
        """Adapt the color of every temperature units in the grid using their adaptTemperatureColor function"""
        for row in self.temperature_units_list:
            for unit in row:
                unit.adaptTemperatureColor()

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
                self.getTemperatureUnit(x, y).changeTemperature(new_temperature)

    def makeTemperatureDiffuse(self) -> None:
        """Cross every temperature unit and diffuses the temperature by thermal conduction."""
        for x in range(self.units_on_width):
            for y in range(self.units_on_length):
                leftward_flux = phy.computeThermalFlux(
                    self.getTemperatureUnit(x, y).temperature,
                    self.getTemperatureUnit(x - 1, y).temperature,
                )
                rigthward_flux = phy.computeThermalFlux(
                    self.getTemperatureUnit(x, y).temperature,
                    self.getTemperatureUnit(x + 1, y).temperature,
                )
                upward_flux = phy.computeThermalFlux(
                    self.getTemperatureUnit(x, y).temperature,
                    self.getTemperatureUnit(x, y - 1).temperature,
                )
                downward_flux = phy.computeThermalFlux(
                    self.getTemperatureUnit(x, y).temperature,
                    self.getTemperatureUnit(x, y + 1).temperature,
                )
                self.getTemperatureUnit(x, y).changeTemperatureFromFlux(
                    leftward_flux + rigthward_flux + upward_flux + downward_flux
                )


if __name__ == "__main__":
    temp_grid = TemperatureGrid(4, 4, 300.047897)
    # OK -> possible de faire qqch pour bien aligner les index du haut cependant
    print(temp_grid)

    # Changing temperature test
    print(temp_grid.getTemperatureUnit(1, 1))
    temp_grid.changeMultipleTemperature([1, 2], [1, 2], 400)  # OK
    print(temp_grid)

    # Computing every temperature colors test
    temp_grid.computeAllTemperatureColors()
    print(temp_grid.getTemperatureUnit(1, 1))
    print(temp_grid.getTemperatureUnit(1, 2))
    print(temp_grid.getTemperatureUnit(2, 1))
    print(temp_grid.getTemperatureUnit(2, 2))  # OK

    # Diffusing temperature test
    # temp_grid.makeTemperatureDiffuse() # OK
    # print(temp_grid)
