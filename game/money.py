import pygame
from const import TILE_SIZE, ANIM_SPEED


class Money(pygame.sprite.Sprite):  # класс монеток
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.all_images = []
        for i in range(1, 7):
            img = pygame.image.load(f'data/images/money/coin_{i}.png')
            img = pygame.transform.scale(img, (TILE_SIZE // 2, TILE_SIZE // 2))
            self.all_images.append(img)

        self.image = self.all_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.count = 0
        self.speed = 10
        self.id = 0

    def update(self):  # анимация
        self.count += 1
        if self.count > self.speed:
            self.count = 0
            self.id += 1
            self.image = self.all_images[self.id % 5]
