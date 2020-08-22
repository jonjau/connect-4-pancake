import os

class Settings:
    """A class containing settings for the game."""

    def __init__(self):
        """Initialise the game's static settings."""

        # assume .png's can be loaded
        # pygame only guarantees support for .bmp's
        self.coin_image_paths = {
            1: os.path.join('assets', 'coin1.png'),
            2: os.path.join('assets', 'coin2.png')
        }
        self.tile_image_paths = {
            "light": os.path.join('assets', 'tile_light.png'),
            "dark": os.path.join('assets', 'tile_dark.png')
        }
        self.title_image_path = os.path.join('assets', 'title.png')

        # audio file paths
        self.music_path = {
            "menu_music": os.path.join('assets', 'main_menu_music.wav'),
            "game_music": os.path.join('assets', 'game_music.wav'),
        }
        self.sound_path = {
            "coin_drop": os.path.join('assets', 'coin_drop_sound.wav')
        }

        # board and coin settings, board size is (width,height), in pixels
        self.coin_length = 100
        self.cell_size = (self.coin_length, self.coin_length)
        self.n_rows = 7
        self.n_cols = 7
        self.board_size = (
            self.n_cols * self.coin_length, self.n_rows * self.coin_length)
        self.coin_fall_speed = 10

        # how many coins a player needs to connect to win
        self.connect_num = 4

        # screen settings: for now the board takes up the whole game screen
        self.screen_size = self.board_size
        self.bg_color = (230, 230, 230)

    def set_board_size(self, n_rows, n_cols, adjust=True):
        """
        Sets the board size to `n_rows` x `n_cols`,
        optionally adjusting coin length so that the board size
        (hence screen size) is not changed by much.
        """
        if adjust:
            coin_length = int(min(
                self.board_size[0] / n_cols, self.board_size[1] / n_rows))
        else:
            coin_length = self.coin_length

        self.cell_size = (coin_length, coin_length)
        self.coin_length = coin_length
        self.n_rows = n_rows
        self.n_cols = n_cols
        
        self.board_size = (
            n_cols * self.coin_length,
            n_rows * self.coin_length)

        self.screen_size = self.board_size
