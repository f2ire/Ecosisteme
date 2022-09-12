import pygame
from World import World
from Cell import Cell
import tools.data_logger as data_logger

# INITIALISATION
pygame.init()  # Initiation of pygame -> mandatory

# CREATION OF THE WINDOW
world_side = 500

# CREATION OF THE ENVIRONMENT GRID
the_world = World(world_side)

main_window = pygame.display.set_mode(the_world.pixel_dimensions)

main_window.fill(the_world.bg_color)

# MANAGING CELLS
# Creating a cell in the middle of our window and initiating it
first_cell = Cell(the_world.environment_grid, 250, 250)
the_world.addCellToList(first_cell)

main_window.fill(first_cell.color, first_cell.display_rect)

# For displaying the number of cells over time
logger = data_logger.DataLogger(the_world.cells_list)

# GAME LOOP
step = 0
while True:
    main_window.fill(the_world.bg_color)  # Resetting the window blank
    event = pygame.event.poll()  # Collecting an event from the user
    if event.type == pygame.QUIT:  # End loop if user click on cross butun
        break

    if len(the_world.cells_list) == 0:  # If the list is empty we stop the loop
        break

    else:
        for a_cell in the_world.cells_list:
            if a_cell.isTooOld():
                # Remove cell object and end loop
                a_cell.deleteCellFromEnvironment(the_world.environment_grid)
                the_world.removeCellFromList(a_cell)
                break

            else:
                a_cell.age += 1
                a_cell.adaptColor()

                a_cell.deleteCellFromEnvironment(the_world.environment_grid)
                a_cell.moving(the_world.environment_grid)

                potential_cell = a_cell.replicating(the_world.environment_grid)
                if isinstance(potential_cell, Cell):
                    the_world.addCellToList(potential_cell)
                else:
                    pass

                a_cell.addCellOnEnvironment(the_world.environment_grid)

                main_window.fill(a_cell.color, a_cell.display_rect)

    if step % 100 == 0:  # divide by 100 number of data
        logger.countingCell()

    pygame.display.flip()  # Displaying the window continuously

logger.drawCellNumberByTime()
# Displaying the graph of the number of cells over time

pygame.quit()  # Closing the window if leaving the loop
