import sys

import pygame
import pygame.freetype

import pygame_gui

PLAYER_DICT = {1: "Yellow", 2: "Red"}

class Interface:
    def __init__(self, ui_manager, settings, screen, clock):

        self.ui_manager = ui_manager
        self.screen = screen
        self.clock = clock

        #self.player_display = 

class GameOver:
    """
    Class representing the 'game over' overlay window.
    Run its event loop with `show()`
    """

    def __init__(self, settings, screen, clock):
        """Initialise the windows's settings, layout, and UI elements."""

        self.ui_manager = pygame_gui.UIManager(settings.screen_size)
        self.settings = settings
        self.screen = screen
        self.clock = clock

        # visual layout parameters
        self.margin = 50
        self.button_size = (0.2 * screen.get_width(), 50)
        self.window_side_length_ratio = 0.5

        self.rects = self.init_rects()

        self.window = pygame.Surface(self.rects['window'].size)
        self.window.fill(settings.bg_color)

        self.font = pygame.freetype.SysFont(name=None, size=26)
        self.text = None

        self.back_button = pygame_gui.elements.ui_button.UIButton(
            relative_rect=self.rects['button'],
            text="Back to menu",
            manager=self.ui_manager
        )

    def init_rects(self):
        """
        Initialise and returns a dictionary of `Rect`'s representing
        containers for the game over window elements
        """
        width, height = self.screen.get_size()
        margin = self.margin
        side = self.window_side_length_ratio * min(width, height)

        # root container covers the entire window
        root = pygame.Rect((0, 0), (width, height))

        # game over window is centered and has length equal to `side`
        window = root.inflate(side - width, side - height)

        # text container is around the top of the game over window, with padding
        text = window.inflate(-margin, -margin)
        text.topleft = (window.x + 0.5 * margin, window.y + 0.5 * margin)

        # button container is around the mid bottom of the game over window,
        # with padding
        button = pygame.Rect((0, 0), self.button_size)
        button.midbottom = window.midbottom
        button.y -= margin

        return {
            "window": window,
            "text": text,
            "button": button
        }

    def set_winner(self, winner):
        """Set the text to be displayed, based on the winner of the game."""

        self.text = self.font.render(f"{PLAYER_DICT[winner]} wins!")[0]

    def show(self):
        """Starts the game over screen event loop."""

        ui_manager = self.ui_manager

        is_in_game_over_screen = True
        while is_in_game_over_screen:
            time_delta = self.clock.tick(120)/1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # close window clicked: stop the game
                    sys.exit()

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        # handle button events
                        if event.ui_element == self.back_button:
                            is_in_game_over_screen = False

                # let pygame_gui handle internal UI events
                ui_manager.process_events(event)

            # draw the window, then the text, then the back button
            self.screen.blit(self.window, self.rects['window'])
            self.screen.blit(self.text, self.rects['text'])

            ui_manager.update(time_delta)
            ui_manager.draw_ui(self.screen)

            pygame.display.flip()
