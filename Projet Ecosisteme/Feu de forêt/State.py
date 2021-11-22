from enum import Enum

class State(Enum):
    """
    Differents values corresponding to a state for the cells.
    """
    ALIVE = 0
    BURNING = 1
    DEAD = 2
    LAC = 3
    ROUTE = 4
    ROCK = 5
    VIGNE = 6
    IMMOBILIER = 7
    ASH = 8
