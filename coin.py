import pygame


class Coin(pygame.sprite.Sprite):
    """Class representing a coin in the game."""

    def __init__(self, settings, screen, state, start_pos, end_pos, music):
        """Initialise the coin and set its starting and ending position."""

        # construct the parent pygame.Sprite of this Coin
        super().__init__()

        # each Coin owns a reference to screen
        self.screen = screen

        self.music = music
        # load the coin image, and set its rect attribute
        image = pygame.image.load(settings.coin_image_paths[state])
        self.image = pygame.transform.scale(image, settings.cell_size)
        self.rect = self.image.get_rect()

        # start each new coin at the position given as input
        # each coin has a predefined destination: end_pos
        self.rect.centery, self.rect.centerx = start_pos
        self.end_pos = end_pos

        # coin starts off falling, constant speed
        self.is_falling = True
        self.fall_speed = settings.coin_fall_speed

    def draw(self):
        """Draw the coin at its current position."""

        self.screen.blit(self.image, self.rect)

    def is_done_falling(self):
        """Return true if coin is at its ending position."""

        return self.rect.centery >= self.end_pos[0]

    def update(self):
        """Update this coin's position."""

        if self.is_falling:
            if self.is_done_falling():
                self.music.play('coin_drop')
                self.is_falling = False
            else:
                self.rect.y += (self.fall_speed)
