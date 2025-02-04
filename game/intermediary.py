from life import Life
import pygame
from const import WIDTH, HEIGHT

# что бы файлы друг на друга не ссылались, мне пришлось сделать посредника :/

screen = pygame.display.set_mode((WIDTH - 2, HEIGHT - 2))
life = Life(screen)


def new_life():
    global life
    life.new_game(screen)
