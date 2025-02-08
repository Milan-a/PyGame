import pygame
from const import FPS, WIDTH, HEIGHT, TILE_SIZE, SIZE
from player import Player
from world import World, draw_world
from help_funс import load_level, draw_text
from button import Button
from intermediary import life, screen, new_life
from variables import *

pygame.init()
pygame.display.set_caption("Call of the Wild")
icon = pygame.image.load('data/images/icon.png')
pygame.display.set_icon(icon)
bg_image = pygame.image.load('data/images/background_1.png')
bg_image = pygame.transform.scale(bg_image, SIZE)
clock = pygame.time.Clock()

# Загрузка звуков
pygame.mixer.init()
pygame.mixer.music.load('data/sounds/Music.mp3')  # Фоновая музыка
pygame.mixer.music.play(loops=-1)  # Зациклить музыку
pygame.mixer.music.set_volume(0.2)  # Громкость фоновой музыки
# Звуки завершения уровня и выигрыша
level_win_sound = pygame.mixer.Sound('data/sounds/LevelWin.mp3')
level_win_sound.set_volume(0.5)
win_sound = pygame.mixer.Sound('data/sounds/Win.mp3')
foot_steps_sound = pygame.mixer.Sound('data/sounds/Footsteps.mp3')  # Звук шагов
damage_sound = pygame.mixer.Sound('data/sounds/Damage.mp3')  # Звук получения урона
money_sound = pygame.mixer.Sound('data/sounds/Money.mp3')  # Звук поднятия денег
game_over_sound = pygame.mixer.Sound('data/sounds/GameOver.mp3')  # Звук при окончании игры

font1 = pygame.font.SysFont('Playbill', 40)
font2 = pygame.font.SysFont('Playbill', 55)

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
    global GAME_OVER, MENU, LVL, SCORE, WIN, world, level, enemy_group, lava_group, money_group, player, win_sound_played
    GAME_OVER = 0
    MENU = False  # Начинаем с отключенного меню
    LVL = 1
    SCORE = 0  # Сброс счета
    WIN = False
    win_sound_played = False  # Сбрасываем флаг звука выигрыша
    new_life()

    # Перезагрузить все игровые группы
    enemy_group = pygame.sprite.Group()
    lava_group = pygame.sprite.Group()
    money_group = pygame.sprite.Group()

    # Загрузка первого уровня
    level = load_level(f'level_{LVL}.txt')
    world = World(level, enemy_group, lava_group, money_group)

    # Заново инициализировать игрока
    player = Player(TILE_SIZE + TILE_SIZE * 0.1, HEIGHT - TILE_SIZE * 4,
                    TILE_SIZE - TILE_SIZE * 0.08, TILE_SIZE + TILE_SIZE * 0.2,
                    enemy_group, lava_group, money_group)

    # Перезапуск музыки
    pygame.mixer.music.stop()
    pygame.mixer.music.play(loops=-1)  # Зациклить музыку


game_over_sound_played = False  # Флаг для отслеживания воспроизведения звука Game Over
win_sound_played = False  # Флаг для отслеживания воспроизведения звука You Win


def main():
    global MENU, SCORE, WIN, LVL, world, enemy_group, lava_group, level, money_group, bg_image, game_over_sound_played

    running = True
    while running:
        clock.tick(FPS)
        if WIN:  # если игрок выиграл, рисуем картинку win_image
            screen.blit(win_image, (0, 0))
            draw_text(screen, f'Your score: {SCORE}', font2, 'black', TILE_SIZE * 7 - 17, TILE_SIZE * 10 - 8)
            draw_text(screen, f'Your score: {SCORE}', font2, 'orange', TILE_SIZE * 7 - 15, TILE_SIZE * 10 - 10)
            player.toggle_step_sound(False)  # Выключаем звуки шагов
            global win_sound_played  # Используем глобальный флаг
            if not win_sound_played:  # Если звук еще не был воспроизведен
                pygame.mixer.music.stop()
                win_sound.play()  # Воспроизвести звук выигрыша
                win_sound_played = True  # Устанавливаем флаг
        else:
            screen.blit(bg_image, (0, 0))
            if MENU:
                pygame.mixer.music.stop()
                if button_for_start.draw(screen):  # нажали кнопку 'старт' => начинаем с нуля
                    play_reboot()
                    MENU = False
                if button_for_exit.draw(screen):  # нажали кнопку 'выйти' => выходим
                    running = False
            else:
                draw_world(screen)  # рисуем мир
                life.draw(screen)
                game_over = player.move_player(screen, GAME_OVER)  # рисуем игрока
                if game_over == 'rip':  # игрок умер, но у него остались жизни
                    damage_sound.play()  # Звук получения урона
                    player.start(TILE_SIZE + TILE_SIZE * 0.1, HEIGHT - TILE_SIZE * 4,
                                 TILE_SIZE - TILE_SIZE * 0.08, TILE_SIZE + TILE_SIZE * 0.2,
                                 enemy_group, lava_group, money_group)
                if game_over == 'portal':  # игрок пересёкся с порталом
                    enemy_group = pygame.sprite.Group()
                    lava_group = pygame.sprite.Group()
                    money_group = pygame.sprite.Group()
                    LVL += 1
                    try:  # если уровень загружается, то продолжаем играть
                        level = load_level(f'level_{LVL}.txt')
                        world = World(level, enemy_group, lava_group, money_group)
                        level_win_sound.play()  # Воспроизводим звук завершения уровня
                        player.start(TILE_SIZE + TILE_SIZE * 0.1, HEIGHT - TILE_SIZE * 4,
                                     TILE_SIZE - TILE_SIZE * 0.08, TILE_SIZE + TILE_SIZE * 0.2,
                                     enemy_group, lava_group, money_group)
                    except FileNotFoundError:  # если падает с ошибкой, значит мы выиграли
                        WIN = True

                if game_over is None:  # игра не закончена
                    enemy_group.update()
                    money_group.update()
                    if pygame.sprite.spritecollide(player, money_group, True):  # пересечение с монеткой
                        SCORE += 1
                        money_sound.play()  # Звук поднятия монеты

                    draw_text(screen, f'Score: {SCORE}', font1, 'black', TILE_SIZE * 12, 6)
                    draw_text(screen, f'Score: {SCORE}', font1, 'white', TILE_SIZE * 12 + 2, 5)

                    draw_text(screen, f'LVL: {LVL}', font1, 'black', WIDTH - (TILE_SIZE * 2 + 2), 6)
                    draw_text(screen, f'LVL: {LVL}', font1, 'white', WIDTH - TILE_SIZE * 2, 5)

                enemy_group.draw(screen)
                lava_group.draw(screen)
                money_group.draw(screen)

                if game_over == -1:  # игра закончена
                    fon = pygame.Surface((WIDTH, HEIGHT))  # красный фон
                    fon = fon.convert_alpha()
                    fon.fill((255, 0, 0, 100))
                    screen.blit(fon, (0, 0))

                    pygame.mixer.music.stop()  # Остановить фоновую музыку

                    if not game_over_sound_played:
                        game_over_sound.play()
                        game_over_sound_played = True

                    draw_text(screen, f'Score: {SCORE}, LVL: {LVL}', font2, 'black', TILE_SIZE * 6 - 2, TILE_SIZE * 6)
                    draw_text(screen, f'Score: {SCORE}, LVL: {LVL}', font2, 'white', TILE_SIZE * 6, TILE_SIZE * 6 - 2)

                    if button_for_menu.draw(screen):  # нажали кнопку 'меню'
                        MENU = True
                        game_over_sound_played = False  # Сброс флага на случай перезапуска через меню
                    if button_for_play.draw(screen):  # нажали 'играть' => начинаем с нуля
                        game_over_sound_played = False  # Сбрасываем флаг при новом запуске игры
                        play_reboot()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if WIN and pygame.mouse.get_pressed()[0]:  # выиграли + нажали на кнопку мыши => перезапускаем игру
                play_reboot()
                win_sound.stop()
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
