import pygame
from pygame.locals import *
from State import State
import time
import random
class Cell :
    """
    Create a new cell.
    Paramater:
    ----------
    x : int
        Number of columns
    y : int
        Number of lines
    state : 
        State of the cell
    """
    def __init__(self,x :int,y:int,state:int) : 
        self.hp = 1
        self.state = State(state)
        self.x = x
        self.y = y

    def __repr__(self) :
        return str(self.state).split(".")[1]

    def get_color_from_state(self): # rajoute couleur -> State.py pour rajouter l'état
        """
        Return an appropriated color from the actual state.
        """
        if self.state == State.ALIVE : 
            return Color(30,140,5)
        elif self.state == State.BURNING : 
            return Color(255,165,0)
        elif self.state == State.DEAD :
            return Color(50,15,13)
        elif self.state == State.LAC :
            return Color(70,110,220)
        elif self.state == State.ROUTE :
            return Color(129,112,98)
        elif self.state == State.ROCK :
            return Color(71,37,5)
        elif self.state == State.VIGNE :
            return Color(255,67,255)
        elif self.state == State.IMMOBILIER :
            return Color(134,115,21)
        elif self.state == State.ASH :
            return Color(0,0,0)
  
    def draw_square(self,screen,pixel_size:int) :
        """
        Create the design of the cells from the given dimensions.
        """
        pygame.draw.rect(screen,self.get_color_from_state(),Rect(self.x*pixel_size,self.y*pixel_size,pixel_size-0.5,pixel_size-0.5))

    def next_state(self):
        """
        Allows changing states of the cells.
        """
        self.state = State((self.state.value + 1)%len(State))

    def h1_cellburning(self,grid:list,grid_y:int,grid_x:int,wind_y:int,wind_x:int):
        """
        Test the adjacent cells around the cell in the "BURNING" state and modify the states if conditions are met.
        Parameters:
        ----------
        grid : list
            Cells grid
        grid_y : int
            Size of the grid
        grid_x : int
            Width of the grid
        wind_y : int
            Wind force from Y axis
        wind_x : int
            Wind force from X axis
        """
        # print(Game.GRID[y][x].state)
        for y in range(max(0,self.y-1),min(grid_y,self.y+2)):
            for x in range(max(0,self.x-1),min(grid_x,self.x+2)): #pour le vent if x > self.x (ca veux dire cest a droite)
                if grid[y][x].state == State.BURNING or grid[y][x].state == State.DEAD or grid[y][x].state == State.ASH or grid[y][x] == grid[self.y][self.x]:
                    pass
                elif grid[y][x].state == State.ROUTE :
                    if Cell.randomize(1,100000000):
                        grid[y][x].state = State.BURNING
                elif grid[y][x].state == State.IMMOBILIER :
                    grid[y][x].state = State.ASH
                else :
                    if Cell.randomize(1,6):
                        grid[y][x].state = State.BURNING
                    if Cell.randomize(1,3):
                        cell_winded_state = self.h2_wind(grid,grid_y,grid_x,wind_y,wind_x)
                        if cell_winded_state.state == State.ROUTE:
                            if Cell.randomize(1,10):
                                cell_winded_state.state = State.BURNING
                        else :
                            cell_winded_state.state = State.BURNING
        self.state = State.DEAD

    def h2_wind(self,grid,grid_y,grid_x,wind_y,wind_x):
        """
        Return the position of the cell who will catch fire while wind is active.
        Parameter:
        ----------
        grid : list
            Cells grid
        grid_y : int
            Size of the grid
        grid_x : int
            Width of the grid
        wind_y : int
            Wind force from Y axis
        wind_x : int
            Wind force from X axis
        """
        return grid[max(x for x in [self.y,self.y+wind_y] if x < grid_y) if self.y<self.y+wind_y else min(x for x in [self.y,self.y+wind_y] if x >= 0)][max(x for x in [self.x,self.x+wind_x] if x < grid_x) if self.x<self.x+wind_x else min(x for x in [self.x,self.x+wind_x] if x >= 0)]

        # self.state = State(1)

        # if x > 0:
        #     if Game.GRID[y][x-1].state == State.BURNING:
        #         self.state = State(1)
        # if x < Game.GRID_X-1:
        #     if Game.GRID[y][x+1].state == State.BURNING:
        #         self.state = State(1)
        # if y > 0:
        #     if Game.GRID[y-1][x].state == State.BURNING:
        #         self.state = State(1)
        # if y < Game.GRID_Y-1:
        #     if Game.GRID[y+1][x].state == State.BURNING:
        #         self.state = State(1)
        # print(x,y)

    @classmethod
    def fill_grid(cls,grid,grid_y,grid_x) :
        for y in range(grid_y) :
            for x in range(grid_x) : 
                grid[y][x] = Cell(x,y,grid[y][x])


    @staticmethod
    def randomize(nb_chance:int,total:int):
        """
        Return true from probability from "nb_chance/total".
        """
        return random.randint(0,total-1) in range(nb_chance)
