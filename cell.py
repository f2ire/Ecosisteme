###########
# MODULES # 
###########
import random
import tools.direction as dir


class Cell:
    """
    The cell object, the fondamental unit of life
    Cells should be capable of moving towards energy&food sources and replicate itself
    A cell is represented as a small square in the environment
    """
    # The dimensions of the cell for the display in the pygame window
    (length, width) = (10, 10)
    birth_color = (255, 102, 0)
    death_color = (0, 12, 255)

    # The number of pixels the cell is capable of moving in one iteration of the game loop
    mvmt_speed = 0.5

    # The number of times the cell replicates itself in one iteration of the game loop
    growth_rate = 1/4000

    # The oldest age a cell can be. This number is chosen randomly between 6000 and 10000 to simulates diversity
    max_age = random.randint(8000,14000)


    def __init__(self, pos_x=0, pos_y=0):
        # The starting position of the cell
        self.x = pos_x
        self.y = pos_y

        # Attributes is in this rectangle tuple format to fit to the pygame.fill() method which fills rectangle objects
        self.attributes = (self.x, self.y, self.width, self.length)

        # When a cell is created, it age is set on 0. The cell is aging over time and it color is changing with it age
        self.age = 0
        self.color = self.birth_color


    def moving(self):
        """
        Makes the cell move randomly (for the moment) in one direction if possible
        """
        random_direction = dir.Direction.get_random_direction()
        self.x += self.mvmt_speed * random_direction[0]
        self.y += self.mvmt_speed * random_direction[1]
        self.attributes = (self.x, self.y, self.length, self.width)

    def isReplicating(self):
        """
        Returns True if the cell replicates itself based on its growth_rate
        """
        # Boolean telling if the cell is gonna replicates itself
        is_replicating = random.random() <= self.growth_rate
        return is_replicating


    def replication(self):
        """
        The cell makes a copy of itself in one direction accessible around it, this method returns the daughter cell.
        """        
        # The daughter cell is made in a random direction around mother cell
        random_direction = dir.Direction.get_random_direction()
        new_x = self.x + 10 * random_direction[0]
        new_y = self.y + 10 * random_direction[1]
        return Cell(new_x, new_y)


    def isTooOld(self):
        """
        Returns True if the cell's age is superior to its max_age
        """
        if self.age > self.max_age:
            return True
        else:
            return False


    def adapt_color(self):
        """
        Linear interpolation to determine the cell's color depending of its age
        """
        alpha = self.age/self.max_age
        self.color = (
            (1-alpha)*self.birth_color[0] + alpha*self.death_color[0],
            (1-alpha)*self.birth_color[1] + alpha*self.death_color[1],
            (1-alpha)*self.birth_color[2] + alpha*self.death_color[2]
        )


#############
# MAIN CODE #
#############
if __name__ == '__main__':
    cell_list = []
    cell1 = Cell(50, 50,)
    cell_list.append(cell1)
    i = 0
    while i < 16000:
        if cell1.replication() != None:
            cell_list.append(cell1.replication())
        else:
            pass
        i += 1
    print(len(cell_list))