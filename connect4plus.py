import pygame
import pygame_gui

from settings import Settings
from game import Game, in_board
from music import Music
from menu import Menu


def run():
    """Main game function."""

    settings = Settings()

    # create game process and set display size and title
    pygame.init()
    screen = pygame.display.set_mode(settings.screen_size)
    pygame.display.set_caption("lorem ipsum")

    clock = pygame.time.Clock()

    game = Game(settings, screen)

    ui_manager = pygame_gui.UIManager(settings.screen_size)

    rotate_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((750, 600), (100, 50)),
        text='Rotate!',
        manager=ui_manager)

    music = Music(settings)

    pygame.mixer.init()

    # create the main menu and run the menu event loop
    menu = Menu(settings, screen, clock)
    menu.run()

    # main game loop
    is_running = True
    while is_running:

        # keep framerate at 120 (not sure if this works)
        time_delta = clock.tick(120)/1000.0

        game.draw_background()

        # handle events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                # close window clicked: stop the game
                is_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # mouse click detected: drop coin
                mouse_pos = pygame.mouse.get_pos()
                if in_board(game.board, mouse_pos):
                    game.drop_coin(mouse_pos)
                    music.play("coin_drop")
                else:
                    menu.run()

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == rotate_button:
                        print('Rotated')

            ui_manager.process_events(event)

        ui_manager.update(time_delta)
        ui_manager.draw_ui(screen)

        # update coins' positions and draw them
        game.update_coins()
        game.draw_coins()

        # update the whole display Surface
        pygame.display.flip()



# only run() if this python module is the one being run (not when imported)
if __name__ == "__main__":
    run()
