from enum import Enum
import itertools
import math

import pygame

from coin import Coin
from board import Board
from settings import Settings

import game_functions as game


class GameState(Enum):
    """Enum representing a game state. UNUSED"""
    PLAYER_1 = 0
    PLAYER_2 = 1

class Game:
    """Class representing the state of the game. UNUSED"""

    def __init__(self, screen):
        """Initialise settings and game state."""

        self.settings = Settings()
        self.screen = screen

        # whose turn it currently is; player 1 is 0, player 2 is 1.
        # initially it is player 1's turn
        self.state = next(GAME_STATES)

    def next_turn(self):
        """go to the next turn."""
        self.state = next(GAME_STATES)

GAME_STATES = itertools.cycle([1, 2])

def run():
    """Main game function."""

    settings = Settings()
    state = next(GAME_STATES)

    # create game process and set display size and title
    pygame.init()
    screen = pygame.display.set_mode(settings.board_size)
    pygame.display.set_caption("lorem ipsum CLICK TO DROP COINS")

    # create sprites, they aren't drawn yet
    coins = pygame.sprite.Group()
    board = Board(settings, screen)
    #board = pygame.image.load("assets/tile1.png")
    #screen.blit(board, (20, 20))

    clock = pygame.time.Clock()

    # main game loop
    running = True
    while running:

        # redraw reddish background, and the board
        screen.fill((100, 10, 10))
        board.draw()

        # handle events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                # close window clicked: stop the game
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # mouse click detected: create a coin at the top of the
                # closest column

                mouse_pos = pygame.mouse.get_pos()
                col = closest_column(board, mouse_pos)
                row = get_next_open_row(board, col)

                # ugly
                start_pos = board.rects[0][col].center

                coins.add(Coin(state, settings, screen, start_pos,
                               board.rects[row][col].center))

                drop_coin(board, col, state)

                # next player's turn now
                state = next(GAME_STATES)

        # update the positions of coins and draw them
        game.update_coins(coins)

        # update the whole display Surface
        pygame.display.flip()

        # keep framerate at 120
        clock.tick(120)


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

def drop_coin(board, col, player):
    row = get_next_open_row(board, col)

    board.grid[row][col] = player

    print(board.grid)


# only run() if this python module is the one being run (not when imported)
if __name__ == "__main__":
    run()

