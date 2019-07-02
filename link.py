import pygame
from pygame.sprite import Sprite


class Link():
    """This class control Link's: sprite, movements"""
    def __init__(self, ai_settings, screen):
        """initialise Link"""
        self.screen = screen
        self.ai_settings = ai_settings

        #load image of Link
        self.image = pygame.image.load('images/link.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #put Link at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - 15

        #used to allow Link to be controlled more sensitvely via link_speed_factor
        self.center = float(self.rect.centerx)
        
        #movement flags to say when the left and right keys are hold down for continuous movement
        self.moving_right = False
        self.moving_left = False
    

    def update(self):
        """if movement flags is true and Link is within boundaries of the screen move him accordingly """ 
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.link_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.link_speed_factor
        self.rect.centerx = self.center


    def blitme(self):
        """draw Link onto the screen"""
        self.screen.blit(self.image, self.rect)

    
    def center_link(self):
        """center Link, used after deaths"""
        self.center = self.screen_rect.centerx



class Lifes(Sprite):
    """class used to display the amount of lifes link has left"""
    def __init__(self, ai_settings, screen):
        super().__init__()
        
        self.image = pygame.image.load('images/heart.png')
        self.rect = self.image.get_rect()