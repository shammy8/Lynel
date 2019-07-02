import pygame
from pygame.sprite import Sprite


class Arrow(Sprite):
    def __init__(self, ai_settings, screen, link):
        """initialises a bomb, inherits from the built in Sprite class"""
        super().__init__()
        self.screen = screen

        #loads image for the arrow and get the information for it to be used by Python
        self.image = pygame.image.load('images/arrow2.png')
        self.rect = self.image.get_rect()
        
        #start the arrow from top of Link's head
        self.rect.centerx = link.rect.centerx
        self.rect.top = link.rect.top

         #float allow more fine tuning of the speed of the arrows
        self.y = float(self.rect.y)
        self.speed_factor = ai_settings.arrow_speed_factor
    

    def update(self):
        #moves the arrows forward
        self.y -= self.speed_factor
        self.rect.y = self.y
    

    def draw_arrow(self):
        #display the arrows on the window
        self.screen.blit(self.image, self.rect)