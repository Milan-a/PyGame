import pygame
from const import *
from enemy import Enemy
from money import Money
from lava import Lava

tile_list = []


def append_tile(image, type_im, cords):
    image_rect = image.get_rect()
    image_rect.x = TILE_SIZE * cords[1]
    image_rect.y = TILE_SIZE * cords[0]
    tile = (image, image_rect, type_im)
    tile_list.append(tile)


def draw_world(screen):  # рисуем блоки
    for block, coord, type_im in tile_list:
        screen.blit(block, coord)


class World:
    def __init__(self, data, enemy_group, lava_group, money_group):
        self.start(data, enemy_group, lava_group, money_group)

    def start(self, data, enemy_group, lava_group, money_group):
        tile_list.clear()
        # заглушка на случай ошибки
        img11 = pygame.image.load('data/images/blocks/block_11.png')

        for i, row in enumerate(data):  # делаем список из блоков
            for j, block in enumerate(row):
                if block == '0':
                    continue
                elif block == 'p1' or block == 'p2':
                    img = pygame.image.load(f'data/images/blocks/portal{block[-1]}.png')
                    image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                    type_im = 'portal'
                    append_tile(image, type_im, (i, j))
                elif block == 'e':  # приведение
                    enemy = Enemy(TILE_SIZE * j + 15, TILE_SIZE * i + 15)
                    enemy_group.add(enemy)
                elif block == 'l':  # лава
                    lava = Lava(TILE_SIZE * j, TILE_SIZE * i)
                    lava_group.add(lava)
                elif block == 'm':  # монетки
                    money = Money(TILE_SIZE * j + (TILE_SIZE // 2), TILE_SIZE * i + (TILE_SIZE // 2))
                    money_group.add(money)

                else:
                    try:
                        img = pygame.image.load(f'data/images/blocks/block_{block}.png')
                        image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                    except FileNotFoundError:
                        image = pygame.transform.scale(img11, (TILE_SIZE, TILE_SIZE))
                    type_im = 'block'
                    append_tile(image, type_im, (i, j))
