import environment_unit


class Environment:
    """
    Class stocking multiple environment_unit
    """

    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.number_columns = round(
            self.width / environment_unit.EnvironmentalUnit.width
        )
        self.number_rows = round(
            self.length / environment_unit.EnvironmentalUnit.length
        )
        self.grid = [
            [
                environment_unit.EnvironmentalUnit(
                    x * environment_unit.EnvironmentalUnit.width,
                    y * environment_unit.EnvironmentalUnit.length,
                )
                for x in range(self.number_columns)
            ]
            for y in range(self.number_rows)
        ]
