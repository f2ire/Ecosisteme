import pygame
from world import World
from cell import Cell
import tools.data_logger as data_logger

# INITIALISATION
pygame.init()  # Initiation of pygame -> mandatory

# CREATION OF THE WINDOW
world_width: int = 50  # number of units of the world's width
world_length: int = 50  # number of units of the world's length

# CREATION OF THE ENVIRONMENT GRID
the_world = World(world_width, world_length)

main_window = pygame.display.set_mode(the_world.display_tuple)
bg_color = (255, 255, 255)
main_window.fill(bg_color)

# MANAGING CELLS
# Creating a cell in the middle of our window and initiating it
first_cell = Cell(the_world.environment_grid)
cells_list = [first_cell]

main_window.fill(first_cell.color, first_cell.display_tuple)

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
                the_world.environment_grid.changeMultipleOccupationStates(
                    a_cell.occupied_x_coord, a_cell.occupied_y_coord, False
                )
                cells_list.remove(a_cell)
                break

            else:
                a_cell.age += 1
                a_cell.adaptColor()

                a_cell.deleteCellFromEnvironment(the_world.environment_grid)
                a_cell.moving(the_world.environment_grid)

                potential_cell = a_cell.replicating(the_world.environment_grid)
                if isinstance(potential_cell, Cell):
                    cells_list.append(potential_cell)
                else:
                    pass

                a_cell.addCellOnEnvironment(the_world.environment_grid)

                main_window.fill(a_cell.color, a_cell.display_tuple)

    if step % 100 == 0:  # divide by 100 number of data
        logger.countingCell()

    pygame.display.flip()  # Displaying the window continuously

logger.drawCellNumberByTime()
# Displaying the graph of the number of cells over time

pygame.quit()  # Closing the window if leaving the loop
