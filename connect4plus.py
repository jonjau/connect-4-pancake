import pygame

from settings import Settings
from game import Game


def run():
    """Main game function."""

    settings = Settings()

    # create game process and set display size and title
    pygame.init()
    screen = pygame.display.set_mode(settings.screen_size)
    pygame.display.set_caption("lorem ipsum")

    clock = pygame.time.Clock()

    game = Game(settings, screen)

    # main game loop
    running = True
    while running:

        game.draw_background()

        # handle events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                # close window clicked: stop the game
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # mouse click detected: drop coin
                mouse_pos = pygame.mouse.get_pos()
                game.drop_coin(mouse_pos)

        # update coins' positions and draw them
        game.update_coins()
        game.draw_coins()

        # update the whole display Surface
        pygame.display.flip()

        # keep framerate at 120 (not sure if this works)
        clock.tick(120)


# only run() if this python module is the one being run (not when imported)
if __name__ == "__main__":
    run()
