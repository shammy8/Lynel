import pygame


class Settings():

    def __init__(self):
        self.screen_width = 1024
        self.screen_height = 768

        pygame.mixer.music.load("sounds/Palace.mp3")

        pygame.display.set_mode((self.screen_width, self.screen_height))
        self.background = pygame.image.load("images/background1.png").convert()

        #speed factor controls the speed of Link and amount of lifes per game
        self.link_speed_factor = 1
        self.link_lifes = 3

        #speed of arrows and number of arrows allowed on screen
        self.arrow_speed_factor = 1
        self.arrows_allowed = 2

        #the direction of lynels left or right, base points each lynel is worth, how fast the lynels increases each level
        self.horde_direction = 1
        self.lynel_points = 10
        self.speedup_scale = 0.05 

        #amount of bombs allowed at once, time it takes to explode, distance in the y direction they travel and how long the hitbox is out for
        self.bomb_limit = 1
        self.bomb_duration = 2000
        self.bomb_distance = 250
        self.bomb_hitbox_duration = 150

        self.initialize_dynamic_settings(1)


    def initialize_dynamic_settings(self, level):
        """settings that change each level"""
        lynel_speed_factor_levels = [0.5, 0.5, 0.5, 0.7, 0.7, 0.7, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9] #how fast lynels move left left and right for up to level 12
        horde_drop_speed_levels = [10, 10, 10, 10, 10, 10, 10, 10, 10, 20, 20, 20] #how far the lynels move down for up to level 12
        no_of_rows_levels = [2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 3, 4] #number of rows of lynels for up to level 12
        self.lynel_speed_factor = lynel_speed_factor_levels[level-1]
        self.horde_drop_speed = horde_drop_speed_levels[level -1]
        self.no_of_rows = no_of_rows_levels[level-1]


    def increase_speed(self):
        """increase the speed of the lynels"""
        self.lynel_speed_factor += self.speedup_scale
        