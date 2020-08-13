import pygame
import numpy as np

class Board(pygame.sprite.Sprite):
    """Class representing the game board."""

    def __init__(self, settings, screen):
        """Initialise the board and set its starting position."""
        # construct the parent pygame.Sprite of this Board
        super().__init__()

        # Board owns a reference to screen and settings
        self.screen = screen
        self.settings = settings

        self.grid = np.zeros((7, 7))

        image = pygame.image.load(settings.board_image_path)
        self.image = pygame.transform.scale(image, settings.board_size)
        self.rect = self.image.get_rect()

        # set initial position somewhere...
        self.rect.x = 0
        self.rect.y = 0

    def draw(self):
        """Draw the board at its current position."""
        self.screen.blit(self.image, self.rect)


