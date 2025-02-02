import pygame
from const import TILE_SIZE


class Lava(pygame.sprite.Sprite):  # класс лавы
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('data/images/blocks/lava.jpg')
        self.image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move = 1
        self.count_move = 0
