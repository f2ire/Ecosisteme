###########
# MODULES #

import pygame
import cell
import data_logger
import environment

#############
# FUNCTIONS #
#############

#############
# MAIN CODE #
#############

# INITIALISATION
pygame.init()  # Initiation of pygame -> mandatory

# CREATION OF THE WINDOW

window_edge = 600  # in pixel
# Creation of the main window -> size : window_surface x window_surface
main_window = pygame.display.set_mode((window_edge, window_edge))
bg_color = (255, 255, 255)  # WHITE for the background color
main_window.fill(bg_color)  # Colouring the window

# CREATION OF THE ENVIRONMENT GRID
cell.Cell.env = environment.Environment(window_edge, window_edge)

# MANAGING CELLS
# Creating a cell in the middle of our window
first_cell = cell.Cell(window_edge // 2, window_edge // 2)
cells_list = [first_cell]
main_window.fill(first_cell.color, first_cell.attributes)

# For displaying the number of cells over time
logger = data_logger.DataLogger(cells_list)

# GAME LOOP
step = 0
while True:
    event = pygame.event.poll()  # Collecting an event from the user
    if event.type == pygame.QUIT:  # End loop if user click on cross butun
        break

    main_window.fill(bg_color)  # Resetting the window blank

    if len(cells_list) == 0:  # If the list is empty we stop the loop
        break

    else:
        for cells in cells_list:
            if cells.isTooOld():
                # Remove cell object and end loop
                cells_list.remove(cells)
                break
            else:
                cells.age += 1
                cells.adapt_color()
                cells.moving()

                if cells.isReplicating():
                    # Add pointer to cell in the cells_list
                    cells_list.append(cells.replication())

            main_window.fill(cells.color, cells.attributes)

    if step % 100 == 0:  # divide by 100 number of data
        logger.counting_cell()

    pygame.display.flip()  # Displaying the window continuously

logger.draw_cell_number_by_time()
# Displaying the graph of the number of cells over time

pygame.quit()  # Closing the window if leaving the loop
