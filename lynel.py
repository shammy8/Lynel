import pygame
from pygame.sprite import Sprite

class Lynel(Sprite):

    def __init__(self, ai_settings, screen):
        """initialises a lynel, inherits from the built in Sprite class"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #loads image for the lynel and get the information for it to be used by Python
        self.image = pygame.image.load('images/enemies.png')
        self.rect = self.image.get_rect()

        #used to move the lynel closer the the edge
        self.rect.x = self.rect.width #/ 4 
        self.rect.y = self.rect.height #/ 4

        #float allow more fine tuning of the speed of the lynels
        self.x = float(self.rect.x)


    def blitme(self):
        #draw the lynels to the screen
        self.screen.blit(self.image, self.rect)


    def check_edges(self):
        #return True if the lynels are touching or outside the window
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True


    def update(self):
        #move the lynels left and right
        self.x += self.ai_settings.lynel_speed_factor * self.ai_settings.horde_direction
        self.rect.x = self.x