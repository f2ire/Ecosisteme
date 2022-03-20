# This is the main file of our 'Ecosysteme' project
# Here is the list of commands needed to save the changes and update the files to Github.com
# git add .
# git commit -m "Ecrire un message résumant les changemets"
# git push 

###########
# MODULES #
###########
import pygame
import cell
import environment
import data_logger

#############
# FUNCTIONS #
#############
def makeEnvironmentGrid(length,width):
    """
    Creates and returns a list of size length, containing lists of size width
    length and width should be integers
    """
    # The grid
    environment_grid = []
    for i in range(length):
        row = []
        for j in range(width):
            row.append(environment.environmental_unit(i,j))
            j += 1
        environment_grid.append(row)
        i += 1
    
    return environment_grid

#############
# MAIN CODE #
#############

# INITIALISATION
pygame.init()  # Initiation of pygame -> mandatory

# CREATION OF THE WINDOW
window_edge = 600  # in pixels -> wanted edge size for the display window
# Creation of the main window -> size : window_surface x window_surface
main_window = pygame.display.set_mode((window_edge, window_edge))
bg_color = (255, 255, 255)  # WHITE for the background color
main_window.fill(bg_color)  # Colouring the window

# CREATION OF THE ENVIRONMENT GRID
environment_grid = makeEnvironmentGrid(window_edge,window_edge) 

# MANAGING CELLS
# Creating a cell in the middle of our window
first_cell = cell.Cell(window_edge//2, window_edge//2)
cells_list = [first_cell]
main_window.fill(first_cell.color, first_cell.attributes)

# For displaying the number of cells over time
logger = data_logger.DataLogger(cells_list)

# GAME LOOP
i = 0
while True:
  event = pygame.event.poll()  # Collecting an event from the user

  # The loop (and the code) terminates if the user click on the close button of the window
  if event.type == pygame.QUIT:
    break

  main_window.fill(bg_color)  # Resetting the window blank
  
  # If the list is empty we stop the loop
  if len(cells_list) == 0:
    break
  else:
    for cells in cells_list:
    # Determine if cells should die from age
        if cells.isTooOld(): # Yes -> removes the cell from the list and the loop goes directly on the next cell
            cells_list.remove(cells)
            break
        else: # No -> cells is aging, moving and maybe replicating
            # cells is aging
            cells.age += 1

            # cells is moving
            cells.moving() 

            # cells might replicates itself
            if cells.isReplicating():
                cells_list.append(cells.replication())
            else:
                pass

            # cells is changing color as a function of it age
            cells.adapt_color()

        main_window.fill(cells.color, cells.attributes)

    
  if i % 100 == 0:
    logger.counting_cell()

  pygame.display.flip()  # Displaying the window continuously

logger.draw_cell_number_by_time() # Displaying the graph of the number of cells over time

pygame.quit()  # Closing the window if leaving the loop
