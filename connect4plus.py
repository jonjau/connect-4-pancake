from enum import Enum
import itertools

import pygame

from coin import Coin
from board import Board
from settings import Settings

import game_functions as game


class GameState(Enum):
    """Enum representing a game state. UNUSED"""
    PLAYER_1 = 0
    PLAYER_2 = 1

GAME_STATES = itertools.cycle([0, 1])

class Game:
    """Class representing the state of the game. UNUSED"""

    def __init__(self):
        """Initialise settings and game state."""

        self.settings = Settings()

        # whose turn it currently is; player 1 is 0, player 2 is 1.
        # initially it is player 1's turn
        self.state = next(GAME_STATES)

    def next_turn(self):
        """go to the next turn."""
        self.state = next(GAME_STATES)


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
                # mouse click detected: create a coin at that position
                mouse_pos = pygame.mouse.get_pos()
                coins.add(Coin(state, settings, screen, mouse_pos))
                state = next(GAME_STATES)

        # update the positions of coins and draw them
        game.update_coins(coins)

        # update the whole display Surface
        pygame.display.flip()

        # keep framerate at 120
        clock.tick(120)

# if this python module is the one being run (not when it is imported)
if __name__ == "__main__":
    # GAME = Game()
    # GAME.run()
    run()
