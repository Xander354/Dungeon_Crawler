import pygame
from pygame.locals import *
from tiles import *
from player import *
from enemies import *
from level import *

import sys

pygame.init()

size = (width, height) = (800, 600)

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
color = (0, 0, 0)
images = {"w": "images/tiles/wall12.gif", "f": "images/tiles/floor13.gif",
          "s": {True: "images/tiles/openDoor31.gif", False: "images/tiles/door31.gif"},
          "e": {True: "images/tiles/openDoor12.gif", False: "images/tiles/door12.gif"}}
player = Player("images/player/superhero.gif", (16, 16), False)
levels = []
level_num = 0
current_level = None
font = pygame.font.SysFont('oldenglishtext', 32)
debug = True


def change_level(change):
    global level_num, current_level
    if change == 1:
        if level_num == len(levels) - 1:
            levels.append(RandomLevel(player, images, .5, 2 + 2 * level_num))
        level_num += 1
        current_level = levels[level_num]
        player.up_level(current_level)
    elif change == -1:
        if level_num > 0:
            level_num -= 1
            current_level = levels[level_num]
            player.back_level(current_level)


# initializes globals to starting state
def restart():
    global player, levels, level_num, current_level
    player = Player("images/player/superhero.gif", (16, 16), False)
    levels = [RandomLevel(player, images, .5, 2)]
    level_num = 0
    current_level = levels[level_num]
    player.up_level(current_level)


def main():
    global screen, level_num, current_level
    restart()
    restart_pressed = False
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                # confirm/ exit restart if triggered
                if restart_pressed:
                    if event.key == K_RETURN:
                        restart()
                        restart_pressed = False
                    elif event.key == K_ESCAPE:
                        restart_pressed = False
                    continue
                # screen controls
                if event.key == K_f:
                    screen = pygame.display.set_mode(size, FULLSCREEN)
                elif event.key == K_ESCAPE:
                    screen = pygame.display.set_mode(size)
                # player movement controls
                elif event.key == K_UP:
                    player.change_y(-32)
                elif event.key == K_DOWN:
                    player.change_y(32)
                elif event.key == K_RIGHT:
                    player.change_x(32)
                elif event.key == K_LEFT:
                    player.change_x(-32)
                elif event.key == K_a:
                    player.attack()
                # initiates restart prompt
                elif event.key == K_r:
                    restart_pressed = True
                # debugging related controls
                if debug:
                    # Go up one level
                    if event.key == K_w:
                        if level_num == len(levels)-1:
                            levels.append(RandomLevel(player, images, .5, 2 + 2 * level_num))
                        level_num += 1
                        current_level = levels[level_num]
                        player.up_level(current_level)
                    # Go down one level
                    elif event.key == K_s:
                        if level_num > 0:
                            level_num -= 1
                            current_level = levels[level_num]
                            player.back_level(current_level)
        # update the level if not is restart mode
        if not restart_pressed:
            change_level(current_level.update())
        screen.fill(color)
        current_level.draw(screen)
        text = font.render("Level: {}    Health: {}    Attack LvL: {}    Defense LvL: {}".format(
            level_num+1, player.health, player.attack_damage, player.defense), True, (230, 230, 230))
        text_rect = text.get_rect()
        text_rect.bottomright = (width, height)
        screen.blit(text, text_rect)
        if restart_pressed:
            text = font.render("Press Enter to restart, press ESC to cancel", True, (230, 230, 230))
            text_rect = text.get_rect()
            text_rect.center = (width//2, height//2)
            screen.blit(text, text_rect)
        pygame.display.flip()


if __name__ == "__main__":
    main()
