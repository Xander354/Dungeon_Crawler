import random

import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, path, pos):
        super().__init__()
        self.path = path
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def scroll(self, change):
        self.rect.move_ip(change)


class Door(Tile):
    def __init__(self, images, pos, unlocked):
        super().__init__(images[unlocked], pos)
        self.images = images
        self.unlocked = unlocked

    def unlock(self):
        self.unlocked = True
        self.image = pygame.image.load(self.images[self.unlocked])


class Chest(Tile):
    def __init__(self, image, pos):
        super().__init__(image, pos)

    def give_bonus(self, player):
        num = random.randint(1, 3)
        self.kill()
        if num == 1:
            inc = random.randint(3, 7)
            player.health += inc
        elif num == 2:
            inc = random.randint(1, 3)
            player.attack_damage += inc
        elif num == 3:
            player.defense += 1
