import sys

import pygame
import pygame.freetype

import pygame_gui as gui


class Menu:
    """Class representing the main menu."""

    def __init__(self, settings, screen, clock):
        """Initialise the menu's settings, layout, and UI elements."""

        # UIManager keeps track of pygame_gui elements
        self.ui_manager = gui.UIManager(settings.screen_size)
        self.screen = screen
        self.clock = clock

        self.bg_color = settings.bg_color
        self.fonts = {
            "large": pygame.freetype.SysFont(None, 32),
            "small": pygame.freetype.SysFont(None, 16),

        }
        title_image = pygame.image.load(settings.title_image_path)

        # menu layout settings
        self.button_width = 0.5 * screen.get_width()
        self.button_height = 50
        self.button_vspace = self.button_height * 1.2
        self.button_size = (self.button_width, self.button_height)
        self.corner_button_size = (0.5 * self.button_width, self.button_height)

        # initialise rects for positioning and sizing elements
        self.containers = self.init_container_rects()
        self.button_rects = self.init_button_rects()

        self.tutorial = Tutorial(settings, screen, clock,
                                 self.containers, self.fonts)
        self.settings_menu = SettingsMenu(settings, screen, clock,
                                          self.containers, self.fonts)

        # create menu elements, these will be drawn every frame
        self.title = gui.elements.UIImage(
            relative_rect=self.containers['title'],
            image_surface=title_image,
            manager=self.ui_manager)

        self.play_button = gui.elements.UIButton(
            relative_rect=self.button_rects['play'],
            text='Play game',
            manager=self.ui_manager)

        self.tutorial_button = gui.elements.UIButton(
            relative_rect=self.button_rects['tutorial'],
            text='How to play',
            manager=self.ui_manager)

        self.settings_button = gui.elements.UIButton(
            relative_rect=self.button_rects['settings'],
            text='Settings',
            manager=self.ui_manager)

        self.quit_button = gui.elements.UIButton(
            relative_rect=self.button_rects['quit'],
            text='Quit',
            manager=self.ui_manager)

    def init_container_rects(self):
        """
        Initialise and returns a dictionary of `Rect`'s representing
        containers for menu elements.
        """
        width, height = self.screen.get_size()

        # root container covers the entire window
        root = pygame.Rect((0, 0), (width, height))

        # nasty but functional: separates window into two non-overlapping
        # sections, top 25% is title container and bottom 75% is menu container
        title_height = root.height * 0.25
        menu_height = root.height - title_height
        title = root.inflate(0, -menu_height)
        title.topleft = (0, 0)
        menu = root.inflate(0, -title_height)
        menu.bottomright = (width, height)

        # within the menu container is a container for buttons, its width is
        # determined by the buttons' width and it has padding on top and bottom
        buttons = menu.inflate(self.button_width - menu.width,
                               -self.button_vspace)
        
        # container for elements at the corners
        margin = self.button_vspace
        topleft = pygame.Rect((0, 0), self.corner_button_size)
        topleft.topleft = (margin, margin)

        bottomright = pygame.Rect((0, 0), self.corner_button_size)
        bottomright.bottomright = (width - margin, height - margin)

        bottomleft = pygame.Rect((0, 0), self.corner_button_size)
        bottomleft.bottomleft = (margin, height - margin)

        return {
            'root': root,
            'title': title,
            'menu': menu,
            'buttons': buttons,
            'topleft': topleft,
            'bottomright': bottomright,
            'bottomleft': bottomleft
        }

    def init_button_rects(self):
        """
        Initialises and returns a dictionary of `Rect`'s representing buttons.
        """
        topleft = self.containers['buttons'].topleft
        button_size = self.button_size
        vspace = self.button_vspace

        rects = {}
        labels = ['play', 'tutorial', 'settings', 'quit']

        # need to add vertical spacing between buttons
        for i, label in enumerate(labels):
            rects[label] = pygame.Rect(
                (topleft[0], topleft[1] + i * vspace), button_size)

        return rects

    def show(self):
        """Starts the main menu event loop."""

        ui_manager = self.ui_manager

        is_in_menu = True
        while is_in_menu:
            time_delta = self.clock.tick(120)/1000.0

            # draw background
            self.screen.fill(self.bg_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # close window clicked: stop the game
                    sys.exit()

                if event.type == pygame.USEREVENT:
                    if event.user_type == gui.UI_BUTTON_PRESSED:
                        # handle button events
                        if event.ui_element == self.play_button:
                            is_in_menu = False
                        elif event.ui_element == self.tutorial_button:
                            self.tutorial.show()
                        elif event.ui_element == self.settings_button:
                            self.settings_menu.show()
                        elif event.ui_element == self.quit_button:
                            sys.exit()

                # let pygame_gui handle internal UI events
                ui_manager.process_events(event)

            ui_manager.update(time_delta)
            ui_manager.draw_ui(self.screen)

            pygame.display.flip()


class Tutorial:
    def __init__(self, settings, screen, clock, containers, fonts):
        self.ui_manager = gui.UIManager(settings.screen_size)
        self.screen = screen
        self.clock = clock

        self.bg_color = settings.bg_color
        tutorial_image = pygame.image.load(settings.tile_image_paths["light"])

        root = pygame.Rect((0, 0), self.screen.get_size())

        # tutorial image takes up the whole window
        self.tutorial = gui.elements.UIImage(
            relative_rect=root,
            image_surface=tutorial_image,
            manager=self.ui_manager)

        # fixed button text and size, button is anchored to bottom right corner
        button_rect = pygame.Rect(0, 0, 200, 50)
        button_rect.bottomright = (-30, -30)

        self.back_button = gui.elements.UIButton(
            relative_rect=containers['bottomright'],
            text='Back to menu',
            manager=self.ui_manager)

    def show(self):

        ui_manager = self.ui_manager

        is_in_tutorial = True
        while is_in_tutorial:
            time_delta = self.clock.tick(120)/1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # close window clicked: stop the game
                    sys.exit()

                if event.type == pygame.USEREVENT:
                    if event.user_type == gui.UI_BUTTON_PRESSED:
                        # handle button events
                        if event.ui_element == self.back_button:
                            is_in_tutorial = False

                # let pygame_gui handle internal UI events
                ui_manager.process_events(event)

            ui_manager.update(time_delta)
            ui_manager.draw_ui(self.screen)

            pygame.display.flip()


class SettingsMenu:
    def __init__(self, settings, screen, clock, containers, fonts):
        self.ui_manager = gui.UIManager(settings.screen_size)
        self.settings = settings
        self.screen = screen
        self.clock = clock

        self.bg_color = settings.bg_color
        self.containers = containers

        # fixed button text and size, button is anchored to bottom right corner
        button_rect = pygame.Rect(0, 0, 200, 50)
        button_rect.bottomright = (-30, -30)

        self.title, _ = fonts["large"].render("Settings")
        self.labels = {
            'title': fonts['large'].render('Settings')[0],
            'rows': fonts['small'].render('number of rows')[0],
            'cols': fonts['small'].render('number of columns')[0],
            'coins': fonts['small'].render('number of coins needed to win')[0],
        }

        self.input_size = (0.5 * screen.get_width(), 50)
        self.input_vspace = 50

        self.input_rects = self.init_input_rects()

        self.rows_input = gui.elements.ui_text_entry_line.UITextEntryLine(
            relative_rect=self.input_rects['rows'][1],
            manager=self.ui_manager)
        self.rows_input.set_allowed_characters('numbers')
        self.rows_input.set_text_length_limit(limit=2)

        self.cols_input = gui.elements.ui_text_entry_line.UITextEntryLine(
            relative_rect=self.input_rects['cols'][1],
            manager=self.ui_manager)
        self.cols_input.set_allowed_characters('numbers')
        self.cols_input.set_text_length_limit(limit=2)

        self.coins_input = gui.elements.ui_text_entry_line.UITextEntryLine(
            relative_rect=self.input_rects['coins'][1],
            manager=self.ui_manager)
        self.coins_input.set_allowed_characters('numbers')
        self.coins_input.set_text_length_limit(limit=2)

        self.save_button = gui.elements.UIButton(
            relative_rect=containers['bottomleft'],
            text='Save changes',
            manager=self.ui_manager)

        self.back_button = gui.elements.UIButton(
            relative_rect=containers['bottomright'],
            text='Back to menu',
            manager=self.ui_manager)

    def init_input_rects(self):
        topleft = self.containers['buttons'].topleft
        input_size = self.input_size
        vspace = self.input_vspace

        rects = {}
        labels = ['rows', 'cols', 'coins']

        # need to add vertical spacing between inputs
        for i, label in enumerate(labels):
            rects[label] = split_rects(pygame.Rect(
                (topleft[0], topleft[1] + i * vspace), input_size), 0.8)

        return rects

    def show(self):

        ui_manager = self.ui_manager

        is_in_settings = True
        while is_in_settings:
            time_delta = self.clock.tick(120)/1000.0

            # draw background and page title on topleft
            self.screen.fill(self.bg_color)
            self.screen.blit(self.labels['title'], self.containers['topleft'])
            self.screen.blit(self.labels['rows'], self.input_rects['rows'][0])
            self.screen.blit(self.labels['cols'], self.input_rects['cols'][0])
            self.screen.blit(self.labels['coins'], self.input_rects['coins'][0])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # close window clicked: stop the game
                    sys.exit()

                if event.type == pygame.USEREVENT:
                    if event.user_type == gui.UI_BUTTON_PRESSED:
                        # handle button events
                        if event.ui_element == self.back_button:
                            is_in_settings = False
                        elif event.ui_element == self.save_button:
                            self.settings.set_board_size(
                                self.settings.n_cols + 1,
                                self.settings.n_rows + 1
                            )
                            print(self.settings.n_cols)

                # let pygame_gui handle internal UI events
                ui_manager.process_events(event)

            ui_manager.update(time_delta)
            ui_manager.draw_ui(self.screen)

            pygame.display.flip()


def split_rects(rect, ratio):
    rect1 = rect.copy()
    rect2 = rect.copy()

    rect1.width = rect.width * ratio
    rect2.width = rect.width * (1 - ratio)
    rect2.x += rect1.width

    return (rect1, rect2)