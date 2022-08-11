import physical_data as phy
from EnvironmentUnit import EnvironmentUnit
import math


class TemperatureUnit(EnvironmentUnit):
    """An environmental unit used to store and modify the temperature of the environment.

    Attributes :
        temperature (float): temperature of the unit, in Kelvin
        color (tuple): tuple in RGB format, used to display a temperature map of the
        environment

    Functions :
        changeTemperature
        adaptTemperatureColor
    """

    temperature: float
    color: tuple

    def __init__(self, initial_temperature: float) -> None:
        """
        initial_temperature (float): initial temperature of the unit, in Kelvin
        """
        super().__init__()
        self.temperature = initial_temperature
        self.adaptTemperatureColor()

    def __str__(self) -> str:
        string = (
            "Temperature "
            + super().__str__()
            + f"Having a temperature of : {self.temperature} K\n"
        )
        string += (
            f"Its color in RGB encoding is : ({self.color[0]:.2f}"
            + f"{self.color[1]:.2f}"
            + "{self.color[2]:.2f})\n"
        )
        return string

    def changeTemperature(self, new_temperature: float) -> None:
        """Sets the temperature attribute to new_temperature.

        Args:
            new_temperature (float): temperature to be set, in Kelvin
        """
        self.temperature = new_temperature

    def changeTemperatureFromFlux(self, thermal_flux: float) -> None:
        """Update the actual temperature attribute of the temperature unit according to
        the thermal flux it's receiving. Calculus is made following the equation
        Tf = Ti + Q/(m*c). Tf and Ti are final and initial temperature of the unit.
        m is the total mass of the unit, c it's heat capacity and Q the received thermal
        energy

        Args:
            thermal_flux (float): thermal flux the unit is receiving, in W
        """
        self.temperature += phy.computeThermalEnergy(thermal_flux) / (
            self.mass * phy.WATER_HEAT_CAPACITY
        )

    def adaptTemperatureColor(self) -> None:
        """Modifies the unit's temperature color according to its temperature.
        The color should be blue when the temperature is low, green when it is optimal
        and red when it's too high.
        """
        self.color = (
            255 / 2 * math.erf((self.temperature - 350) / 50) + 255 / 2,
            255 * math.exp(-1 / 1000 * (self.temperature - 320) ** 2),
            255 * math.exp(-self.temperature / 300),
        )


if __name__ == "__main__":
    test_temperature_unit = TemperatureUnit(298.15)
    # Print tests
    print(test_temperature_unit)  # OK

    # Variable change tests
    test_temperature_unit.changeTemperatureFromFlux(thermal_flux=0.5)
    print(
        test_temperature_unit.temperature
        == 298.15
        + phy.computeThermalEnergy(0.5)
        / (phy.WATER_HEAT_CAPACITY * phy.WATER_DENSITY * 8 * 10 ** (-9))
    )  # OK
    # Color adaptation test
    test_temperature_unit.adaptTemperatureColor()
    print(test_temperature_unit)  # OK
