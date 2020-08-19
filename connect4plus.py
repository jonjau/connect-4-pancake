import pygame
import pygame_gui

from pygame.locals import *

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

    music = Music(settings)

    pygame.mixer.init()

    # create the main menu and run the menu event loop
    menu = Menu(settings, screen, clock)
    menu.show(music)

    # update screen size to reflect new settings (if modified at all)
    screen = pygame.display.set_mode(settings.screen_size)

    game = Game(settings, screen)

    angle = 0
    target_angle = 0

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

        # draw background before coins
        game.draw_background()

        # update coins' positions and draw them
        game.update_coins()
        game.draw_coins()

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


def blitRotate(surf, image, pos, originPos, angle):

    # calcaulate the axis aligned bounding box of the rotated image
    w, h       = image.get_size()
    box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot
    pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move   = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)

    # rotate and blit the image
    surf.blit(rotated_image, origin)

    # draw rectangle around the image
    pygame.draw.rect (surf, (255, 0, 0), (*origin, *rotated_image.get_size()),2)


# only run() if this python module is the one being run (not when imported)
if __name__ == "__main__":
    run()
