import itertools
import math
import sys

import numpy as np

import pygame
from pygame.locals import *

from coin import Coin
from board import Board
from interface import GameOver

# mouse button constants as defined by pygame
LEFT_MOUSE_BUTTON = 1
RIGHT_MOUSE_BUTTON = 2

# whose turn it currently is; player 1 is 1, player 2 is 2.
GAME_STATES = itertools.cycle([1, 2])


class Game:
    """
    Class containing the game state, objects and functions that modify them.
    """

    def __init__(self, settings, screen, music, clock):
        """Initialise settings and game state."""

        # Game owns a reference to settings and screen
        self.settings = settings
        self.screen = screen

        self.music = music
        self.clock = clock

        self.game_over = GameOver(settings, screen, clock)

        # initially it is player 1's turn
        self.state = next(GAME_STATES)

        # create game objects, they aren't drawn yet
        self.coins = pygame.sprite.Group()
        self.board = Board(settings, screen, 0, 0)

    def next_turn(self):
        """Go to the next turn."""
        self.state = next(GAME_STATES)

    def draw_background(self):
        """Draw the screen background, and the game board over it."""

        self.screen.fill(self.settings.bg_color)
        self.board.draw()

    def drop_coin(self, mouse_pos):
        """Drop one coin from the top of the column closest to `mouse_pos`"""
        board = self.board

        # coin is spawned at the top of the column closest to the mouse
        col = closest_column(board, mouse_pos)
        try:
            start_pos = board.rects[0][col].center
        except IndexError:
            return

        # coin will fall to the next open row
        row = get_next_open_row(board, col)
        try:
            end_pos = board.rects[row][col].center
        except TypeError:
            # if row is full: do nothing
            return

        # add it to the group of coin sprites
        self.coins.add(Coin(self.settings, self.screen, self.state,
                            start_pos, end_pos))

        # place the current player's number at (row, col)
        board.grid[row][col] = self.state

        print(board.grid)

        # check for win after each coin drop
        if self.check_win():
            print(f"player {self.state} wins!")

        # next player's turn now
        self.next_turn()

    def update_coins(self):
        """Update positions of all coins in play."""
        for coin in self.coins:
            coin.update()

    def draw_coins(self):
        """Draw all coins in play."""
        for coin in self.coins:
            coin.draw()

    def check_win(self):
        """
        Returns true if a winning connection exists in the board,
        false otherwise.
        """
        connect_num = self.settings.connect_num
        board = self.board
        player = self.state
        n_cols = board.n_cols
        n_rows = board.n_rows

        # Check horizontal
        for c in range(n_cols - (connect_num - 1)):
            for r in range(n_rows):
                count = 0
                for i in range(connect_num):
                    if board.grid[r][c+i] == player:
                        count += 1
                    if count == connect_num:
                        return True

        # Check vertical
        for c in range(n_cols):
            for r in range(n_rows - (connect_num - 1)):
                count = 0
                for i in range(connect_num):
                    if board.grid[r+i][c] == player:
                        count += 1
                    if count == connect_num:
                        return True

        # Check left diagonal
        for c in range(n_cols - (connect_num - 1)):
            for r in range(n_rows - (connect_num - 1)):
                count = 0
                for i in range(connect_num):
                    if board.grid[r+i][c+i] == player:
                        count += 1
                    if count == connect_num:
                        return True

        # Check right diagonal
        for c in range(n_cols - (connect_num - 1)):
            for r in range((connect_num - 1), n_rows):
                count = 0
                for i in range(connect_num):
                    if board.grid[r-i][c+i] == player:
                        count += 1
                    if count == connect_num:
                        return True
        return False

    def rotate_board(self, clockwise):
        """
        Rotate the current board clockwise or anticlockwise, then replaces
        this `Game`'s board and coins to reflect the new state.
        Additionally updates game-wide settings and the screen. 
        """
        if clockwise:
            rotated_grid = np.rot90(self.board.grid, k=1, axes=(1, 0))
        else:
            rotated_grid = np.rot90(self.board.grid, k=1, axes=(0, 1))

        n_rows, n_cols = rotated_grid.shape

        # adjust game-wide settings, then
        # update screen to reflect new board dimensions
        settings = self.settings
        settings.set_board_size(n_rows=n_rows, n_cols=n_cols, adjust=False)
        self.screen = pygame.display.set_mode(self.settings.screen_size)

        # reset game board and coins
        board = Board(self.settings, self.screen, 0, 0)
        self.board = board
        self.coins = pygame.sprite.Group()

        # from the bottom row up: drop the floating coins
        for row in range(n_rows - 1, -1, -1):
            for col in range(n_cols):

                player = rotated_grid[row][col]

                if player != 0:
                    rotated_grid[row][col] = 0

                    # find where to drop to, and create a coin to drop there
                    landing_row = get_next_open_row(board, col)

                    self.coins.add(Coin(self.settings, self.screen, player,
                                        board.rects[row][col].center,
                                        board.rects[landing_row][col].center))
                    # update grid
                    board.grid[landing_row][col] = player

    def run(self):
        """Run the game loop, then show game over screen after the game ends."""

        clock = self.clock
        music = self.music
        screen = self.screen
        settings = self.settings

        angle = 0
        target_angle = 0
        is_rotating = False

        # main game loop
        is_running = True
        while is_running:

            # keep framerate at 120 (not sure if this works)
            clock.tick(120)

            # handle events
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    # close window clicked: stop the game
                    sys.exit()

                if (event.type == pygame.MOUSEBUTTONDOWN and
                        event.button == LEFT_MOUSE_BUTTON):
                    # left mouse click detected: drop coin
                    mouse_pos = pygame.mouse.get_pos()
                    self.drop_coin(mouse_pos)
                    music.play("coin_drop")
                    if self.check_win():
                        is_running = False

                if (event.type == pygame.KEYDOWN):
                    pressed_keys = pygame.key.get_pressed()
                    if pressed_keys[K_q]:
                        target_angle -= 90
                        angle = target_angle + 90
                        increment = -2.5
                        is_rotating = True

                    elif pressed_keys[K_w]:
                        target_angle += 90
                        angle = target_angle - 90
                        increment = 2.5
                        is_rotating = True

            # draw background before coins
            # self.update_background()
            self.draw_background()

            # update coins' positions and draw them
            self.update_coins()
            self.draw_coins()

            # rect and sub screenshots the entire board as it currently is
            rect = pygame.Rect((0, 0), settings.board_size)
            sub = screen.subsurface(rect)
            pos = (settings.board_size[0]//2, settings.board_size[1]//2)

            # blitRotate was completely "inspired" by the post on StackOverflow
            # pos is inputted twice to center the spinning axis and the center
            # of the board, THIS ONLY WORKS FOR A SQUARE BOARD, will need
            # changes for a rectangular board
            blitRotate(screen, sub, pos, pos, angle)

            if angle == target_angle:
                if is_rotating:
                    # just finished a rotation
                    clockwise = target_angle < 0

                    # reset rotation variables
                    is_rotating = False
                    target_angle = 0
                    angle = 0

                    self.rotate_board(clockwise)
            else:
                angle += increment

            # update the whole display Surface
            pygame.display.flip()

        # exited game loop: someone has won, so say that they've won
        self.game_over.set_winner(self.state)
        self.game_over.show()

# functions that are less closely tied to game objects go below


def blitRotate(surf, image, pos, originPos, angle):

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
    rotated_image = pygame.transform.rotate(image, angle)

    # rotate and blit the image
    surf.blit(rotated_image, origin)

    # draw rectangle around the image
    pygame.draw.rect(surf, (255, 0, 0),
                     (*origin, *rotated_image.get_size()), 2)


def closest_column(board, mouse_pos):
    """
    Returns the column number in `board` closest to the given mouse position.
    """
    x_pos = mouse_pos[0]
    col = int(math.floor(x_pos / board.cell_length))

    print(f"dropped at col {col}.")

    return col


def get_next_open_row(board, col):
    """
    Finds the topmost vacant cell in column `col`, in `board`'s grid.
    Returns that cell's corresponding row index.
    """
    n_rows = board.n_rows

    # check row by row, from bottom row to top row ([0][0] is topleft of grid)
    for row in range(n_rows - 1, -1, -1):
        if board.grid[row][col] == 0:
            return row

    # so pylint doesn't complain
    return None
