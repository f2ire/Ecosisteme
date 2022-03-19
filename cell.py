###########
# MODULES #
###########
import random


class Cell:
    """
    The cell object, the fondamental unit of life
    Cells should be capable of moving towards energy&food sources and replicate itself 
    A cell is represented as a small blue square in the environment
    """
    # The dimensions of the cell for the display in the pygame window ->
    # a small blue square of 10x10 pixels
    (length, width) = (10, 10)
    color = (0, 0, 255)

    # The number of pixels the cell is capable of moving in one iteration of the game loop
    mvmt_speed = 0.1
    # The number of times the cell replicates itself in one iteration of the game loop
    growth_rate = 0.0001

    def __init__(self, pos_x=0, pos_y=0):
        # The starting position of the cell
        self.x = pos_x
        self.y = pos_y
        # Attributes is in this rectangle tuple format to fit to the pygame.fill() method which fills rectangle objects
        self.attributes = (self.x, self.y, self.length, self.width)

    def moving(self):
        """
        Makes the cell move randomly (for the moment) in one direction if possible
        """
        random_direction = random.randint(
            0, 3)  # Chosing the direction between 4 possibilities -> north, south, east and west
        if random_direction == 0:  # The cell go north
            self.y -= self.mvmt_speed
        if random_direction == 1:  # The cell go south
            self.y += self.mvmt_speed
        if random_direction == 2:  # The cell go east
            self.x += self.mvmt_speed
        if random_direction == 3:  # The cell go south
            self.x -= self.mvmt_speed
        self.attributes = (self.x, self.y, self.length, self.width)

    def replication(self):
        """
        The cell makes a copy of itself in one direction accessible around it, this method returns the daughter cell. 
        The number of copy realised is defined by the growth rate.
        """

        # The daughter cell is made in a random direction around mother cell
        random_direction = random.randint(0, 3)
        # Daughter cell is made on top of the mother cell
        if random_direction == 0:
            return Cell(self.x, self.y-10)
         # Daughter cell is made on the bottom of the mother cell
        if random_direction == 1:
            return Cell(self.x, self.y+10)
        # Daughter cell is made on the right of the mother cell
        if random_direction == 2:
            return Cell(self.x+10, self.y)
        # Daughter cell is made on the left of the mother cell
        if random_direction == 3:
            return Cell(self.x-10, self.y)


###########
# MAIN CODE #
###########
if __name__ == '__main__':
    cell1 = Cell(50, 50,)
    for i in range(50):
        cell1.moving()
        print(cell1.attributes)
