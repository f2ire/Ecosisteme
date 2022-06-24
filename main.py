###########
# MODULES #

import pygame
from cell import Cell
import data_logger
from environment import Environment

#############
# FUNCTIONS #
#############

#############
# MAIN CODE #
#############

# INITIALISATION
pygame.init()  # Initiation of pygame -> mandatory

# CREATION OF THE WINDOW
window_edge = 600  # in pixels
# Creation of the main window -> size : window_surface x window_surface
main_window = pygame.display.set_mode((window_edge, window_edge))
bg_color = (255, 255, 255)  # WHITE for the background color
main_window.fill(bg_color)  # Colouring the window

# CREATION OF THE ENVIRONMENT GRID
world = Environment(window_edge, window_edge) # same dimensions as the window

# MANAGING CELLS
# Creating a cell in the middle of our window and initiating it
first_cell = Cell(world,window_edge // 2, window_edge // 2) ; print(first_cell.occupied_x_coord)
cells_list = [first_cell]
world.usedSpace(first_cell, first_cell.occupied_x_coord, first_cell.occupied_y_coord)
main_window.fill(first_cell.color, first_cell.attributes)

# For displaying the number of cells over time
logger = data_logger.DataLogger(cells_list)

# GAME LOOP
step = 0
while True:
  main_window.fill(bg_color)  # Resetting the window blank
  event = pygame.event.poll()  # Collecting an event from the user
  if event.type == pygame.QUIT:  # End loop if user click on cross butun
    break

  if len(cells_list) == 0:  # If the list is empty we stop the loop
    break

  else:
    for a_cell in cells_list:
      if a_cell.isTooOld():
        # Remove cell object and end loop
        world.usedSpace(a_cell, a_cell.occupied_x_coord, a_cell.occupied_y_coord, delete=True)
        cells_list.remove(a_cell)
        break
      else:
        a_cell.age += 1
        a_cell.adaptColor()
        a_cell.moving(world)
        a_cell.replicating(world,cells_list)
    
        main_window.fill(a_cell.color, a_cell.attributes)

  if step % 100 == 0:  # divide by 100 number of data
    logger.countingCell()

  pygame.display.flip()  # Displaying the window continuously

logger.drawCellNumberByTime()
# Displaying the graph of the number of cells over time

pygame.quit()  # Closing the window if leaving the loop
