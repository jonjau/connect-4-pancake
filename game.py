import itertools
import math
import sys
import random

import numpy as np

import pygame
from pygame.locals import *
import pygame_gui

from coin import Coin
from board import Board
from interface import Interface, GameOver
from background import Background

# mouse button constants as defined by pygame
LEFT_MOUSE_BUTTON = 1
RIGHT_MOUSE_BUTTON = 2

# whose turn it currently is; player 1 is 1, player 2 is 2.
GAME_STATES = itertools.cycle([1, 2])
PLAYER_DICT = {1: "Yellow", 2: "Red"}


class Game:
    """
    Class containing the game state, objects and functions that modify them.
    """

    def __init__(self, settings, screen, music, clock, game_mode='sandbox'):
        """Initialise settings and game state."""

        # Game owns a reference to settings and screen
        self.settings = settings
        self.screen = screen

        # to reset to when game is over
        self.original_n_cols = settings.n_cols
        self.original_n_rows = settings.n_rows

        self.music = music
        self.clock = clock
        self.game_mode = game_mode

        print(f"playing in game_mode: '{game_mode}'.")

        self.ui_manager = pygame_gui.UIManager(settings.screen_size)
        self.interface = Interface(self.ui_manager, settings, screen, clock)
        self.ui_elements = self.interface.init_elements()

        # create game objects, they aren't drawn yet
        self.coins = pygame.sprite.Group()
        self.board = Board(settings, screen)
        self.background = Background(settings, screen)

        # initially it is player 1's turn
        self.next_turn()

    def next_turn(self):
        """Go to the next turn."""
        self.state = next(GAME_STATES)
        
        self.update_interface()

    def update_interface(self):
        """Update the interface to say whose turn it currently is."""

        self.ui_elements['player'].set_text(
            f"{PLAYER_DICT[self.state]}'s turn.")
        

    def draw_background(self):
        """Draw the screen background, and the game board over it."""

        self.screen.blit(self.background.image, (0, 0))
        self.board.draw()

    def drop_coin(self, mouse_pos):
        """Drop one coin from the top of the column closest to `mouse_pos`"""
        board = self.board
        board_xy = (self.settings.padding_left, self.settings.padding_top)

        # coin is spawned at the top of the column closest to the mouse
        col = closest_column(board, mouse_pos, self.settings)
        try:
            start_pos = board.rects[0][col].center
        except TypeError:
            return
        
        start_pos = (start_pos[0] + board_xy[1], start_pos[1] + board_xy[0])

        # coin will fall to the next open row
        row = get_next_open_row(board, col)
        try:
            end_pos = board.rects[row][col].center
        except TypeError:
            # if row is full: do nothing
            return

        end_pos = (end_pos[0] + board_xy[1], end_pos[1] + board_xy[0])

        # add it to the group of coin sprites
        self.coins.add(Coin(self.settings, self.screen, self.state,
                            start_pos, end_pos, self.music))
        
        print(f"dropped at col {col}.")

        # place the current player's number at (row, col)
        board.grid[row][col] = self.state

        print(board.grid)


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

    def rotate_board(self, angle):
        """
        Rotate the current board clockwise or anticlockwise, then replaces
        this `Game`'s board and coins to reflect the new state.
        Additionally updates game-wide settings and the screen.
        """
        if angle == -90:
            rotated_grid = np.rot90(self.board.grid, k=1, axes=(1, 0))
        elif angle == 90:
            rotated_grid = np.rot90(self.board.grid, k=1, axes=(0, 1))
        else:
            rotated_grid = np.rot90(self.board.grid, k=2, axes=(0, 1))

        n_rows, n_cols = rotated_grid.shape

        # adjust game-wide settings, then
        # update screen to reflect new board dimensions
        settings = self.settings
        settings.set_board_size(n_rows=n_rows, n_cols=n_cols, adjust=False)
        self.screen = pygame.display.set_mode(self.settings.screen_size)

        # reset board, coins, background
        board = Board(settings, self.screen)
        self.board = board
        self.coins = pygame.sprite.Group()
        self.background = Background(settings, self.screen)
        board_xy = (settings.padding_left, settings.padding_top)

        # from the bottom row up: drop the floating coins
        for row in range(n_rows - 1, -1, -1):
            for col in range(n_cols):

                player = rotated_grid[row][col]

                if player != 0:
                    rotated_grid[row][col] = 0

                    # find where to drop to, and create a coin to drop there
                    landing_row = get_next_open_row(board, col)

                    start_pos = board.rects[row][col].center
                    start_pos = (start_pos[0] + board_xy[1],
                                 start_pos[1] + board_xy[0])

                    end_pos = board.rects[landing_row][col].center
                    end_pos = (end_pos[0] + board_xy[1],
                               end_pos[1] + board_xy[0])

                    self.coins.add(Coin(self.settings, self.screen, player,
                                        start_pos, end_pos, self.music))
                    self.music.play('coin_drop')
                    # update grid
                    board.grid[landing_row][col] = player

    def run(self):
        """Run the game loop, then show game over screen after the game ends."""

        clock = self.clock
        music = self.music
        screen = self.screen
        settings = self.settings
        ui_manager = self.ui_manager
        board = self.board

        angle = 0
        target_angle = 0
        is_rotating = False

        music.play('game')

        # main game loop
        is_running = True
        handling_events = True
        end_game_delay = 100

        # AI mechanics
        bot_mode = self.game_mode == "ai_easy" or self.game_mode == 'ai_hard'
        difficulty = 0 # 0 for easy, 1 for hard
        if self.game_mode == 'ai_hard':
            difficulty = 1
        bot_delay = 80

        while is_running:
            
            # keep framerate at 120 (not sure if this works)
            time_delta = clock.tick(120)/1000.0

            # handle events
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    # close window clicked: stop the game
                    sys.exit()

                if handling_events:
                    if (event.type == pygame.MOUSEBUTTONDOWN and
                            event.button == LEFT_MOUSE_BUTTON and
                            (self.state == 1 or not bot_mode)):
                        # left mouse click detected: drop coin
                        mouse_pos = pygame.mouse.get_pos()
                        bot_delay = 80
                        #if in_board(self.board, mouse_pos):
                        print(mouse_pos)
                        if in_board(board, mouse_pos):
                            self.drop_coin(mouse_pos)
                            if self.check_win():
                                handling_events = False
                            else:
                                self.next_turn()

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

                        elif pressed_keys[K_e]:
                            target_angle += 180
                            angle = target_angle - 180
                            # rotate twice as fast
                            increment = 5.0
                            is_rotating = True
                    
                        elif pressed_keys[K_ESCAPE]:
                            return

                    if event.type == pygame.USEREVENT:
                        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                            # handle button events: copy paste time
                            if (event.ui_element ==
                                    self.ui_elements['rotate_90_clockwise']):
                                target_angle -= 90
                                angle = target_angle + 90
                                increment = -2.5
                                is_rotating = True
                            elif (event.ui_element ==
                                   self.ui_elements['rotate_90_anticlockwise']):
                                target_angle += 90
                                angle = target_angle - 90
                                increment = 2.5
                                is_rotating = True
                            elif (event.ui_element ==
                                    self.ui_elements['rotate_180']):
                                target_angle += 180
                                angle = target_angle - 180
                                increment = 5.0
                                is_rotating = True
                            elif event.ui_element == self.ui_elements['quit']:
                                return

                # let pygame_gui handle internal UI events
                ui_manager.process_events(event)

            # AI mechanics
            if bot_mode and self.state == 2 and not bot_delay:
                self.call_AI(board, settings, difficulty)
            else:
                bot_delay -= 1

            if angle == target_angle:
                if is_rotating:
                    self.rotate_board(target_angle)
                    # reset rotation variables
                    is_rotating = False
                    target_angle = 0
                    angle = 0
                    bot_delay = 80
                    if self.check_win():
                        handling_events = False
                    else:
                        self.next_turn()
            else:
                angle += increment

            if not handling_events and end_game_delay:
                end_game_delay -= 1
            elif not handling_events and not end_game_delay:
                is_running = False

            # draw background before coins
            # self.update_background()
            self.draw_background()

            # update and draw ui elements
            ui_manager.update(time_delta)
            ui_manager.draw_ui(self.screen)

            # update coins' positions and draw them
            self.update_coins()
            self.draw_coins()

            # rect and sub screenshots the entire board as it currently is
            margin_x = settings.padding_left
            margin_y = settings.padding_top
            rect = pygame.Rect((margin_x, margin_y), settings.board_size)
            sub = screen.subsurface(rect)
            pos = (settings.board_size[0] / 2 + margin_x,
                settings.board_size[1] / 2 + margin_y)

            # blitRotate was completely "inspired" by the post on StackOverflow
            # pos is inputted twice to center the spinning axis and the center
            # of the board, THIS ONLY WORKS FOR A SQUARE BOARD, will need
            # changes for a rectangular board
            blit_rotate(screen, sub, pos, pos, angle, margin_x, margin_y)

            # update the whole display Surface
            pygame.display.flip()


        # exited game loop: someone has won, so say that they've won
        game_over = GameOver(settings, screen, clock)
        game_over.set_winner(self.state)
        game_over.show()

        # reset screen size to original
        settings.set_board_size(n_rows=self.original_n_rows,
                                n_cols=self.original_n_cols,
                                adjust=False)
        self.screen = pygame.display.set_mode(self.settings.screen_size)

    def call_AI(self, board, settings, difficulty):
        mouse_pos = (random.randint(
                        settings.padding_left,
                        settings.board_size[0] + settings.padding_left),
                        settings.padding_y+1)
        if difficulty == 0:
            print(mouse_pos)
            self.drop_coin(mouse_pos)
            if self.check_win():
                handling_events = False
            else:
                self.next_turn()
        elif difficulty == 1:
            # prioritise center area
            for i in range(board.n_rows-1, 0, -1):
                for j in range(board.n_cols//2 - 1, board.n_cols//2 + 1):
                    if not board.grid[i][j] and i < 4:
                        mouse_pos = (j*settings.coin_length, 0)
                        break

            # find 3's, try to complete
            target_location = self.check_threes()
            print(target_location)
            if target_location:
                if not board.grid[target_location[0], target_location[1]]:
                    print('smart')
                    mouse_pos = (target_location[0]*settings.coin_length, 0)

            x_pos = mouse_pos[0]
            col = int(math.floor(x_pos / board.cell_length))
            print('AI dropped col ', col)
            self.drop_coin(mouse_pos)

    def check_threes(self):
        connect_num = self.settings.connect_num
        board = self.board
        player = self.state
        n_cols = board.n_cols
        n_rows = board.n_rows

        connect_num -= 1
        # Check horizontal
        for c in range(n_cols - (connect_num - 1)):
            for r in range(n_rows):
                count = 0
                for i in range(connect_num):
                    if board.grid[r][c+i] == player:
                        count += 1
                    if count == connect_num:
                        print('hori')
                        return [r, c+i]

        # Check vertical
        for c in range(n_cols):
            for r in range(n_rows - (connect_num - 1)):
                count = 0
                for i in range(connect_num):
                    if board.grid[r+i][c] == player:
                        count += 1
                    if count == connect_num:
                        print('vert')
                        return [r+i, c]

        # Check left diagonal
        for c in range(n_cols - (connect_num - 1)):
            for r in range(n_rows - (connect_num - 1)):
                count = 0
                for i in range(connect_num):
                    if board.grid[r+i][c+i] == player:
                        count += 1
                    if count == connect_num:
                        print('l diag')
                        return [r+i, c+i]

        # Check right diagonal
        for c in range(n_cols - (connect_num - 1)):
            for r in range((connect_num - 1), n_rows):
                count = 0
                for i in range(connect_num):
                    if board.grid[r-i][c+i] == player:
                        count += 1
                    if count == connect_num:
                        print('r diag')
                        return [r-i, c+i]
        return False

# functions that are less closely tied to game objects go below


def blit_rotate(surf, image, pos, originPos, angle, x, y):

    # calcaulate the axis aligned bounding box of the rotated image
    w, h = image.get_size()
    box = [pygame.math.Vector2(p)
           for p in [(x, -y), (x + w, -y), (x + w, -y - h), (x, -y - h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box = (min(box_rotate, key=lambda p: p[0])[0],
                min(box_rotate, key=lambda p: p[1])[1])
    max_box = (max(box_rotate, key=lambda p: p[0])[0],
                max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot
    pivot = pygame.math.Vector2(originPos[0], -originPos[1])
    pivot_move = pivot.rotate(angle) - pivot

    # calculate the upper left origin of the rotated image
    origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0],
            pos[1] - originPos[1] - max_box[1] + pivot_move[1])

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)

    # rotate and blit the image
    surf.blit(rotated_image, origin)


def in_board(board, pos, settings):
    """returns True if pos (y, x) is within the board's Rect."""
    # x_pos = pos[0]
    # y_pos = pos[1]

    # x_out = (x_pos < 0 or x_pos > settings.board_size[0])
    # y_out = (y_pos < 0 or y_pos > settings.board_size[0])

    # return not (x_out or y_out)
    return bool(board.rect.collidepoint(pos))

def closest_column(board, mouse_pos, settings):
    """
    Returns the column number in `board` closest to the given mouse position.
    """
    
    x_pos = mouse_pos[0] - settings.padding_left
    y_pos = mouse_pos[1] - settings.padding_top

    # restrict the clicked position to be within the board
    if x_pos < 0 or x_pos > settings.board_size[0]:
        return None

    if y_pos < 0 or y_pos > settings.board_size[0]:
        return None

    col = int(math.floor(x_pos / board.cell_length))

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
