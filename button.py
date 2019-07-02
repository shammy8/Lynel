import pygame.font


class Button():

    def __init__(self, ai_settings, screen, msg):
        """initialises a play button between games"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width, self.height = 600, 50
        self.button_color = (255, 0, 0)
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = 600
        self.prep_msg(msg)

    
    def prep_msg(self, msg):
        """initialises the message to be displayed on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.centerx = self.rect.centerx
        self.msg_image_rect.centery = 600

    
    def draw_button(self):
        """draw button to the window"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
