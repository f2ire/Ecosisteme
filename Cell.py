import random
from environment.grid.EnvironmentGrid import EnvironmentGrid
from environment.grid.GlucoseGrid import GlucoseGrid
from tools.direction import Direction

# import environment.physical_data as phy


class Cell:
    """Class reprensenting a cellular individual as a colored cube,
    capable of movement and replication.
    The cell's color is changing along with its age.

    Attributes:
    calculus_width (float) : size of the width of the cell in meters
    calculus_length (float): size of the length of the cell in meters
    calculus_height (float): size of the heigth of the cell in meters
    surface (float): surface of one face of the cell in m²
    volume (float) : volume of the cell in m³
    x (float): coordinates along the x axis of the cell
    y (float): coordinates along the y axis of the cell
    display_x (float): coordinate along the x axis used to display the cell on the pygame window
    display_y (float): coordinate along the Y axis used to display the cell on the pygame window
    ending_x (float): coordinate along the x axis of bottom right corner of the cell
    ending_y (float): coordinate along the y axis of bottom right corner of the cell
    birth_color (tuple): RGB tuple of the starting color of the cell, when the cell's age is 0
    color (tuple): actual RBG tuple of the cell's color
    death_color (tuple): RGB tuple the cell is closing by when it's aging
    width (int): size of the width of the cell in the pygame window in pixels
    length (int) : size of the length of the cell in the pygame window in pixels
    display_rect (tuple): contains the information for a cell to be displayed on a pygame window,
      in this format ; (x, y, width, length)
    speed (float): speed of the cell in pixel.loop⁻¹.
    replication_rate (float): probability of the cell to replicate in one iteration of the game loop
    age (int): actual age of the cell or the number of loops it has been living
    max_age (int): maximal age the cell can be
    """

    calculus_width: float = 1 * 10 ** (-6)  # m
    calculus_length: float = 1 * 10 ** (-6)  # m
    calculus_heigth: float = 1 * 10 ** (-6)  # m

    surface: float = 6 * calculus_width * calculus_length  # m²
    volume: float = calculus_width * calculus_length * calculus_heigth  # m³

    width: int = 20  # pixels
    length: int = 20  # pixels

    x: float
    y: float
    display_x: float
    display_y: float
    ending_x: float
    ending_y: float

    birth_color: tuple = (0, 12, 255)
    color: tuple = birth_color
    death_color: tuple = (0, 0, 0)
    display_rect: tuple

    speed: float = 5  # pixels.loop⁻¹

    replication_rate: float = 1 / 1000

    age: int = 0
    max_age: int = 6000  # loops

    energy: int

    glucose_tolerance: float = 1  # betwenn 0 and 1
    glucose_permeability: float = 1  # between 0 and 1

    def __init__(
        self, environment: EnvironmentGrid, pos_x: float = 0, pos_y: float = 0
    ):
        # The starting position of the cell
        self.x = pos_x
        self.y = pos_y
        self.display_x = pos_x
        self.display_y = pos_y

        self.ending_x = self.x + self.width
        self.ending_y = self.y + self.length

        environment.changeMultipleOccupationStates(
            (self.x, self.y),
            (self.x + self.width, self.y + self.length),
            True,
        )

        self.display_rect = (self.x, self.y, self.width, self.length)

    def __str__(self) -> str:
        string = f"Cell's age is : {self.age} loops\n"
        string += f"Its color in RGB encoding is {self.color}\n"
        return string

    def isReplicationPossible(self) -> bool:
        """Takes a random number between 0 and 1 and checks if it is lower than the replication rate of the cell

        Returns:
          bool: True if the cell is randomly capable of replicating itself
        """
        return random.random() <= self.replication_rate

    def deleteCellFromEnvironment(self, environment: EnvironmentGrid) -> None:
        """Change every Environment units' is_occupied attribute the cell is currently lying over
        on False

        Args:
            environment (EnvironmentGrid): object of class EnvironmentGrid
        """
        environment.changeMultipleOccupationStates(
            (self.x, self.y), (self.ending_x, self.ending_y), False
        )

    def addCellOnEnvironment(self, environment: EnvironmentGrid) -> None:
        """Change every Environment units' is_occupied attribute the cell is currently lying over
        on True

        Args:
            environment (EnvironmentGrid): object of class EnvironmentGrid
        """
        environment.changeMultipleOccupationStates(
            (self.x, self.y), (self.ending_x, self.ending_y), True
        )

    def convertGlucoseIntoEnergy(self, mass_glucose: float):
        """_summary_

        Args:
            mass_glucose (float): _description_
        """
        self.energy

    def moving(self, environment: EnvironmentGrid, direction: tuple = ()) -> None:
        """
        This method makes the cell move in a random direction, after checking if
        the environment in the direction isn't occupied by others cells
        The new coordinates are changed directly using UpdateSpace()
        Args :
            environment (Environment): an object of the instance Environment from
                the environment.py module
            direction (tuple): tuple containing the x and y coordinates of the movement
        """
        if direction == ():
            direction = Direction.getRandomDirection()
        else:
            pass

        self.deleteCellFromEnvironment(environment)

        # Compute the potential coordinates of the cell
        x_movement = self.speed * direction[0]
        y_movement = self.speed * direction[1]

        is_space_for_moving = environment.isSpace(
            (self.x, self.y), (self.ending_x, self.ending_y), (x_movement, y_movement)
        )

        # print("The cell is moving : ", is_space_for_moving)

        if is_space_for_moving:
            self.x += x_movement
            self.y += y_movement
            self.display_x = (self.display_x + x_movement) % environment.width
            self.display_y = (self.display_y + y_movement) % environment.length
            self.ending_x += x_movement
            self.ending_y += y_movement

            self.display_rect = (
                self.display_x,
                self.display_y,
                self.width,
                self.length,
            )

        self.addCellOnEnvironment(environment)

    def replicating(self, environment: EnvironmentGrid):
        """
        Add a new cell to cells_list if their is enough space to create it.
        Args :
          environment (EnvironmentGrid): an object of the instance Environment from the environment.py module
          cells_list (list): the list of all the cells of our environment
        """
        if self.isReplicationPossible():
            random_direction = Direction.getRandomReplicationDirection()
            # print("rdm dir :",random_direction)
            needed_replication_space = (
                self.width * random_direction[0],
                self.length * random_direction[1],
            )
            is_space_for_replication = environment.isSpace(
                (self.x, self.y),
                (self.ending_x, self.ending_y),
                needed_replication_space,
            )
            # print("is_space :",is_space)
            if is_space_for_replication:
                return Cell(
                    environment,
                    self.x + self.width * random_direction[0],
                    self.y + self.length * random_direction[1],
                )
            else:
                pass
        else:
            pass
        return None

    def isTooOld(self) -> bool:
        """
        Returns True if the cell's age is superior to its max_age
        """
        if self.age > self.max_age:
            return True
        else:
            return False

    def adaptColor(self) -> None:
        """
        Linear interpolation to determine the cell's color depending of its age
        """
        alpha = self.age / self.max_age
        self.color = (
            (1 - alpha) * self.birth_color[0] + alpha * self.death_color[0],
            (1 - alpha) * self.birth_color[1] + alpha * self.death_color[1],
            (1 - alpha) * self.birth_color[2] + alpha * self.death_color[2],
        )
        return None


if __name__ == "__main__":
    enviro = EnvironmentGrid(10, 10)
    cell1 = Cell(enviro)
    cell2 = Cell(enviro, 25.45, 0)
    print(cell1)  # OK
    print(enviro)  # OK

    # Age test
    cell1.age = 7000
    print(cell1.isTooOld())  # OK

    # Movements and collision tests
    for i in range(10):
        cell1.moving(enviro, (1, 0))
        print(
            f"Cell 1 from ({cell1.x % 50}, {cell1.y % 50}) to ({cell1.ending_x % 50}, {cell1.ending_y % 50})"
        )
        print(
            f"Cell 2 from ({cell2.x % 50}, {cell2.y % 50}) to ({cell2.ending_x % 50}, {cell2.ending_y % 50})"
        )
        print(enviro)
