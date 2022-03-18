# This is the main file of our 'Ecosysteme' project 
# Here is the list of commands needed to save the changes and update the files to Github.com
# git add .
# git commit -m "Ecrire un message résumant les changemets"
# git push  

###########
# MODULES #
###########
import pygame

###########
# MAIN CODE #
###########
pygame.init() # Initiation of pygame -> mandatory
window_edge = 600 # in pixels -> wanted edge size for the display window
main_window = pygame.display.set_mode((window_edge,window_edge)) # Creation of the main window -> size : window_surface x window_surface
    
small_rect = (300, 200, 150, 90) # Datas on size and position of a rectangle  
some_color = (255, 0, 0) # RED for the rectangle
bg_color = (0,200,255) # SKY BLUE for the bg color of our window
    
    
    # Game loop
while True:
    event = pygame.event.poll()
 # Collecting an event from the user 
            
    # The loop (and the code) terminates if the user click on the close button of the window
    if event.type == pygame.QUIT:
        break
        
    main_window.fill(bg_color) # Colouring the window
    main_window.fill(some_color,small_rect) # Colouring a rectangle on the window 
    pygame.display.flip() # Displaying the window
    #pygame.quit() # Closing the window if leaving the loop
    


    