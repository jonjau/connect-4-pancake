import sys

import pygame
import pygame.freetype

import pygame_gui as gui


class Menu:
    """
    Class representing the main menu. Contains other pages as members.
    Run its event loop with `show()`.
    """

    def __init__(self, settings, screen, clock):
        """Initialise the menu's settings, pages, layout, and UI elements."""

        # UIManager keeps track of pygame_gui elements
        self.ui_manager = gui.UIManager(settings.screen_size)
        self.screen = screen
        self.clock = clock

        self.bg_color = settings.bg_color
        self.fonts = {
            "large": pygame.freetype.SysFont(name=None, size=32),
            "small": pygame.freetype.SysFont(name=None, size=16),

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

        # other pages are components of menu, they share much of menu's state
        self.tutorial = Tutorial(settings, screen, clock, self.containers)
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

        # container for elements at the corners, with margins
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
        Initialises and returns a dictionary of `Rect`'s representing
        positions of buttons.
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
    """
    Class representing tutorial menu page. Run its event loop with `show()`.
    """

    def __init__(self, settings, screen, clock, containers):
        """Initialise the tutorial page's tutorial image and UI elements."""

        self.ui_manager = gui.UIManager(settings.screen_size)

        # shared state with main menu
        self.screen = screen
        self.clock = clock
        self.bg_color = settings.bg_color

        # TODO: placeholder tutorial image
        tutorial_image = pygame.image.load(settings.title_image_path)

        # create UI elements: tutorial image takes up the whole window
        self.tutorial = gui.elements.UIImage(
            relative_rect=containers['root'],
            image_surface=tutorial_image,
            manager=self.ui_manager)

        self.back_button = gui.elements.UIButton(
            relative_rect=containers['bottomright'],
            text='Back to menu',
            manager=self.ui_manager)


    def show(self):
        """Starts the tutorial page event loop."""

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
    """
    Class representing settings menu page. Run its event loop with `show()`.
    """

    def __init__(self, settings, screen, clock, containers, fonts):
        """Initialise the setting page's layout and UI elements."""

        self.ui_manager = gui.UIManager(settings.screen_size)

        # shared state with main menu
        self.settings = settings
        self.screen = screen
        self.clock = clock
        self.bg_color = settings.bg_color
        self.containers = containers

        # render text labels, not drawn yet. These are non-pygame_gui.
        self.labels = {
            'title': fonts['large'].render('Settings')[0],
            'rows': fonts['small'].render('Number of rows:')[0],
            'cols': fonts['small'].render('Number of columns:')[0],
            'coins': fonts['small'].render('Number of coins needed to win:')[0],
        }

        # slightly magical, but not tied to program logic: purely for layout
        self.input_size = (0.5 * screen.get_width(), 50)
        self.input_vspace = 50
        self.input_col_ratio = 0.8

        # initialise "settings menu"-specific element layout
        self.input_rects = self.init_input_rects()

        # create menu elements, these will be drawn every frame
        # for n_rows, n_cols, and connect_num allow numbers 1 to 99,
        # 0 will lead to no-op when saved
        self.rows_input = gui.elements.ui_text_entry_line.UITextEntryLine(
            relative_rect=self.input_rects['rows'][1],
            manager=self.ui_manager)
        self.rows_input.set_allowed_characters('numbers')
        self.rows_input.set_text_length_limit(limit=2)
        self.rows_input.set_text(str(settings.n_rows))

        self.cols_input = gui.elements.ui_text_entry_line.UITextEntryLine(
            relative_rect=self.input_rects['cols'][1],
            manager=self.ui_manager)
        self.cols_input.set_allowed_characters('numbers')
        self.cols_input.set_text_length_limit(limit=2)
        self.cols_input.set_text(str(settings.n_cols))

        self.coins_input = gui.elements.ui_text_entry_line.UITextEntryLine(
            relative_rect=self.input_rects['coins'][1],
            manager=self.ui_manager)
        self.coins_input.set_allowed_characters('numbers')
        self.coins_input.set_text_length_limit(limit=2)
        self.coins_input.set_text(str(settings.connect_num))

        self.save_button = gui.elements.UIButton(
            relative_rect=containers['bottomleft'],
            text='Save changes',
            manager=self.ui_manager)

        self.back_button = gui.elements.UIButton(
            relative_rect=containers['bottomright'],
            text='Back to menu',
            manager=self.ui_manager)

    def init_input_rects(self):
        """
        Initialises and returns a dictionary of `Rect`'s representing
        positions of inputs.
        """
        topleft = self.containers['buttons'].topleft
        input_size = self.input_size
        vspace = self.input_vspace

        rects = {}
        labels = ['rows', 'cols', 'coins']

        # need to add vertical spacing between inputs
        for i, label in enumerate(labels):
            rects[label] = split_rects(pygame.Rect(
                (topleft[0], topleft[1] + i * vspace),
                input_size),self.input_col_ratio)

        return rects

    def save_settings(self):
        """
        Saves the current settings set in the inputs, modifying
        the game's `Settings` object.
        """
        n_rows = int(self.rows_input.get_text())
        n_cols = int(self.cols_input.get_text())
        connect_num = int(self.coins_input.get_text())

        # don't save if any number is 0, otherwise there'll be division by 0
        if n_rows == 0 or n_cols == 0 or connect_num == 0:
            return

        # modify connect win condition, and board size (hence screen size too)
        self.settings.connect_num = connect_num
        self.settings.set_board_size(n_rows, n_cols)

    def draw_labels(self):
        """
        Draw onto the screen the title and input labels of the settings menu,
        all of which are not managed by `pygame_gui`.
        """
        self.screen.blit(self.labels['title'], self.containers['topleft'])
        self.screen.blit(self.labels['rows'], self.input_rects['rows'][0])
        self.screen.blit(self.labels['cols'], self.input_rects['cols'][0])
        self.screen.blit(self.labels['coins'], self.input_rects['coins'][0])

    def show(self):
        """Starts the settings page event loop."""

        ui_manager = self.ui_manager

        is_in_settings = True
        while is_in_settings:
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
                        if event.ui_element == self.back_button:
                            is_in_settings = False
                        elif event.ui_element == self.save_button:
                            self.save_settings()

                # let pygame_gui handle internal UI events
                ui_manager.process_events(event)

            ui_manager.update(time_delta)
            ui_manager.draw_ui(self.screen)
            
            # draw non-pygame_gui text labels
            self.draw_labels()

            pygame.display.flip()


def split_rects(rect, ratio):
    """
    Splits the given `pygame.Rect` `rect` horizontally into two Rects, with
    the left one having a width of `ratio` * `rect`'s width.
    Returns the left and right Rects as a tuple, in that order.
    """
    rect1 = rect.copy()
    rect2 = rect.copy()

    rect1.width = rect.width * ratio
    rect2.width = rect.width * (1 - ratio)
    rect2.x += rect1.width

    return rect1, rect2
