import pygame

class Coin(pygame.sprite.Sprite):
    """Class representing a coin in the game."""

    def __init__(self, player, settings, screen, start_pos, end_pos):
        """Initialise the coin and set its starting and ending position."""
        # construct the parent pygame.Sprite of this Coin
        super().__init__()

        # each Coin owns a reference to screen
        self.screen = screen

        # load the coin image, and set its rect attribute
        image = pygame.image.load(settings.coin_image_paths[player])
        self.image = pygame.transform.scale(image, settings.cell_size)
        self.rect = self.image.get_rect()

        # start each new coin at the position given as input
        self.rect.centery, self.rect.centerx = start_pos

        self.end_pos = end_pos

        # store (a copy of) the coin's vertical position
        self.y_pos = float(self.rect.y)

        # coin starts off falling
        self.is_falling = True
        self.fall_speed = settings.coin_fall_speed
        
    def draw(self):
        """Draw the coin at its current position."""
        self.screen.blit(self.image, self.rect)

    def is_at_the_bottom(self):
        """Return true if coin is at its ending position."""

        #screen_rect = self.screen.get_rect()
        return self.rect.centery >= self.end_pos[0]

    def update(self):
        """Update the coin's position."""

        if self.is_falling:

            # TODO: y_pos: redundant variable?
            self.y_pos += (self.fall_speed)
            self.rect.y = self.y_pos
