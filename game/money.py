import pygame
from const import TILE_SIZE


class Money(pygame.sprite.Sprite):  # класс монеток
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('data/images/blocks/money.png')
        self.image = pygame.transform.scale(image, (TILE_SIZE // 2, TILE_SIZE // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

