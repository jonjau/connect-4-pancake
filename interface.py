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

        self.padding_top = settings.padding_top
        self.padding_right = settings.padding_right
        self.interface_width = settings.padding_right - settings.padding_left
        self.board_size = settings.board_size
        self.margin = settings.padding_left * 2.5


        self.containers = self.init_containers()

        self.element_width = self.containers['interface'].width
        self.element_height = 50
        self.element_vspace = self.element_height * 1.2
        self.element_size = (self.element_width, self.element_height)

        self.element_rects = self.init_element_rects()


    def init_containers(self):
        """
        Initialise and returns a dictionary of `Rect`'s representing
        containers for interface elements.
        """
        width, height = self.screen.get_size()
        root = pygame.Rect((0, 0), (width, height))

        interface = pygame.Rect((0, 0),
            (self.interface_width - 2 * self.margin, self.board_size[1]))
        interface.topright = (width - self.margin, self.padding_top)

        return {
            "root": root,
            "interface": interface
        }


    def init_element_rects(self):
        """
        Initialises and returns a dictionary of `Rect`'s representing
        positions of UI elements.
        """
        topleft = self.containers['interface'].topleft
        element_size = self.element_size
        vspace = self.element_vspace

        rects = {}
        labels = ['player', 'rotate_90_clockwise',
                  'rotate_90_anticlockwise', 'rotate_180', 'quit']

        # need to add vertical spacing between buttons
        for i, label in enumerate(labels):
            rects[label] = pygame.Rect(
                (topleft[0], topleft[1] + i * vspace), element_size)

        return rects


    def init_elements(self):
        player_display = pygame_gui.elements.ui_label.UILabel(
            relative_rect=self.element_rects['player'],
            text="",
            manager=self.ui_manager
        )

        rotate_90_clockwise_button = pygame_gui.elements.UIButton(
            relative_rect=self.element_rects['rotate_90_clockwise'],
            text="90 clockwise [Q]",
            manager=self.ui_manager
        )

        rotate_90_anticlockwise_button = pygame_gui.elements.UIButton(
            relative_rect=self.element_rects['rotate_90_anticlockwise'],
            text="90 anticlockwise [W]",
            manager=self.ui_manager
        )

        rotate_180_button = pygame_gui.elements.UIButton(
            relative_rect=self.element_rects['rotate_180'],
            text="180 flip [E]",
            manager=self.ui_manager
        )

        quit_game_button = pygame_gui.elements.UIButton(
            relative_rect=self.element_rects['quit'],
            text="Quit game [Esc]",
            manager=self.ui_manager
        )

        return {
            "player": player_display,
            "rotate_90_clockwise": rotate_90_clockwise_button,
            "rotate_90_anticlockwise": rotate_90_anticlockwise_button,
            "rotate_180": rotate_180_button,
            "quit": quit_game_button
        }


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
