import pygame
import numpy as np

class Board():
    """Class representing the game board."""

    def __init__(self, settings, screen):
        """Initialise the board and set its starting position."""
        # construct the parent pygame.Sprite of this Board
        # super().__init__()

        # Board owns a reference to screen and settings
        self.screen = screen
        self.settings = settings

        self.grid = np.zeros((self.settings.n_rows, self.settings.n_cols))
        self.rects = self.init_rect_grid()

        self.dark_tile_image = pygame.transform.scale(
            pygame.image.load(settings.tile_image_paths["dark"]),
            settings.cell_size)

        self.light_tile_image = pygame.transform.scale(
            pygame.image.load(settings.tile_image_paths["light"]),
            settings.cell_size)

    def init_rect_grid(self):
        """aa"""
        n_rows = self.settings.n_rows
        n_cols = self.settings.n_cols
        cell_size = self.settings.cell_size[0]

        rects = [[None for i in range(n_cols)] for j in range(n_rows)]
        for i in range(n_rows):
            for j in range(n_cols):
                rects[i][j] = pygame.Rect(
                    i * cell_size, j * cell_size,
                    cell_size, cell_size)

        # print(rects[2][3].top)
        # print(rects[2][3].left)

        return rects

    def draw(self):
        """Draw the board at its current position, tile by tile."""
        rects = self.rects

        for row in range(self.settings.n_rows):
            for col in range(self.settings.n_cols):

                rect = rects[row][col]

                if row % 2 == col % 2:
                    tile_image = self.light_tile_image
                else:
                    tile_image = self.dark_tile_image

                self.screen.blit(tile_image, rect.topleft)

    def drop_coin(self, row, col, player):
        self.grid[row, col] = player


