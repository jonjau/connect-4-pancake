import pygame
import pygame_gui

from settings import Settings
from game import Game
from music import Music
from menu import Menu

# mouse button constants as defined by pygame
LEFT_MOUSE_BUTTON = 1
RIGHT_MOUSE_BUTTON = 2


def run():
    """Main game function."""

    settings = Settings()

    # create game process and set display size and title
    pygame.init()
    screen = pygame.display.set_mode(settings.screen_size)
    pygame.display.set_caption("lorem ipsum")

    clock = pygame.time.Clock()

    game = Game(settings, screen)

    music = Music(settings)

    pygame.mixer.init()

    # create the main menu and run the menu event loop
    menu = Menu(settings, screen, clock)
    menu.show()

    # main game loop
    is_running = True
    while is_running:

        # keep framerate at 120 (not sure if this works)
        clock.tick(120)

        # handle events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                # close window clicked: stop the game
                is_running = False

            if (event.type == pygame.MOUSEBUTTONDOWN and
                    event.button == LEFT_MOUSE_BUTTON):
                # left mouse click detected: drop coin
                mouse_pos = pygame.mouse.get_pos()
                game.drop_coin(mouse_pos)
                music.play("coin_drop")

        # draw background before coins
        game.draw_background()

        # update coins' positions and draw them
        game.update_coins()
        game.draw_coins()

        # update the whole display Surface
        pygame.display.flip()


# only run() if this python module is the one being run (not when imported)
if __name__ == "__main__":
    run()
