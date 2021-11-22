from board import grid
import pygame

grid.grid_maker()
print(grid.grid)
grid.init()

model = 1 
while model :
    pygame.display.flip()
