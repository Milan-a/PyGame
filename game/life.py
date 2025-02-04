import pygame


class Life:  # класс жизни 0_0
    def __init__(self, screen):

        self.all_images = []
        for i in range(0, 6):
            img = pygame.image.load(f'data/images/life/hearts_{i}.png')
            img = pygame.transform.scale(img, (170, 30))
            self.all_images.append(img)

        self.num_image = -1
        self.image = self.all_images[self.num_image]
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = 10
        self.draw(screen)

    def rip(self, screen):
        self.num_image -= 1
        try:
            self.image = self.all_images[self.num_image]
            self.draw(screen)
            if self.num_image == -6:
                return -1
        except IndexError:
            return -1

    def new_game(self, screen):
        self.num_image = -1
        self.image = self.all_images[self.num_image]
        self.draw(screen)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
