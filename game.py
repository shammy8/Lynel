import pygame
from pygame.sprite import Group

from settings import Settings
from link import Link
from bomb import Bomb
import game_functions as gf 
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    """main function of the game used to create instances of all the classes, create the window, load the music etc"""
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Lynel Invasion")
    pygame.mixer.music.play(-1)

    clock = pygame.time.Clock()
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    play_button = Button(ai_settings, screen, "Click here or press any key to start.")

    link = Link(ai_settings, screen)
    bombs = Group()
    arrows = Group()
    lynels = Group()

    gf.create_horde(ai_settings, screen, link, lynels)
    
    #main loop of the game, continues until user quits the game. checks for user inputs and display the images on screen
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, link, lynels, arrows, bombs, clock)
        if stats.game_active:
                link.update()
                gf.update_arrows(ai_settings, screen, stats, sb, link, lynels, arrows, bombs)
                gf.update_lynels(ai_settings, screen, stats, sb, link, lynels, arrows)
                gf.update_bombs(ai_settings, screen, link, lynels, bombs, clock)
        gf.update_screen(ai_settings, screen, stats, sb, link, lynels, arrows, bombs, play_button)


run_game()