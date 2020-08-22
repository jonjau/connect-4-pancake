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
    pygame.display.set_caption("lorem ipsum")

    clock = pygame.time.Clock()

    music = Music(settings)
    pygame.mixer.init()

    # update screen size to reflect new settings (if modified at all)
    screen = pygame.display.set_mode(settings.screen_size)

    # main game loop
    while True:
        # create the main menu and run the menu event loop
        menu = Menu(settings, screen, clock)
        menu.show(music)

        # update screen size to reflect new settings (if modified at all)
        screen = pygame.display.set_mode(settings.screen_size)

        game = Game(settings, screen, music, clock)
        game.run()


# only run() if this python module is the one being run (not when imported)
if __name__ == "__main__":
    run()

'''
old loop

    is_running = true
    while is_running:

        # keep framerate at 120 (not sure if this works)
        time_delta = clock.tick(120)/1000.0

        # handle events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                # close window clicked: stop the game
                is_running = False

            if (event.type == pygame.MOUSEBUTTONDOWN and
                    event.button == LEFT_MOUSE_BUTTON):
                # left mouse click detected: drop coin
                mouse_pos = pygame.mouse.get_pos()
                self.drop_coin(mouse_pos)
                music.play("coin_drop")

            if (event.type == pygame.KEYDOWN):
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_q]:
                    target_angle -= 90
                    angle = target_angle + 90
                    increment = -2.5
                if pressed_keys[K_w]:
                    target_angle += 90
                    angle = target_angle - 90
                    increment = 2.5

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    # handle button events
                    pass

            ui_manager.process_events(event)

        # draw background before coins
        game.draw_background()

        # update coins' positions and draw them
        game.update_coins()
        game.draw_coins()

        if game.check_win():

            # handle events
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        # handle button events
                        if event.ui_element == back_button:
                            is_running = False

                ui_manager.process_events(event)

            screen.blit(window_surface, game_over_window)
            ui_manager.draw_ui(screen)
            ui_manager.update(time_delta)
            pygame.display.flip()

        # rect and sub screenshots the entire board as it currently is
        rect = pygame.Rect((0, 0), settings.board_size)
        sub = screen.subsurface(rect)
        pos = (settings.board_size[0]//2, settings.board_size[1]//2)

        # blitRotate was completely "inspired" by the post on StackOverflow
        # pos is inputted twice to center the spinning axis and the center of
        # the board, THIS ONLY WORKS FOR A SQUARE BOARD, will need changes
        # for a rectangular board
        blitRotate(screen, sub, pos, pos, angle)

        if angle != target_angle:
            angle += increment

        # update the whole display Surface
        pygame.display.flip()
'''