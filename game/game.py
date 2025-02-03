import pygame
from const import FPS, WIDTH, HEIGHT, TILE_SIZE, SIZE
from player import Player
from world import World, draw_world
from help_funс import load_level, draw_text
from button import Button

# важные значения
GAME_OVER = 0
MENU = True
LVL = 3
SCORE = 0
WIN = False

pygame.init()
screen = pygame.display.set_mode((WIDTH - 2, HEIGHT - 2))
pygame.display.set_caption("Miner")  # типо 'шахтёр'
icon = pygame.image.load('data/images/icon.png')
pygame.display.set_icon(icon)
bg_image = pygame.image.load('data/images/background_1.png')
bg_image = pygame.transform.scale(bg_image, SIZE)
clock = pygame.time.Clock()
font1 = pygame.font.SysFont('Playbill', 40)
# OCR A Extended, Cooper Black, Playbill, Bauhaus 93, Showcard Gothic, Wide Latin

win_image = pygame.image.load('data/images/background _ win.jpg')
win_image = pygame.transform.scale(win_image, SIZE)

enemy_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
money_group = pygame.sprite.Group()

level = load_level(f'level_{LVL}.txt')
world = World(level, enemy_group, lava_group, money_group)
player = Player(TILE_SIZE + TILE_SIZE * 0.1, HEIGHT - TILE_SIZE * 4,
                TILE_SIZE - TILE_SIZE * 0.08, TILE_SIZE + TILE_SIZE * 0.2,
                enemy_group, lava_group, money_group)

# кнопка start
start_image = pygame.image.load('data/images/buttoms/buttom_for_start.png')
start_image = pygame.transform.scale(start_image, (WIDTH // 6, HEIGHT // 20))
button_for_start = Button(WIDTH // 2 - 69, HEIGHT // 2 - 50, start_image, 'start')

# кнопка exit
exit_image = pygame.image.load('data/images/buttoms/buttom_for_exit.png')
exit_image = pygame.transform.scale(exit_image, (WIDTH // 7, HEIGHT // 19))
button_for_exit = Button(WIDTH // 2 - 60, HEIGHT // 2 + 10, exit_image, 'exit')

# кнопка menu
menu_image = pygame.image.load('data/images/buttoms/buttom_for_menu.png')
menu_image = pygame.transform.scale(menu_image, (WIDTH // 6, HEIGHT // 19))
button_for_menu = Button(WIDTH // 2 - 69, HEIGHT // 2 - 50, menu_image, 'menu')

# кнопка play
play_image = pygame.image.load('data/images/buttoms/buttom_for_play.png')
play_image = pygame.transform.scale(play_image, (WIDTH // 7, HEIGHT // 19))
button_for_play = Button(WIDTH // 2 - 60, HEIGHT // 2 + 10, play_image, 'play')


def play_reboot():  # начинаем игру с самого нуля
    global GAME_OVER, MENU, LVL, SCORE, WIN, world, level, enemy_group, lava_group, money_group
    GAME_OVER = 0
    MENU = True
    LVL = 1
    SCORE = 0
    WIN = False
    LVL = 1
    level = load_level(f'level_{LVL}.txt')
    enemy_group = pygame.sprite.Group()
    lava_group = pygame.sprite.Group()
    money_group = pygame.sprite.Group()
    world = World(level, enemy_group, lava_group, money_group)
    player.start(TILE_SIZE + TILE_SIZE * 0.1, HEIGHT - TILE_SIZE * 4,
                 TILE_SIZE - TILE_SIZE * 0.08, TILE_SIZE + TILE_SIZE * 0.2,
                 enemy_group, lava_group, money_group)


def draw():  # вспомогательная функция, рисующая сетку на экране
    for line in range(20):
        pygame.draw.line(screen, (255, 255, 255), (0, line * TILE_SIZE), (WIDTH, line * TILE_SIZE))
        pygame.draw.line(screen, (255, 255, 255), (line * TILE_SIZE, 0), (line * TILE_SIZE, HEIGHT))


def main():
    global MENU, SCORE, WIN, world, enemy_group, lava_group, LVL, level, money_group, bg_image
    clock.tick(FPS)

    running = True
    while running:
        if WIN:
            screen.blit(win_image, (0, 0))
        else:
            screen.blit(bg_image, (0, 0))
            if MENU:
                if button_for_start.draw(screen):
                    play_reboot()
                    MENU = False
                if button_for_exit.draw(screen):
                    running = False
            else:
                draw_world(screen)  # рисуем мир
                game_over = player.move_player(screen, GAME_OVER)  # рисуем игрока
                if game_over == 'portal':
                    enemy_group = pygame.sprite.Group()
                    lava_group = pygame.sprite.Group()
                    money_group = pygame.sprite.Group()
                    LVL += 1
                    try:  # если уровень загружается, то продолжаем играть
                        level = load_level(f'level_{LVL}.txt')
                        world = World(level, enemy_group, lava_group, money_group)
                        player.start(TILE_SIZE + TILE_SIZE * 0.1, HEIGHT - TILE_SIZE * 4,
                                     TILE_SIZE - TILE_SIZE * 0.08, TILE_SIZE + TILE_SIZE * 0.2,
                                     enemy_group, lava_group, money_group)
                    except FileNotFoundError:  # если падает с ошибкой, значит мы выиграли
                        WIN = True
                if game_over is None:
                    enemy_group.update()
                    if pygame.sprite.spritecollide(player, money_group, True):
                        SCORE += 1
                    draw_text(screen, f'Score: {SCORE}', font1, 'black', 570, 6)
                    draw_text(screen, f'Score: {SCORE}', font1, 'white', 572, 5)

                    draw_text(screen, f'LVL: {LVL}', font1, 'black', WIDTH - 102, 6)
                    draw_text(screen, f'LVL: {LVL}', font1, 'white', WIDTH - 100, 5)

                enemy_group.draw(screen)
                lava_group.draw(screen)
                money_group.draw(screen)

                if game_over == -1:
                    fon = pygame.Surface((WIDTH, HEIGHT))
                    fon = fon.convert_alpha()
                    fon.fill((255, 0, 0, 100))
                    screen.blit(fon, (0, 0))

                    if button_for_menu.draw(screen):
                        MENU = True
                    if button_for_play.draw(screen):
                        player.start(TILE_SIZE + TILE_SIZE * 0.1, HEIGHT - TILE_SIZE * 4,
                                     TILE_SIZE - TILE_SIZE * 0.08, TILE_SIZE + TILE_SIZE * 0.2,
                                     enemy_group, lava_group, money_group)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if WIN and pygame.mouse.get_pressed()[0]:
                play_reboot()
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
