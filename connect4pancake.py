import pygame

from settings import Settings
from game import Game
from music import Music
from menu import Menu

def run():
    """Main game function."""

    settings = Settings()

    # create game process and set display size and title
    pygame.init()
    screen = pygame.display.set_mode(settings.screen_size)
    pygame.display.set_caption("Connect 4 Pancake")

    clock = pygame.time.Clock()
    music = Music(settings)
    pygame.mixer.init()

    # update screen size to reflect new settings (if modified at all)
    screen = pygame.display.set_mode(settings.screen_size)

    # main game loop
    while True:
        # create the main menu and run the menu event loop
        # retrieve the picked game_mode
        menu = Menu(settings, screen, clock)
        game_mode = menu.show(music)

        # update screen size to reflect new settings (if modified at all)
        screen = pygame.display.set_mode(settings.screen_size)

        game = Game(settings, screen, music, clock, game_mode)
        game.run()


# only run() if this python module is the one being run (not when imported)
if __name__ == "__main__":
    run()
