###########
# MODULES #
###########
import math
import random
import environment
from tools.direction import Direction

####################
# CLASS DEFINITION #
####################
class Cell:
    """
    Cell object is the fondamental unit of life
    Cells should be capable of moving towards energy&food sources
    and replicate itself. It has some basic attributs
    A cell is represented as a small square in the environment
    localized by his coordonates
    """

    # Visual caracteristic
    length: int = 10
    width: int = 10
    birth_color: tuple = (255, 102, 0)
    death_color: tuple = (0, 12, 255)

    # Cell parameter
    mvmt_speed: float = 3

    # The number of times the cell replicates itself in one iteration of the
    # game loop
    growth_rate: float = 1 / 3500

    # This number is chosen randomly between 6000 and 10000 for diversity
    max_age: int = random.randint(6000, 10000)

    # Square in the Environment grid used by the cell
    occupied_x_coord: list = []
    occupied_y_coord: list = []

    env: environment.Environment = None

    
    def __init__(self, pos_x: int = 0, pos_y: int = 0):
        # The starting position of the cell
        self.x: int = pos_x
        self.y: int = pos_y

        # Initialization of the space used by the cell
        self.UsedSpace()
        
        
        self.unit_pos = None

        self.updatePosIntoEnvironment()

        # Attributes is in this rectangle tuple format to fit
        # to the pygame.fill() method which fills rectangle objects
        self.attributes = (self.x, self.y, self.width, self.length)

        # When a cell is created, it age is set on 0. The cell
        #  is aging over time and it color is changing with it age
        self.age = 0
        self.color = Cell.birth_color


    def __repr__(self) -> str:
        return f"Cell at ({self.x}, {self.y}) is {'' if self in self.unit_pos.cell_list else 'not'} cell_list"
    
    ###########
    # METHODS #
    ########### 
    def UsedSpace(self) -> None:
        """
        A cell is using a certain surface of the terrain -> width x length square
        The method keeps track of the surface used by the cell in the environment grid by updating the occupied coordonates in 2 lists :
        occupied_x_coord and occupied_y_coord
        """
        # Pygame creates a square from it top-right hand corner -> we start from posx and posy
        self.occupied_x_coord = [x for x in range(self.x, self.x + self.width)]
        self.occupied_y_coord = [y for y in range(self.y, self.y + self.length)]
        return None


    def Moving(self) -> None:
        """
        This method makes the cell move in a random direction, 
        after checking if the environment in the direction isn't occupied by others cells
        The new coordinates are 
        """
        # Computes the potential coordonates of the cell
        random_direction = Direction.get_random_direction()
        movement_size: tuple = ((self.mvmt_speed * random_direction[0]),
                                (self.mvmt_speed * random_direction[1]))

        if self.env.IsSpaceForMoving(random_direction):
            self.x += movement_size[0]  % Cell.env.width
            self.y += movement_size[1]  % Cell.env.length
            self.attributes = (self.x, self.y, self.length, self.width)
            self.UpdatePosIntoEnvironment()
        else: pass # The cell don't move if the space is occupied
        return None


    def UpdatePosIntoEnvironment(self) -> None:
        if self.unit_pos is not None:
            self.unit_pos.cell_del(self)
        self.unit_pos = Cell.env.grid[math.floor(self.y / self.length)][
            math.floor(self.x / self.width)
        ]
        self.unit_pos.cell_insert(self)
        return None

    
    def Die(self):
        self.unit_pos.cell_list.remove(self)
        return None


    def IsReplicating(self) -> bool:
        """
        Returns True if the cell replicates itself based on its growth_rate
        """
        is_replicating = random.random() <= self.growth_rate
        return is_replicating


    def Replication(self):
        """
        The cell makes a copy of itself in one direction accessible around it,
        this method returns the daughter cell.
        """
        random_direction = Direction.get_random_direction()
        new_x = self.x + 10 * random_direction[0]
        new_y = self.y + 10 * random_direction[1]
        return Cell(new_x, new_y)


    def IsTooOld(self) -> bool:
        """
        Returns True if the cell's age is superior to its max_age
        """
        if self.age > self.max_age:
            return True
        else:
            return False

    def AdaptColor(self) -> None:
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


#############
# MAIN CODE #
#############
if __name__ == "__main__":
    cell_list = []
    cell1 = Cell(
        50,
        50,
    )
    cell_list.append(cell1)
    i = 0
    while i < 16000:
        if cell1.replication() is not None:
            cell_list.append(cell1.replication())
        else:
            pass
        i += 1
    print(len(cell_list))
