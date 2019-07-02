import pygame
from pygame.sprite import Sprite

class Bomb(Sprite):
    def __init__(self, ai_settings, screen, link):
        """initialises a bomb, inherits from the built in Sprite class"""
        super().__init__()
        self.screen = screen

        #load two images one of the bomb and one of the explosion
        self.image = pygame.image.load('images/mybombchu2.png')
        self.image2 = pygame.image.load('images/bomb_explode_big.png')
        self.rect = self.image.get_rect()
        
        #start the bomb at the top of Link's head
        self.rect.centerx = link.rect.centerx
        self.rect.top = link.rect.top
         
         #float allow more fine tuning of the speed of the bomb
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

        #timer for how long the bomb has been deplyed, set at 0 to begin with
        self.timer = 0
        #direction flag of the bomb 0 for right and 1 for left
        self.bomb_direction = 0


    def update_right(self):
        """moves the bomb right at a 45 degree angle"""
        self.y -= 1
        self.rect.y = self.y
        self.x += 1
        self.rect.x = self.x
    

    def update_left(self):
        """moves the bomb left at a 45 degree angle"""
        self.y -= 1
        self.rect.y = self.y
        self.x -= 1
        self.rect.x = self.x
        
        
    def draw_bomb(self):
        """draw the bomb on the window"""
        self.screen.blit(self.image, self.rect)
        
    