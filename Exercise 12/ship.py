import pygame

class Ship:
    """A Class to manage the ship."""

    def __init__(self, ai_game):
        """Initialise the ship and set its starting position."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #Load the ship image and get its rect.
        self.image = pygame.image.load('Exercise 12\images\ship - Copy.bmp')
        self.rect = self.image.get_rect()

        #Start each new ship at the left side of the screen.
        self.rect.midleft = self.screen_rect.midleft

        #Store a decimal value for the ship's horizontal position.
        self.y = float(self.rect.y)

        #Movement flags
        self.moving_up = False
        self.moving_down = False


    def update(self):
        """Update the ship's position based on movement flags."""
        #Update the ship's y value, not the rect.
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        #Update rect object from self.x.
        self.rect.y = self.y

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
