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
env = Environment(window_edge, window_edge) # same dimensions as the window

# MANAGING CELLS
# Creating a cell in the middle of our window and initiating it
first_cell = Cell(env,window_edge // 2, window_edge // 2) ; print(first_cell.occupied_x_coord)
cells_list = [first_cell]
env.UsedSpace(first_cell, first_cell.occupied_x_coord, first_cell.occupied_y_coord)
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
    for c in cells_list:
      if c.IsTooOld():
        # Remove cell object and end loop
        env.UsedSpace(c, c.occupied_x_coord, c.occupied_y_coord, delete=True)
        cells_list.remove(c)
        break
      else:
        c.age += 1
        c.AdaptColor()
        c.Moving(env)
        c.Replicating(env,cells_list)
    
        main_window.fill(c.color, c.attributes)

  if step % 100 == 0:  # divide by 100 number of data
    logger.counting_cell()

  pygame.display.flip()  # Displaying the window continuously

logger.draw_cell_number_by_time()
# Displaying the graph of the number of cells over time

pygame.quit()  # Closing the window if leaving the loop
