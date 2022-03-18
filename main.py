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

###########
# MAIN CODE #
###########

# INITIALISATION
pygame.init() # Initiation of pygame -> mandatory

# CREATION OF THE WINDOW
window_edge = 600 # in pixels -> wanted edge size for the display window
main_window = pygame.display.set_mode((window_edge,window_edge)) # Creation of the main window -> size : window_surface x window_surface
bg_color = (255,255,255) # WHITE for the background color
main_window.fill(bg_color) # Colouring the window

# ADDING A CELL TO THE ENVIRONMENT
first_cell = cell.Cell(window_edge//2,window_edge//2) # Creating a cell in the middle of our window
main_window.fill(first_cell.color,first_cell.attributes)

# GAME LOOP
while True:
    event = pygame.event.poll() # Collecting an event from the user 
            
    # The loop (and the code) terminates if the user click on the close button of the window
    if event.type == pygame.QUIT:
        break
    main_window.fill(bg_color) # Resetting the window blank
    first_cell.moving() # Moving the cell to the right (for now)
    main_window.fill(first_cell.color,first_cell.attributes)
    
    pygame.display.flip() # Displaying the window continuously
    
pygame.quit() # Closing the window if leaving the loop
    


    