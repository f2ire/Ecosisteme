###########
# MODULES #
###########
import random
import tools.direction as dir


class Cell:
    """
    The cell object, the fondamental unit of life
    Cells should be capable of moving towards energy&food sources and replicate itself
    A cell is represented as a small blue square in the environment
    """
    # The dimensions of the cell for the display in the pygame window ->
    # a small blue square of 10x10 pixels
    (length, width) = (10, 100)
    birth_color = (255, 102, 0)
    death_color = (0, 12, 255)

    # The number of pixels the cell is capable of moving in one iteration of the game loop
    mvmt_speed = 2
    # The number of times the cell replicates itself in one iteration of the game loop
    growth_rate = 1/4000

    def __init__(self, pos_x=0, pos_y=0):
        # The starting position of the cell
        self.x = pos_x
        self.y = pos_y
        # Attributes is in this rectangle tuple format to fit to the pygame.fill() method which fills rectangle objects
        self.age = 0
        self.color = self.birth_color
        self.attributes = (self.x, self.y, self.length, self.width)

    def moving(self):
        """
        Makes the cell move randomly (for the moment) in one direction if possible
        """
        random_direction = dir.Direction.get_random_direction()
        self.x += self.mvmt_speed * random_direction[0]
        self.y += self.mvmt_speed * random_direction[1]
        self.attributes = (self.x, self.y, self.length, self.width)

    def replication(self):
        """
        The cell makes a copy of itself in one direction accessible around it, this method returns the daughter cell.
        The number of copy realised is defined by the growth rate.
        """
        # The daughter cell is made in a random direction around mother cell
        random_direction = dir.Direction.get_random_direction()
        new_x = self.x + 10 * random_direction[0]
        new_y = self.y + 10 * random_direction[1]
        return Cell(new_x, new_y)

    def adapt_color(self):
        """
        Linear interpolation to determine the cell's color depends of age
        """
        alpha = self.age/5000
        self.color = (
            (1-alpha)*self.birth_color[0] + alpha*self.death_color[0],
            (1-alpha)*self.birth_color[1] + alpha*self.death_color[1],
            (1-alpha)*self.birth_color[2] + alpha*self.death_color[2]
        )


        ###########
        # MAIN CODE #
        ###########
if __name__ == '__main__':
    cell1 = Cell(50, 50,)
    for i in range(50):
        cell1.moving()
        print(cell1.attributes)
