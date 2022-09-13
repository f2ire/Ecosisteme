# Number of seconds flowing after each iteration of the game loop
TIME_ITERATION: int = 10 ** (-2)  # seconds
PIXEL_METER_SCALE: float = 10 ** (-7)  # one pixel = 10⁻⁷ meter

# Universal constants
NA: float = 6.02214076 * 10**23  # Avogadero constant -> mol⁻¹
R: float = 8.31446261815324  # Gas constant -> J.K⁻¹.mol⁻¹
KB: float = 1.380649 * 10 ** (-23)  # Boltzmann constant -> J.mol⁻¹

# Glucose constants
# taken as constant for T = 298.15 K, in m²/s
GLUCOSE_DIFFUSION_COEFFICIENT: float = 0.651 * 10 ** (-9)
GLUCOSE_DENSITY: float = 1.54 * 10**3  # kg.m⁻³
GLUCOSE_MOLAR_MASS: float = 0.180156  # kg.mol⁻¹

# Water constants
WATER_DENSITY: float = 1.0 * 10**3  # kg.m⁻³
WATER_THERMAL_CONDUCTIVITY: float = 0.6  # W.m⁻¹.K⁻¹
WATER_HEAT_CAPACITY: float = 4.185 * 10**3  # J.K⁻¹.kg⁻¹


def computeThermalEnergy(thermal_flux: float) -> float:
    """Returns Q, the thermal energy according to the formula :
    Q = Flux * dt where dt is the time of one iteration of the loop

    Args:
        thermal_flux (float): thermal flux, in W

    Returns:
        float: Q, the thermal energy, in J
    """
    return thermal_flux * TIME_ITERATION


def computeThermalFlux(temperature_difference: float) -> float:
    """Computes phi, the thermal flux W according to Fourier's law of
    thermal diffusion

    Args:
        temperature_difference (float): in Kelvin

    Returns:
        float: thermal flux, in W.m⁻²
    """
    return -WATER_THERMAL_CONDUCTIVITY * temperature_difference


def computeGlucoseFlux(mass_concentration1: float, mass_concentration2: float) -> float:
    """Computes J, the flux of matter of glucose between two environmental
    units in position 1 (reference) and 2 according to Fick's law of matter
    diffusion. J = -D*(C1-C2)

    Args:
      concentration1 (float): mass concentration of the chemical in position 1,
            by convention the one of reference in kg/m³
      concentration2 (float): mass concentration of the chemical in position 2
            in kg/m³

    Returns:
        float: the flux of matter, in kg/m².
            Positive if concentration2 > concentration1.
    """
    return (
        -GLUCOSE_DIFFUSION_COEFFICIENT
        * (mass_concentration1 - mass_concentration2)
        * TIME_ITERATION
    )


def convertMetersToPixels(meters: float) -> int:
    """Conversion from a value in meters to a value in pixels, using
    the constant PIXEL_METER_SCALE

    Args:
        meters (float): a number of meters

    Returns:
        int: pixel conversion of the meters argument
    """
    return meters * 1 / PIXEL_METER_SCALE


def convertPixelsToMeters(pixels: int) -> float:
    """Conversion from a value in pixels to a value in meters, using
    the constant PIXEL_METER_SCALE

    Args:
        pixels (int): a number of pixels

    Returns:
        float: meter conversion of the pixels argument
    """
    return pixels * PIXEL_METER_SCALE


if __name__ == "__main__":
    # Thermal flux computation tests
    print(computeThermalEnergy(5) == 5 * TIME_ITERATION)  # OK
    print(computeThermalFlux(-100))  # == WATER_THERMAL_CONDUCTIVITY * 100
    # )  # OK

    # Glucose flux computation tests
    print(computeGlucoseFlux(5, 5) == 0)  # OK
    print(computeGlucoseFlux(0.001, 0.006) - 5.0127 < 10 ** (-6))  # OK
    print(computeGlucoseFlux(5 * 10 ** (-3), 7 * 10 ** (-3)))
