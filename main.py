# This is the main file of our 'Ecosysteme' project
# Here is the list of commands needed to save the changes and update the files to Github.com
# git add .
# git commit -m "Ecrire un message résumant les changemets"
# git push 

###########
# MODULES #
###########
import pygame
import time
import cell
import random
import data_logger

#############
# FUNCTIONS #
#############
def isReplicating(cell):
  """
  Returns True if the cell is gonna replicates itselfs.
  """
  # Random number between 0 and 1 -> if < growth_rate then the cell
  # replicates itself
  replication_proba = random.random()

  if replication_proba <= cell.growth_rate:
    return True
    
  else:
    return False


def isTooOld(cell):
  """
  Returns True if the cell's age is equal to it max_age
  """
  if cell.age > cell.max_age:
    return True
  else:
    return False


###########
# MAIN CODE #
###########

# INITIALISATION
pygame.init()  # Initiation of pygame -> mandatory

# CREATION OF THE WINDOW
window_edge = 600  # in pixels -> wanted edge size for the display window
# Creation of the main window -> size : window_surface x window_surface
main_window = pygame.display.set_mode((window_edge, window_edge))
bg_color = (255, 255, 255)  # WHITE for the background color
main_window.fill(bg_color)  # Colouring the window

# MANAGING CELLS
# Creating a cell in the middle of our window
first_cell = cell.Cell(window_edge//2, window_edge//2)
cells_list = [first_cell]
main_window.fill(first_cell.color, first_cell.attributes)

logger = data_logger.DataLogger(cells_list)

# GAME LOOP
i = 0
while True:
  event = pygame.event.poll()  # Collecting an event from the user

  # The loop (and the code) terminates if the user click on the close button
  # of the window
  if event.type == pygame.QUIT:
    break

  main_window.fill(bg_color)  # Resetting the window blank

  for cells in cells_list:
    # Determine if cells shoudl die from age
    if isTooOld(cells): # Yes -> removes the cell from the list and the loop goes directly on the next cell
      cells_list.remove(cells)
      break
    else: # No -> cells is aging, moving and maybe replicating
      # cells is aging
      cells.age += 1

      # cells is moving
      cells.moving() 

      # Determine if cells will be replicating it self
      if isReplicating(cells):
        daugther_cell = cells.replication()
        cells_list.append(daugther_cell)  # Adding the daugther cell to the list
      else:
        pass
    
      
    main_window.fill(cells.color, cells.attributes)

    cells.adapt_color()

    

    
  if i % 100 == 0:
    logger.counting_cell()
  pygame.display.flip()  # Displaying the window continuously

logger.draw_cell_number_by_time()

pygame.quit()  # Closing the window if leaving the loop
