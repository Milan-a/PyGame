import pygame


class Button:
    def __init__(self, x, y, image, button_type):
        self.button_type = button_type
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_click = False

    def draw(self, screen):  # отрисовка + проверка нажатий
        do_click = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.is_click:
                do_click = True
                self.is_click = True
        if not pygame.mouse.get_pressed()[0]:
            self.is_click = False

        screen.blit(self.image, self.rect)

        return do_click
