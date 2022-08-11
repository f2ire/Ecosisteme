from environment.environment_grids import EnvironmentGrid, TemperatureGrid, GlucoseGrid
from environment.environment_units import EnvironmentUnit
import pygame


class World:
    """Class containing all the physical and chemical grids needed to represent a functional environment.

    Attributes:
      width (float) : size of the width of the world in meters
      length (float) : size of the length of the world in meters
      display_tuple (tuple) : contains the width and length in pixels of the pygame windows presenting the world
      units_on_width (int)  : number of units along the width of the World/EnvironmentGrid
      units_on_length (int) : number of units along the length of the World/EnvironmentGrid
      environment_grid (EnvironmentGrid) : object of class EnvironmentGrid
      temperature_grid (TemperatureGrid) : object of class TemperatureGrid
      glucose_grid (GlucoseGrid) : object of class GlucoseGrid
    """

    width: int  # m
    length: int  # m

    display_tuple: tuple  # pixels x pixels

    units_on_width: int
    units_on_length: int

    environment_grid: EnvironmentGrid
    temperature_grid: TemperatureGrid
    glucose_grid: GlucoseGrid

    def __init__(
        self,
        nb_units_width: int,
        nb_units_length: int,
        initial_temperature: float = 298.15,
        initial_glucose: float = 0,
    ) -> None:
        """Initialize an environment as a rectangle of nb_units_width x nb_units_length units
        Args:
          nb_units_width (int): number of units along the width of the World
          nb_units_length (int): number of units along the length of the World
          initial_temperature (float): initial value of temperature of the environment in Kelvin
          initial_glucose (float): initial value of glucose concentration in the environment in kg.m⁻³
        """
        self.units_on_width, self.units_on_length = nb_units_width, nb_units_length

        self.width = EnvironmentUnit.width * self.units_on_width
        self.length = EnvironmentUnit.length * self.units_on_length

        self.display_tuple = (
            EnvironmentUnit.display_width * self.units_on_width,
            EnvironmentUnit.display_length * self.units_on_length,
        )

        self.environment_grid = EnvironmentGrid(
            self.units_on_width, self.units_on_length
        )
        self.temperature_grid = TemperatureGrid(
            self.units_on_width, self.units_on_length, initial_temperature
        )
        self.glucose_grid = GlucoseGrid(
            self.units_on_width, self.units_on_length, initial_glucose
        )

    def __str__(self) -> str:
        string = f"Evironment dimension ({self.width},{self.length}) \n" + str(
            self.environment_grid
        )
        string += str(self.environment_grid)
        return string

    def createUnitDisplayRectangle(self, x_position: int, y_position: int) -> tuple:
        """_summary_

        Args:
          x_position (int): _description_
          y_position (int): _description_

        Returns:
          tuple: _description_
        """
        return (
            x_position,
            y_position,
            EnvironmentUnit.display_width,
            EnvironmentUnit.display_length,
        )

    def displayTemperatureMap(self) -> None:
        """Display the temperature map of the world using pygame"""
        pygame.init()
        temperature_map = pygame.display.set_mode(self.display_tuple)
        self.temperature_grid.computeAllTemperatureColors()
        while True:
            event = pygame.event.poll()  # Collecting an event from the user
            if event.type == pygame.QUIT:  # End loop if user click on cross butun
                break

            x, y = 0, 0
            for row in self.temperature_grid.temperature_units_list:
                for temp_unit in row:
                    temp_unit_display_rectangle = self.createUnitDisplayRectangle(x, y)
                    temperature_map.fill(temp_unit.color, temp_unit_display_rectangle)
                    x += temp_unit_display_rectangle[2]
                x = 0
                y += temp_unit_display_rectangle[3]
            pygame.display.flip()
        pygame.quit()

    def displayGlucoseConcentrationMap(self) -> None:
        """Display the glucose concentration map of the world using pygame"""
        pygame.init()
        glucose_map = pygame.display.set_mode(self.display_tuple)
        self.glucose_grid.computeAllGlucoseColor()
        while True:
            event = pygame.event.poll()  # Collecting an event from the user
            if event.type == pygame.QUIT:  # End loop if user click on cross butun
                break

            x, y = 0, 0
            for row in self.glucose_grid.glucose_units_list:
                for glucose_unit in row:
                    glucose_unit_display_rectangle = self.createUnitDisplayRectangle(
                        x, y
                    )
                    glucose_map.fill(glucose_unit.color, glucose_unit_display_rectangle)
                    x += glucose_unit_display_rectangle[2]
                x = 0
                y += glucose_unit_display_rectangle[3]
            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    the_world = World(40, 40)  # 40 x 40 units
    print(the_world)  # OK
    print(the_world.display_tuple == (200, 200))  # OK
    print(the_world.createUnitDisplayRectangle(5, 3) == (5, 3, 5, 5))  # OK
    the_world.temperature_grid.changeMultipleTemperature(
        [3, 4, 5, 6], [3, 4, 5, 6], 2000
    )
    # the_world.displayTemperatureMap() # OK
    the_world.glucose_grid.changeMultipleGlucoseConcentration(
        [3, 4, 5, 6], [3, 4, 5, 6], 0.004
    )
    the_world.displayGlucoseConcentrationMap()  # OK
