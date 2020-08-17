import sys

import pygame
import pygame_gui

class Menu:
    """Class representing the main menu."""

    def __init__(self, settings, screen, clock):
        """Initialise the menu's settings, layout, and UI elements."""

        # UIManager keeps track of pygame_gui elements
        self.ui_manager = pygame_gui.UIManager(settings.screen_size)
        self.screen = screen
        self.clock = clock

        self.bg_color = settings.bg_color
        self.title_image = pygame.image.load(settings.title_image_path)

        # menu layout settings
        self.button_width = 0.5 * screen.get_width()
        self.button_height = 50
        self.button_vspace = self.button_height * 1.2
        self.button_size = (self.button_width, self.button_height)

        # initialise rects for positioning and sizing elements
        self.containers = self.init_container_rects()
        self.button_rects = self.init_button_rects()

        # create menu elements, these will be drawn every frame
        self.title_image = pygame_gui.elements.UIImage(
            relative_rect=self.containers['title'],
            image_surface=self.title_image,
            manager=self.ui_manager)

        self.play_button = pygame_gui.elements.UIButton(
            relative_rect=self.button_rects['play'],
            text='Play game',
            manager=self.ui_manager)

        self.tutorial_button = pygame_gui.elements.UIButton(
            relative_rect=self.button_rects['tutorial'],
            text='How to play',
            manager=self.ui_manager)

        self.quit_button = pygame_gui.elements.UIButton(
            relative_rect=self.button_rects['quit'],
            text='Quit',
            manager=self.ui_manager)

    def init_container_rects(self):
        """
        Initialise and returns a dictionary of `Rect`'s representing
        containers for menu elements.
        """
        # root container covers the entire window
        root = pygame.Rect((0, 0), self.screen.get_size())

        # nasty but functional: separates window into two non-overlapping
        # sections, top 25% is title container and bottom 75% is menu container
        title_height = root.height * 0.25
        menu_height = root.height - title_height
        title = root.inflate(0, -menu_height).move(0, -menu_height * 0.5)
        menu = root.inflate(0, -title_height).move(0, title_height * 0.5)

        # within the menu container is a container for buttons, its width is
        # determined by the buttons' width and it has padding on top and bottom
        buttons = menu.inflate(self.button_width - menu.width,
                               -self.button_vspace)

        return {'root': root, 'title': title, 'menu': menu, 'buttons': buttons}

    def init_button_rects(self):
        """
        Initialises and returns a dictionary of `Rect`'s representing buttons.
        """
        topleft = self.containers['buttons'].topleft
        button_size = self.button_size
        vspace = self.button_vspace

        rects = {}
        labels = ['play', 'tutorial', 'quit']

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
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        # handle button events
                        if event.ui_element == self.play_button:
                            is_in_menu = False
                        elif event.ui_element == self.tutorial_button:
                            is_in_menu = False
                        elif event.ui_element == self.quit_button:
                            sys.exit()

                # let pygame_gui handle internal UI events
                ui_manager.process_events(event)

            ui_manager.update(time_delta)
            ui_manager.draw_ui(self.screen)

            pygame.display.flip()
