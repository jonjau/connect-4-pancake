import pygame

class Background():

    def __init__(self, settings, screen):
        image_game = pygame.image.load(settings.background_image_path)
        image_main = pygame.image.load(settings.background_main_image_path)
        image_dark = pygame.image.load(settings.background_dark_image_path)
        self.screen = screen
        self.settings = settings
        self.image_game = pygame.transform.scale(image_game, settings.screen_size)
        self.image_main = pygame.transform.scale(image_main, settings.screen_size)
        self.image_dark = pygame.transform.scale(image_dark, settings.screen_size)
        self.rect_main = self.image_main.get_rect()
        self.rect_game = self.image_game.get_rect()
        self.rect_dark = self.image_dark.get_rect()

    def draw_game(self):
        self.screen.blit(self.image_game, self.rect_game)

    def draw_main(self):
        self.screen.blit(self.image_main, self.rect_main)

    def draw_dark(self):
        self.screen.blit(self.image_dark, self.rect_dark)
