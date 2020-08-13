import pygame

class Coin(pygame.sprite.Sprite):
    """Class representing a coin in the game."""

    def __init__(self, state, settings, screen, start_pos):
        """Initialise the coin and set its starting position."""
        # construct the parent pygame.Sprite of this Coin
        super().__init__()

        # each Coin owns a reference to screen and settings
        self.screen = screen
        self.settings = settings

        # load the coin image, and set its rect attribute
        image = pygame.image.load(settings.coin_image_paths[state])
        self.image = pygame.transform.scale(image, settings.coin_size)
        self.rect = self.image.get_rect()

        # start each new coin at the position given as input
        self.rect.centerx, self.rect.centery = start_pos

        # store (a copy of) the coin's vertical position
        self.y_pos = float(self.rect.y)

        # coin starts off falling
        self.is_falling = True

    def draw(self):
        """Draw the coin at its current position."""
        self.screen.blit(self.image, self.rect)

    def is_at_the_bottom(self):
        """Return true if coin is at the bottom of the screen."""

        screen_rect = self.screen.get_rect()
        return self.rect.bottom >= screen_rect.bottom

    def update(self):
        """Update the coin's position."""

        if self.is_falling:
            self.y_pos += (self.settings.coin_fall_speed)
            self.rect.y = self.y_pos
