import pygame
from pygame.locals import *
from Cell import Cell
from State import State 
import json
import os
from Button import *
import tkinter.filedialog

class Game :
    """
    Class who will give all the atributes for the game.
    """
    isin_placing_phase:bool = True
    isin_maping_phase:bool = False
    screen = None
    background = None
    grid = [[]]
    grid_x = 100
    grid_y = 100
    pixel_size = 5
    screen_width = 0
    screen_height = 0
    wind_y = 4 # 0 -> no wind, negative -> power of north wind, positive -> power of south wind
    wind_x = -1 # 0 -> no wind, negative -> power of west wind, positive -> power of east wind
    time = 400

    @classmethod
    def init(cls):
        """
        Game initialisation
        """
        print("Do you want to load a pre-existing map ?")
        if cls.is_yes():
            dico_or_nothing = None
            while dico_or_nothing == None:
                dico_or_nothing = cls.chosing_map()
            dico = dico_or_nothing
            cls.grid = dico['map']
            cls.pixel_size = dico['pixel_size']
            cls.grid_x = len(dico['map'][0])
            cls.grid_y = len(dico['map'])
            cls.screen_width = cls.grid_x * cls.pixel_size
            cls.screen_height = cls.grid_y * cls.pixel_size
            print("Do you want to personalize the wind effect ?")
            if cls.is_yes():
                cls.input_wind()
        else :
            print("Do you want to personalize the wind effect ?")
            if cls.is_yes():
                cls.input_wind()
            cls.grid = cls.grid_maker()
            cls.screen_width = cls.grid_x * cls.pixel_size
            cls.screen_height = cls.grid_y * cls.pixel_size
        Cell.fill_grid(cls.grid,cls.grid_y,cls.grid_x)

        # if test():
        #     dico = cls.chosing_map()
        #     cls.grid = dico['map']
        #     cls.pixel_size = dico['pixel_size']
        #     cls.grid_x = len(dico['map'][0])
        #     cls.grid_y = len(dico['map'])
        #     cls.screen_width = cls.grid_x * cls.pixel_size
        #     cls.screen_height = cls.grid_y * cls.pixel_size
        # else :
        #     cls.grid = cls.grid_maker()
        #     cls.screen_width = cls.grid_x * cls.pixel_size
        #     cls.screen_height = cls.grid_y * cls.pixel_size
        # Cell.fill_grid(cls.grid,cls.grid_y,cls.grid_x)        

        pygame.init()
        cls.screen = pygame.display.set_mode((cls.screen_width,cls.screen_height))
        pygame.display.set_caption('Fire wave simulation')
        # Fill background
        background = pygame.Surface(cls.screen.get_size())
        cls.background = background.convert()
        background.fill((0, 0, 0))
        cls.screen.blit(background, (0, 0))

    @classmethod
    def update(cls):
        """
        Test all events send from user.
        """
        events = pygame.event.get()
        for event in events :
            if event.type == pygame.QUIT :
                return False
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE :
                    cls.isin_maping_phase = True
                if event.key == pygame.K_UP : 
                    cls.time += -50
                if event.key == pygame.K_DOWN :
                    cls.time += 50
                if event.key == pygame.K_p :
                    input("Write anything to resume : ")
        if cls.isin_maping_phase :
            cls.map_phasing()        
        if cls.isin_placing_phase :
            cls.placing_phase(events)
        else : 
             cls.burning_phase(events)
        cls.draw_grid()
        return True

    @classmethod
    def draw_grid(cls):
        """
        Draw a new visual grid from class's parameters.
        """
        cls.screen.blit(cls.background, (0,0))
        for y in range(cls.grid_y) :
            for x in range(cls.grid_x) : 
                cls.grid[y][x].draw_square(cls.screen,cls.pixel_size)

    @classmethod
    def map_phasing(cls):
        """
        Allows to save a grid in a .txt file.
        """
        grid_save = cls.grid_maker()
        for y in range(cls.grid_y) :
            for x in range(cls.grid_x) : 
                grid_save[y][x] = cls.grid[y][x].state.value
        with open(f"""{os.path.dirname(os.path.realpath(__file__))}/map/{input("Nom de la carte : ")}.txt""","w") as fichier :
            json.dump({"map":grid_save,"pixel_size":cls.pixel_size},fichier)
        cls.isin_maping_phase = False

    @classmethod
    def placing_phase(cls,events:list):
        """
        Allows user to change the state of each cells by clicking on it.
        """
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                clic_pos = pygame.mouse.get_pos()
                pos_cell = (clic_pos[0]//cls.pixel_size,clic_pos[1]//cls.pixel_size)
                cell = cls.grid[pos_cell[1]][pos_cell[0]]
                cell.next_state()
            elif event.type == pygame.KEYDOWN :
                if event.key == pygame.K_RETURN :
                    cls.isin_placing_phase = False
    
    @classmethod
    def burning_phase(cls,events:list):
        """
        Test all the cells from the grid, take into account the "BURNING" state.
        """
        # old_grid = grid_maker(GRID_Y,GRID_X)
        burning_list = []
        for y in range(cls.grid_y):
            for x in range(cls.grid_x):
                if cls.grid[y][x].state == State.BURNING :
                    burning_list.append(cls.grid[y][x])
        for cell_burning in burning_list:
            cell_burning.h1_cellburning(cls.grid,cls.grid_y,cls.grid_x,cls.wind_y,cls.wind_x)
        pygame.time.delay(cls.time)
                # new_state = 
                # old_grid[y][x] = new_state
        # for y in range(GRID_Y):
        #     for x in range(GRID_X):
    

    @classmethod
    def grid_maker(cls):
        """
        Create a grid.
        """
        return [[0 for j in range(cls.grid_x)] for i in range(cls.grid_y)]
    
    @classmethod
    def input_wind(cls):
        """
        Allows user to choose the wind values.
        """
        try : 
            value_wind_y = int(input("""Choose a int number between -5 and 5 to gave a value for the wind force / direction on a North/South axis.
0 corresponds to no wind.\nPositif values are power toward south.\nNegatives toward north \n ... """))
            if value_wind_y not in range(-5,6):
                cls.input_wind()
            else : 
                cls.wind_y = value_wind_y
        except :
            print("Please choose a integer between -5 et 5.")
            cls.input_wind()
        try : 
            value_wind_x = int(input("""Choose a int number between -5 and 5 to gave a value for the wind force / direction on a East/West axis.
0 corresponds to no wind.\nPositif values are power toward east.\nNegatives toward west \n ... """))
            if value_wind_x not in range(-5,6):
                cls.input_wind()
            else :
                cls.wind_x = value_wind_x
        except :
            print("Please choose a integer between -5 et 5.")
            cls.input_wind()



    @staticmethod
    def chosing_map():
        """
        Allow to choose a pre-saved grid.
        """
        path_file = tkinter.filedialog.askopenfilename(title="Open the folder:",initialdir=f"""{os.path.dirname(os.path.realpath(__file__))}/map""")  
        try :
            with open(f"""{path_file}""","r") as fichier :
                grid = json.load(fichier)
            return grid
        except : 
            print("Thanks to chose a valid file.")
            return None
    
    @staticmethod
    def is_yes():
        """
        Return True if user say "Yes".
        """
        test = input("(y/n) : ").lower()
        if test not in ('y','n') :
            while test not in ('y','n') :
                print("""Please write only a "y" for yes, and a "n" for no""")
                test = input("(y/n) : ").lower()
        return test == 'y'



