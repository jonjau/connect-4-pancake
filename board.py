import pygame
import numpy as np

class Board():
    """Class representing the game board."""

    def __init__(self, settings, screen):
        """Initialise the board and set its starting position."""

        # Board owns references to screen, and relevant settings
        self.screen = screen
        self.n_rows = settings.n_rows
        self.n_cols = settings.n_cols
        self.cell_length = settings.cell_size[0]

        # grid is a 2D list with 0, 1, 2:
        # representing empty, player 1 and player 2 respectively
        self.grid = np.zeros((settings.n_rows, settings.n_cols))

        # rects is a 2D list of Rects representing tiles on the board.
        self.rects = self.init_rect_grid()

        # load tile images, scaled to cell_size
        self.dark_tile_image = pygame.transform.scale(
            pygame.image.load(settings.tile_image_paths["dark"]),
            settings.cell_size)
        self.light_tile_image = pygame.transform.scale(
            pygame.image.load(settings.tile_image_paths["light"]),
            settings.cell_size)

    def init_rect_grid(self):
        """
        Initialises and returns a 2D grid of pygame.Rect's, representing
        the tiles on the board.
        """
        n_rows = self.n_rows
        n_cols = self.n_cols
        cell_length = self.cell_length

        rects = [[None for i in range(n_cols)] for j in range(n_rows)]

        for i in range(n_rows):
            for j in range(n_cols):
                
                # arguments in order: left, top, width, height
                rects[i][j] = pygame.Rect(
                    i * cell_length, j * cell_length,
                    cell_length, cell_length)

        return rects

    def draw(self):
        """Draws the board at its current position, tile by tile."""

        for row in range(self.n_rows):
            for col in range(self.n_cols):
                
                # checkerboard pattern
                if row % 2 == col % 2:
                    tile_image = self.light_tile_image
                else:
                    tile_image = self.dark_tile_image

                self.screen.blit(tile_image, self.rects[row][col].topleft)



