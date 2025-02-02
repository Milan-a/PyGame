import pygame
from const import FPS, WIDTH, HEIGHT, TILE_SIZE, SIZE
from player import Player
from world import World, draw_world
from help_funс import load_level
from button import Button

GAME_OVER = 0
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Какой то чел")
icon = pygame.image.load('data/images/icon.png')
pygame.display.set_icon(icon)
bg_image = pygame.image.load('data/images/background_1.png')
bg_image = pygame.transform.scale(bg_image, SIZE)
clock = pygame.time.Clock()

enemy_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()

level = load_level('level_1.txt')
world = World(level, enemy_group, lava_group)
player = Player(TILE_SIZE + TILE_SIZE * 0.1, HEIGHT - TILE_SIZE * 4,
                TILE_SIZE - TILE_SIZE * 0.08, TILE_SIZE + TILE_SIZE * 0.2, enemy_group, lava_group)


# кнопка play
play_image = pygame.image.load('data/images/buttoms/buttom_for_play.png')
play_image = pygame.transform.scale(play_image, (WIDTH // 7, HEIGHT // 19))
button_for_play = Button(WIDTH // 2 - 60, HEIGHT // 2 + 40, play_image, 'play')

# кнопка exit
exit_image = pygame.image.load('data/images/buttoms/buttom_for_exit.png')
exit_image = pygame.transform.scale(exit_image, (WIDTH // 7, HEIGHT // 19))
button_for_exit = Button(WIDTH // 2 - 60, HEIGHT // 2 - 40, exit_image, 'exit')

# кнопка start
# start_image = pygame.image.load('data/images/buttoms/buttom_for_start.png')
# start_image = pygame.transform.scale(start_image, (WIDTH // 6, HEIGHT // 20))
# button_for_start = Button(WIDTH // 2 - 60, HEIGHT // 2 + x, start_image, 'start')

# кнопка menu
# menu_image = pygame.image.load('data/images/buttoms/buttom_for_menu.png')
# menu_image = pygame.transform.scale(menu_image, (WIDTH // 6, HEIGHT // 17))
# button_for_menu = Button(WIDTH // 2 - 60, HEIGHT // 2 - x, menu_image, 'menu')


def draw():  # вспомогательная функция, рисующая сетку на экране
    for line in range(20):
        pygame.draw.line(screen, (255, 255, 255), (0, line * TILE_SIZE), (WIDTH, line * TILE_SIZE))
        pygame.draw.line(screen, (255, 255, 255), (line * TILE_SIZE, 0), (line * TILE_SIZE, HEIGHT))


def main():
    clock.tick(FPS)

    running = True
    while running:
        screen.blit(bg_image, (0, 0))
        draw_world(screen)  # рисуем мир
        game_over = player.move_player(screen, GAME_OVER)  # рисуем игрока

        if game_over != -1:
            enemy_group.update()
        enemy_group.draw(screen)
        lava_group.draw(screen)
        # draw()  # сетка для удобства

        if game_over == -1:
            fon = pygame.Surface((WIDTH, HEIGHT))
            fon = fon.convert_alpha()
            fon.fill((255, 0, 0, 100))
            screen.blit(fon, (0, 0))
            result, button_type = button_for_play.draw(screen)
            if result:
                player.start(TILE_SIZE + TILE_SIZE * 0.1, HEIGHT - TILE_SIZE * 4,
                             TILE_SIZE - TILE_SIZE * 0.08, TILE_SIZE + TILE_SIZE * 0.2, enemy_group, lava_group)

            # button_for_menu.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
