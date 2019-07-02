import pygame.font
from pygame.sprite import Group
from link import Lifes


class Scoreboard():

    def __init__(self, ai_settings, screen, stats):
        """initialise information to display on the screen"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        self.text_color = (30,30,30)#(230, 0, 0)
        self.font = pygame.font.SysFont(None, 34)

        self.prep_score()
        self.prep_high_score()
        self.prep_multiplier()
        self.prep_level()
        self.prep_lifes()
        self.prep_help()
        

    def prep_score(self):
        """initialse the score to be displayed"""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 15

    
    def prep_high_score(self):
        """initialse the high score to be displayed"""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "hi: " +"{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top


    def prep_level(self):
        """initialse the current level to be displayed"""
        self.level_image  =self.font.render("lvl: " + str(self.stats.level), True, self.text_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = 10
        self.level_rect.top = self.score_rect.bottom + 10


    def prep_multiplier(self):
        """initialse the scoring multiplier to be displayed"""
        self.multiplier_image  =self.font.render(str(self.stats.multiplier) + "x", True, self.text_color)
        self.multiplier_rect = self.multiplier_image.get_rect()
        self.multiplier_rect.right = self.score_rect.right
        self.multiplier_rect.top = self.score_rect.bottom + 10


    def prep_lifes(self):
        """initialse the lifes left to be displayed"""
        self.lifes = Group()
        for life_number in range(self.stats.link_left):
            life = Lifes(self.ai_settings, self.screen)
            life.rect.x = 10 + life_number * life.rect.width
            life.rect.y = 10
            self.lifes.add(life)


    def prep_help(self):
        """initialse the scoring multiplier to be displayed"""
        font = pygame.font.SysFont(None, 16)
        self.help_image  = font.render("A: move left,  D: move right,  SPACE: fire arrows,  LEFT & RIGHT: launch Bombchu,  1 & 2 & 3: selects songs,  Q: quit",
        True, self.text_color)
        self.help_rect = self.help_image.get_rect()
        self.help_rect.left = self.screen_rect.left + 5
        self.help_rect.bottom = self.screen_rect.bottom - 1


    def show_score(self):
        """display information onto the window"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.multiplier_image, self.multiplier_rect)
        self.lifes.draw(self.screen)
        self.screen.blit(self.help_image, self.help_rect)


    
    