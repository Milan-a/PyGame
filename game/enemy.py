import pygame
from const import TILE_SIZE


class Enemy(pygame.sprite.Sprite):  # класс приведений
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image_l = pygame.image.load('data/images/blocks/enemy_1.png')
        image_l = pygame.transform.scale(image_l, (TILE_SIZE - TILE_SIZE * 0.5, TILE_SIZE - TILE_SIZE * 0.5))
        image_r = pygame.transform.flip(image_l, True, False)
        image_r = pygame.transform.scale(image_r, (TILE_SIZE - TILE_SIZE * 0.5, TILE_SIZE - TILE_SIZE * 0.5))
        self.images_r_l = [image_l, image_r]

        self.image = self.images_r_l[1]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move = 2
        self.count_move = 0

    def update(self):  # перемещение приведений
        self.rect.x += self.move
        self.count_move += 1
        if abs(self.count_move) >= TILE_SIZE:
            self.move *= -1
            self.count_move *= -1

            if self.images_r_l.index(self.image) == 1:  # зеркалим изображение
                self.image = self.images_r_l[0]
            else:
                self.image = self.images_r_l[1]
