import pygame

class Background():

    def __init__(self, settings, screen):
        image = pygame.image.load(settings.background_image_path)
        self.screen = screen
        self.settings = settings
        self.image = pygame.transform.scale(image, settings.screen_size)
        self.rect = self.image.get_rect()

    def draw(self):
        self.screen.blit(self.image, (0, 0))
