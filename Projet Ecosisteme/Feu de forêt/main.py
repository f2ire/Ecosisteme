from typing import List
import pygame
from Game import Game
from Button import *

Game.init()
# Event loop
keepplaying = 1
while keepplaying == 1:
    keepplaying = Game.update()
    pygame.display.flip()
# print(GRID)
