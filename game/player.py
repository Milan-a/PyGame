import pygame
from const import PLAYER_SPEED, JUMP_HEIGHT, ANIM_SPEED
from intermediary import life
from world import tile_list


class Player:
    def __init__(self, x, y, width, height, enemy_group, lava_group, money_group):
        self.start(x, y, width, height, enemy_group, lava_group, money_group)
        self.win = False  # По умолчанию игрок не победил
        # Загружаем звук шагов
        self.step_sound = pygame.mixer.Sound('data/sounds/Footsteps.mp3')  # Укажите путь к файлу звука
        self.step_sound.set_volume(1)  # Устанавливаем громкость (0.0 до 1.0)
        self.playing_step_sound = False  # Флаг, который отслеживает, играется ли звук шагов

    def animation(self, right, jump):  # Анимация персонажа
        if not jump:
            self.count += 1
            if self.count > ANIM_SPEED:
                self.count = 0
                self.walk_id += 1
                if right:
                    self.player_img = self.walk_right[self.walk_id % 4]
                else:
                    self.player_img = self.walk_left[self.walk_id % 4]
        else:
            if right:
                self.player_img = self.walk_right[1]
            else:
                self.player_img = self.walk_left[1]

    def set_win(self, win_status):
        """Обновляет состояние победы в классе Player."""
        self.win = win_status
        if self.win and self.playing_step_sound:  # Если игрок победил, выключаем звук шагов
            self.step_sound.stop()
            self.playing_step_sound = False

    def toggle_step_sound(self, playing):
        """Включает или выключает звук шагов в зависимости от переменной `playing` и состояния игрока."""
        if self.win:  # Если победа — выключаем звук шагов
            if self.playing_step_sound:
                self.step_sound.stop()
                self.playing_step_sound = False
            return
        if playing:  # Если игрок двигается
            if not self.playing_step_sound:  # Если звук не воспроизводится
                self.step_sound.play(loops=-1)  # Включаем звук шагов (повторяем до остановки)
                self.playing_step_sound = True
        else:  # Если игрок остановился
            if self.playing_step_sound:  # Если звук воспроизводится
                self.step_sound.stop()  # Останавливаем звук
                self.playing_step_sound = False

    def move_player(self, screen, game_over):  # Конструкция обработки кнопок для движения персонажа
        dx = 0
        dy = 0
        is_walking = False  # Флаг отслеживает, двигается ли игрок

        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and not self.is_jump and not self.on_flor:
                self.speed_y = -JUMP_HEIGHT
                self.is_jump = True
                self.animation(self.walk_pos, self.is_jump)
            if not key[pygame.K_SPACE]:
                self.is_jump = False

            if key[pygame.K_LEFT]:
                dx -= PLAYER_SPEED
                self.walk_pos = False
                is_walking = True  # Игрок движется
                if not key[pygame.K_SPACE]:
                    self.animation(False, self.is_jump)
            if key[pygame.K_RIGHT]:
                dx += PLAYER_SPEED

                self.walk_pos = True
                is_walking = True  # Игрок движется
                if not key[pygame.K_SPACE]:
                    self.animation(True, self.is_jump)
            if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT] and not self.is_jump:
                self.count = 0
                self.walk_id = 0
                if self.walk_pos:
                    self.player_img = self.walk_right[self.walk_id]
                else:
                    self.player_img = self.walk_left[self.walk_id]

            self.speed_y += 1
            if self.speed_y > 13:
                self.speed_y = 13
            dy += self.speed_y

            self.on_flor = True
            for tile in tile_list:  # проверка столкновений с блоками
                #  Столкновения по X
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                    if tile[-1] == 'portal':
                        return 'portal'
                #  Столкновения по Y
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.speed_y < 0:
                        self.speed_y = 0
                        dy = tile[1].bottom - self.rect.top
                    elif self.speed_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.on_flor = False

            # Проверка работает ли звук шагов
            self.toggle_step_sound(is_walking)

            # Проверка столкновений со всякими зловещими штуками
            if pygame.sprite.spritecollide(self, self.groups[0], False):  # enemy
                self.toggle_step_sound(False)  # Выключаем звук шагов при смерти
                game_over = life.rip(screen)
                screen.blit(self.player_img, self.rect)
                if game_over:
                    return game_over
                else:
                    return 'rip'
            if pygame.sprite.spritecollide(self, self.groups[1], False):  # lava
                self.toggle_step_sound(False)  # Выключаем звук шагов при смерти
                game_over = life.rip(screen)
                screen.blit(self.player_img, self.rect)
                if game_over:
                    return game_over
                else:
                    return 'rip'

            self.move(dx, dy)
            screen.blit(self.player_img, self.rect)  # Отрисовка игрока
        else:
            self.toggle_step_sound(False)  # Выключаем звук, если игра окончена

    def move(self, dx, dy):  # Передвижение
        self.rect.x += dx
        self.rect.y += dy

    def start(self, x, y, width, height, enemy_group, lava_group, money_group):  # = __init__
        self.groups = (enemy_group, lava_group, money_group)
        self.width = width
        self.height = height
        self.walk_right = []
        self.walk_left = []
        self.walk_id = 0
        self.walk_pos = True
        self.count = 0
        for i in range(1, 5):  # Подгоняем размер каждого изображения и добавляем в списки
            img_r = pygame.image.load(f'data/images/player/right_{i}.png').convert_alpha()
            img_r = pygame.transform.scale(img_r, (width, height))
            img_r.set_colorkey((255, 255, 255))
            self.walk_right.append(img_r)
            img_l = pygame.image.load(f'data/images/player/left_{i}.png').convert_alpha()
            img_l = pygame.transform.scale(img_l, (width, height))
            img_l.set_colorkey((255, 255, 255))
            self.walk_left.append(img_l)

        self.player_img = self.walk_right[0]
        self.rect = self.player_img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.c = 0
        self.speed_y = 0
        self.is_jump = False
        self.on_flor = True
