import itertools
import math

import pygame

from coin import Coin
from board import Board

# whose turn it currently is; player 1 is 1, player 2 is 2.
GAME_STATES = itertools.cycle([1, 2])


class Game:
    """
    Class containing the game state, objects and functions that modify them.
    """

    def __init__(self, settings, screen):
        """Initialise settings and game state."""

        # Game owns a reference to settings and screen
        self.settings = settings
        self.screen = screen

        # initially it is player 1's turn
        self.state = next(GAME_STATES)

        # create game objects, they aren't drawn yet
        self.coins = pygame.sprite.Group()
        self.board = Board(settings, screen)

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
        start_pos = board.rects[0][col].center

        # coin will fall to the next open row
        row = get_next_open_row(board, col)
        end_pos = board.rects[row][col].center

        # add it to the group of coin sprites
        self.coins.add(Coin(self.settings, self.screen, self.state,
                            start_pos, end_pos))

        # place the current player's number at (row, col)
        board.grid[row][col] = self.state

        print(board.grid)

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

# functions that are less closely tied to game objects go below

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

    # FIXME: add error handling here: what if there are no open rows?

def in_board(board, mouse_pos):
    """Returns True if mouse_pos is within `board`, False otherwise."""
    topleft_x, topleft_y = board.rects[0][0].topleft
    bottomright_x, bottomright_y = board.rects[-1][-1].bottomright

    x_pos, y_pos = mouse_pos

    return topleft_x <= x_pos <= bottomright_x and \
           topleft_y <= y_pos <= bottomright_y
