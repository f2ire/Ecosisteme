# Number of seconds flowing after each iteration of the game loop
TIME_ITERATION: int = 10 ** (-2)
PIXEL_METER_SCALE: float = 10 ** (-7)  # one pixel = 10⁻⁷ meter

# Universal constants
NA: float = 6.02214076 * 10**23  # Avogadero constant -> mol-1
R: float = 8.31446261815324  # Gas constant -> J/K/mol
KB: float = 1.380649 * 10 ** (-23)  # Boltzmann constant -> J/mol

# Glucose constants
# taken as constant for T = 298.15 K, in m²/s
GLUCOSE_DIFFUSION_COEFFICIENT: float = 0.651 * 10 ** (-9)
GLUCOSE_DENSITY: float = 1.54 * 10**3  # kg/m³
GLUCOSE_MOLAR_MASS: float = 0.180156  # kg/mol

# Water constants
WATER_DENSITY: float = 1.0 * 10**3  # kg/m³
WATER_THERMAL_CONDUCTIVITY: float = 0.6  # W/m/K
WATER_HEAT_CAPACITY: float = 4.185 * 10**3  # J/K/kg


def computeThermalEnergy(thermal_flux: float) -> float:
    """Returns Q, the thermal energy according to the formula :
    Q = Flux * dt where dt is the time of one iteration of the loop

    Args:
        thermal_flux (float): thermal flux, in W

    Returns:
        float: Q, the thermal energy, in J
    """
    return thermal_flux * TIME_ITERATION


def computeThermalFlux(temperature1: float, temperature2: float) -> float:
    """Computes phi, the thermal flux from temperature1 to temperature2 in
    W/m² according to Fourier's law of thermal diffusion

    Args:
        temperature1 (float): temperature, in K
        temperature2 (float): temperature, in K

    Returns:
        float: thermal flux, in W. Positive if temperature2 > temperature1,
            negative otherwise.
    """
    return -WATER_THERMAL_CONDUCTIVITY * (temperature1 - temperature2)


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
    # Glucose flux computation tests
    print(computeThermalEnergy(5) == 5 * TIME_ITERATION)  # OK
    print(computeGlucoseFlux(5, 5) == 0)  # OK
    print(computeGlucoseFlux(0.001, 0.006) - 5.0127 < 10 ** (-6))  # OK
    print(computeGlucoseFlux(5 * 10 ** (-3), 7 * 10 ** (-3)))
    print(computeThermalFlux(350, 300) == -30)  # OK
