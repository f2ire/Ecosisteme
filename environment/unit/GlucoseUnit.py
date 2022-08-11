from EnvironmentUnit import EnvironmentUnit
import math


class GlucoseUnit(EnvironmentUnit):
    """An environmental unit used to store and modify the glucose concentration of the
    environment.

    Attributes :
        glucose_concentration (float): glucose concetration of the unit, in kg/m³
        color (tuple): tuple in RGB format, used to display a glucose map of the environment

    Functions :
        changeGlucoseConcentration
        adaptGlucoseColor
    """

    glucose_concentration: float
    color: tuple

    def __init__(self, initial_concentration: float) -> None:
        """
        initial_concentration (float): initial glucose concentration, in kg/m³
        """
        super().__init__()
        self.glucose_concentration = initial_concentration
        self.adaptGlucoseColor()

    def __str__(self) -> str:
        string = (
            "Glucose "
            + super().__str__()
            + f"Having a glucose concentration of : {self.glucose_concentration} kg.m⁻³\n"
        )
        string += (
            f"Its color in RGB encoding is : ({self.color[0]:.2f}"
            + f" {self.color[1]:.2f}"
            + f" {self.color[2]:.2f})\n"
        )
        return string

    def changeGlucoseConcentration(self, new_glucose_concentration: float) -> None:
        """Replaces the actual glucose concentration of the unit by
        new_glucose_concentration.

        Args:
          new_glucose_concentration (float): concentration of glucose transiting through
              the unit, in kg/m³.
        """
        self.glucose_concentration = new_glucose_concentration

    def changeGlucoseConcentrationFromFlux(self, glucose_flux: float) -> None:
        """Updates the actual glucose concentration of the unit according to an incoming
        mass of glucose.

        Args:
          glucose_flux (float): flux of glucose transiting through the unit, in kg/m².
              Positive if the unit is receiving glucose, negative if it's losing
        """
        self.glucose_concentration += glucose_flux * self.surface / self.volume

    def adaptGlucoseColor(self) -> None:
        """Modifies the unit's color following a linear relationship with it's glucose
        concentration. When the concentration is equal to zéro, the color of the unit is
        mainly red. When the concetration is hight, the color becames green.
        """
        self.color = (
            -255 / 2 * math.erf(self.glucose_concentration * 2000 - 3) + 255 / 2,
            255 / 2 * math.erf(self.glucose_concentration * 1000 - 5) + 255 / 2,
            45,
        )


if __name__ == "__main__":
    test_glucose_unit = GlucoseUnit(0.005)
    scd_glucose_unit = GlucoseUnit(1.2 * 10 ** (-3))

    # Print tests
    print(test_glucose_unit)  # OK

    # Variable change tests

    test_glucose_unit.changeGlucoseConcentrationFromFlux(5 * 10 ** (-6))
    print(
        test_glucose_unit.glucose_concentration
        == 5 * 10 ** (-3) + 5 * 10 ** (-6) * 4 * 10 ** (-6) / (8 * 10 ** (-9))
    )  # OK

    print(test_glucose_unit)
    print(scd_glucose_unit)
