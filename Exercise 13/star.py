import pygame
from pygame.sprite import Sprite

class Star(Sprite):
    """A class to represent a single star in the fleet."""

    def __init__(self, ai_game):
        """Initialise the star and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen

        #Load the star image and set its rect attribute.
        self.image = pygame.image.load(r'Exercise 13\image\redu_star.bmp')
        self.rect = self.image.get_rect()

        #Start each new star near the top left of the screen.
        self.rect.x = 4 * self.rect.width
        self.rect.y = 4 * self.rect.height

        #Store the star's exact horizontal position.
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the star at its current location."""
        self.screen.blit(self.image, self.rect)
