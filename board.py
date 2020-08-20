import pygame
import numpy as np


class Board:
    """Class representing the game board."""

    def __init__(self, settings, screen, start_angle, end_angle):
        """Initialise the board and set its starting position."""

        self.settings = settings

        # Board owns references to screen, and copies of relevant settings
        self.screen = screen
        self.n_rows = settings.n_rows
        self.n_cols = settings.n_cols
        self.cell_length = settings.cell_size[0]

        # grid is a 2D list with 0, 1, 2:
        # representing empty, player 1 and player 2 respectively
        self.grid = np.zeros((settings.n_rows, settings.n_cols))

        # rects is a 2D list of Rects representing tiles on the board.
        self.rects = self.init_rect_grid()

        self.rect = pygame.Rect((0, 0), settings.board_size)
        #self.image = screen.subsurface(self.rect)
        self.pos = (settings.board_size[0]//2, settings.board_size[1]//2)

        self.angle = start_angle
        self.end_angle = end_angle
        self.is_rotating = False

        # load tile images, scaled to cell_size
        self.dark_tile_image = pygame.transform.scale(
            pygame.image.load(settings.tile_image_paths["dark"]),
            settings.cell_size)
        self.light_tile_image = pygame.transform.scale(
            pygame.image.load(settings.tile_image_paths["light"]),
            settings.cell_size)

        self.image = self.init_board_image()

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

    def init_board_image(self):
        """
        Draws the board at its current position, tile by tile, then
        returns that image as a `pygame.Surface`.
        """
        image = pygame.Surface(self.settings.board_size)
        for row in range(self.n_rows):
            for col in range(self.n_cols):

                # checkerboard pattern
                if row % 2 == col % 2:
                    tile_image = self.light_tile_image
                else:
                    tile_image = self.dark_tile_image

                image.blit(tile_image, self.rects[row][col].topleft[::-1])

        return image

    def draw(self):

        self.screen.blit(self.image, self.rect)


'''

    def is_done_rotating(self):
        return self.angle >= self.end_angle

    def update(self):
        """"""
        if self.is_rotating:
            if self.is_done_rotating():
                self.is_rotating = False
            else:
                self.angle += INCREMENT
                self.image = self.rotate(self.image, INCREMENT)
        #print(self.angle)

    def rotate(self, image, angle):
        """"""
        image = self.image
        pos = self.pos
        originPos = self.pos

        # calcaulate the axis aligned bounding box of the rotated image
        w, h = image.get_size()
        box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(angle) for p in box]
        min_box = (min(box_rotate, key=lambda p: p[0])[
                0], min(box_rotate, key=lambda p: p[1])[1])
        max_box = (max(box_rotate, key=lambda p: p[0])[
                0], max(box_rotate, key=lambda p: p[1])[1])

        # calculate the translation of the pivot
        pivot = pygame.math.Vector2(originPos[0], -originPos[1])
        pivot_rotate = pivot.rotate(angle)
        pivot_move = pivot_rotate - pivot

        # calculate the upper left origin of the rotated image
        origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0],
                pos[1] - originPos[1] - max_box[1] + pivot_move[1])

        # get a rotated image
        image = pygame.Surface(self.settings.board_size)
        image.blit(pygame.transform.rotate(image, angle), origin)
        #rotated_image = pygame.transform.rotate(image, angle)
        #pygame.transform.rotate(self.image, angle)

        return image
'''
