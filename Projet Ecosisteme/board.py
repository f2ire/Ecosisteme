import pygame

class grid:
    """
    Class which give all atributes for the map
    """
    grid = [[]]
    grid_dimension = {"x":50,"y":50}
    window_parameter = {
        "window":None,
        "background":None,
        "length":0,
        "width":0,
        "pixel_size":5
        }

    @classmethod
    def grid_maker(cls):
        """
        Create a grid with class dimension.
        """
        cls.grid = [["lol" for i in range(cls.grid_dimension["y"])] for j in range(cls.grid_dimension["x"])]

    @classmethod
    def init(cls):
        """
        Initialisation of the window
        """
        cls.window_parameter["length"]=cls.grid_dimension["y"]*cls.window_parameter["pixel_size"]
        cls.window_parameter["width"]=cls.grid_dimension["x"]*cls.window_parameter["pixel_size"]
        pygame.init()
        cls.window_parameter["screen"] = pygame.display.set_mode((cls.window_parameter["width"],cls.window_parameter["length"])) #arg 1 = tuple
        # pygame.display.set_caption("test")
        bg = pygame.Surface(cls.window_parameter["screen"].get_size())
        cls.window_parameter["background"] = bg.convert()
        cls.window_parameter["background"].fill((33,23,12))
        cls.window_parameter["screen"].blit(cls.window_parameter["background"], (0,0))

