import os

class Settings():
    """A class containing settings for the game."""

    def __init__(self):
        """Initialise the game's static settings."""

        # TODO: screen settings, unused
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # assume .png's can be loaded
        # pygame only guarantees support for .bmp's...

        self.coin_image_paths = {
            0: os.path.join('assets', 'coin1.png'),
            1: os.path.join('assets', 'coin2.png')
        }

        self.tile_image_paths = {
            0: os.path.join('assets', 'tile1.png'),
            1: os.path.join('assets', 'tile2.png')
        }


        self.board_image_path = os.path.join('assets', 'board.png')

        self.coin_length = 100
        self.cell_size = (self.coin_length, self.coin_length)
        self.n_rows = 7
        self.n_cols = 7
        self.board_size = (
            self.n_cols * self.coin_length, self.n_rows * self.coin_length)


        # how fast coins fall
        self.coin_fall_speed = 10
