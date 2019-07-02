"""the main logic of the game"""
import sys
import pygame
from time import sleep

from arrow import Arrow
from bomb import Bomb
from lynel import Lynel
        

def check_events(ai_settings, screen, stats, sb, play_button, link, lynels, arrows, bombs, clock):
    """check for user inputs mainly: quitting, pressing mouse button and preesing and releasing of keyboard buttons"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stats.update_highscore()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #used for checking if the user has pressed the play button to start a new game
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, link, lynels, arrows, bombs, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN and not stats.game_active:
            #starts the game on any keyboard press
            start_game(ai_settings, screen, stats, sb, play_button, link, lynels, arrows, bombs)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, sb, link, arrows, bombs, clock)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, link)


def check_keydown_events(event, ai_settings, screen, stats, sb, link, arrows, bombs, clock):
    """check for key presses, moving left and right, shooting arrows, shooting bombs left and right, choosing songs and quitting"""
    if event.key == pygame.K_d:
        #set moving right flag for continuous movement of Link
        link.moving_right = True
    elif event.key == pygame.K_a:
        #set moving left flag for continuous movement of Link
        link.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_arrow(ai_settings, screen, link, arrows)
    elif event.key == pygame.K_RIGHT:
        #set bomb direction flag
        bombs.bomb_direction = 0
        fire_bomb(ai_settings, screen, stats, sb, link, bombs, clock)
    elif event.key == pygame.K_LEFT:
        #set bomb direction flag
        bombs.bomb_direction = 1
        fire_bomb(ai_settings, screen, stats, sb, link, bombs, clock)
    elif event.key == pygame.K_1:
        pygame.mixer.music.load("sounds/Palace.mp3")
        pygame.mixer.music.play(-1)
    elif event.key == pygame.K_2:
        pygame.mixer.music.load("sounds/DarkGoldenLand.mp3")
        pygame.mixer.music.play(-1)
    elif event.key == pygame.K_3:
        pygame.mixer.music.load("sounds/Classic.mp3")
        pygame.mixer.music.play(-1)
    elif event.key == pygame.K_q:
        stats.update_highscore()
        sys.exit()


def check_keyup_events(event, link):
    """actions for when key releases, used for continuous movement of Link"""
    if event.key == pygame.K_d:
        link.moving_right = False
    elif event.key == pygame.K_a:
        link.moving_left = False


def fire_arrow(ai_settings, screen, link, arrows):
    """if arrows on screen is less than the limit, create a new instance of Arrow and add it to the arrows Group"""
    if len(arrows) < ai_settings.arrows_allowed:
            new_arrow = Arrow(ai_settings, screen, link)
            arrows.add(new_arrow)


def fire_bomb(ai_settings, screen, stats, sb, link, bombs, clock):
    """if bombs on screen are less than the limit, create a new instance of Bomb and add it to the bombs Group.
        also decrease the scoring multiplier by two.
        begin the timer for the bomb"""
    if len(bombs) < ai_settings.bomb_limit:
        stats.multiplier = 1
        sb.prep_multiplier()
        new_bomb = Bomb(ai_settings, screen, link)
        bombs.add(new_bomb)
        new_bomb.timer = pygame.time.get_ticks()


def check_play_button(ai_settings, screen, stats, sb, play_button, link, lynels, arrows, bombs, mouse_x, mouse_y):
    """check if play button has been clicked"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(ai_settings, screen, stats, sb, play_button, link, lynels, arrows, bombs)
        

def start_game(ai_settings, screen, stats, sb, play_button, link, lynels, arrows, bombs):
    """if play button is clicked or any keyboard button is pressed starts the game resetting scoring, lifes, create new lynels etc."""
    ai_settings.initialize_dynamic_settings(1)
    pygame.mouse.set_visible(False)
    stats.reset_stats()
    stats.game_active = True

    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_lifes()

    lynels.empty()
    arrows.empty()
    bombs.empty()
    create_horde(ai_settings, screen, link, lynels)
    link.center_link


def update_screen(ai_settings, screen, stats, sb, link, lynels, arrows, bombs, play_button):
    """draw all the neccessary objects on the screen and display play button if the game isn't active"""
    screen.blit(ai_settings.background,(0,0))
    for arrow in arrows.sprites():
        arrow.draw_arrow() 
    link.blitme()
    for bomb in bombs.sprites():
        bomb.draw_bomb()
    lynels.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def update_arrows(ai_settings, screen, stats, sb, link, lynels, arrows, bombs):
    """For every arrow in the arrows group, if arrow reach the top of the screen decrease the multiplier by one until one, and remove arrow. Check for arrows hitting lynels"""
    arrows.update()
    for arrow in arrows.copy():
        if arrow.rect.bottom <= 0:
            if stats.multiplier > 1:
                stats.multiplier //= 2 
                sb.prep_multiplier()
            arrows.remove(arrow)
    check_arrow_lynel_collisions(ai_settings, screen, stats, sb, link, lynels, arrows, bombs)


def update_bombs(ai_settings, screen, link, lynels, bombs, clock):
    """for every bomb, fire it in the correct position (left/right) and distance. 
    make bomb explode when time is up, change animation.
    remove the bomb and lynels if hit"""
    for bomb in bombs.sprites():
        if bomb.y > ai_settings.screen_height - link.rect.height - ai_settings.bomb_distance and bombs.bomb_direction == 0:
            bomb.update_right()
        elif bomb.y > ai_settings.screen_height - link.rect.height - ai_settings.bomb_distance and bombs.bomb_direction == 1:
            bomb.update_left()
        if pygame.time.get_ticks() - bomb.timer > ai_settings.bomb_duration:
            bomb.image = bomb.image2
            collisions = pygame.sprite.groupcollide(bombs, lynels, False, True)
            if pygame.time.get_ticks() - bomb.timer > ai_settings.bomb_duration + ai_settings.bomb_hitbox_duration:
                bombs.remove(bomb)


def check_arrow_lynel_collisions(ai_settings, screen, stats, sb, link, lynels, arrows, bombs):
    """check for arrows hitting lynels and remove them if they do.
    increase the multiplier if a lynel is hit until a max. of 10, update the onscreen displays for current score, multiplier, hiscore etc."""
    collisions = pygame.sprite.groupcollide(arrows, lynels, True, True)
    if collisions:
        for lynels in collisions.values():
            stats.score += ai_settings.lynel_points * len(lynels) * stats.multiplier
            if stats.multiplier <= 30:
                stats.multiplier *= 2
            sb.prep_score()
            sb.prep_multiplier()
        check_high_score(stats, sb)
    if len(lynels) == 0: #if all lynels are dead go to the next level
        next_level(ai_settings, screen, stats, sb, link, lynels, arrows, bombs)


def next_level(ai_settings, screen, stats, sb, link, lynels, arrows, bombs):
    """if all lynels are dead, delete all the arrows and bombs on screen, go to next level"""
    arrows.empty()
    bombs.empty()
    stats.level += 1
    sb.prep_level()
    if stats.level < 13:
        ai_settings.initialize_dynamic_settings(stats.level)
    else:
        ai_settings.increase_speed()
    create_horde(ai_settings, screen, link, lynels)


def get_number_lynel_x(ai_settings, lynel_width):
    avaliable_space_x = ai_settings.screen_width - lynel_width
    number_lynels_x = int(avaliable_space_x / (2 * lynel_width))
    return number_lynels_x - 1


def create_lynel(ai_settings, screen, lynels, lynel_number, row_number):
    lynel = Lynel(ai_settings, screen)
    lynel_width = lynel.rect.width
    lynel.x = lynel_width + 2.5 * lynel_width * lynel_number
    lynel.rect.x = lynel.x
    lynel.rect.y = lynel.rect.height + 1.1 * lynel.rect.height * row_number - 50
    lynels.add(lynel)


def create_horde(ai_settings, screen, link, lynels):
    lynel = Lynel(ai_settings, screen)
    number_lynels_x = get_number_lynel_x(ai_settings, lynel.rect.width)
    
    for row_number in range (ai_settings.no_of_rows):
        for lynel_number in range(number_lynels_x):
            create_lynel(ai_settings, screen, lynels, lynel_number, row_number)

    
def check_fleet_edges(ai_settings, lynels):
    """if any lynels touch the left or right edges call change_fleet_direction to change the direction of lynels and move them down"""
    for lynel in lynels.sprites():
        if lynel.check_edges():
            change_fleet_direction(ai_settings, lynels)
            break


def change_fleet_direction(ai_settings, lynels):
    """method used when any lynels touch the left or right edges.
    move the lynels down slightly and change their y-direction"""
    for lynel in lynels.sprites():
        lynel.rect.y += ai_settings.horde_drop_speed
    ai_settings.horde_direction *= -1


def update_lynels(ai_settings, screen, stats, sb, link, lynels, arrows):
    """call check_fleet_edges to move lynels down the screen while moving right and left.
    if any lynels hit link call link_hit which gets the game ready for it to be continued"""
    check_fleet_edges(ai_settings, lynels)
    lynels.update()
    if pygame.sprite.spritecollideany(link, lynels):
        link_hit(ai_settings, screen, stats, sb, link, lynels, arrows)
    check_lynels_bottom(ai_settings, screen, stats, sb, link, lynels, arrows)
        

def link_hit(ai_settings, screen, stats, sb, link, lynels, arrows):
    """method for when link gets hit or a lynel reaches the bottom.
    if there are still lifes decrease the life by one, set the multiplier back to one, delete lynels and arrows on screen.
    create new set of lynels, center link and pause for a second.
    if there is no life left set the game active to false"""
    if stats.link_left > 1:
        stats.link_left -= 1
        stats.multiplier = 1
        sb.prep_multiplier()
        sb.prep_lifes()
        lynels.empty()
        arrows.empty()
        create_horde(ai_settings, screen, link, lynels)
        link.center_link()
        sleep(1)
    else:
        sleep(2)
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_lynels_bottom(ai_settings, screen, stats, sb, link, lynels, arrows):
    """check if any of the lynels reach the bottom of the screen, if there is call the link_hit method"""
    screen_rect = screen.get_rect()
    for lynel in lynels.sprites():
        if lynel.rect.bottom >= screen_rect.bottom:
            link_hit(ai_settings, screen, stats, sb, link, lynels, arrows)
            break


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()