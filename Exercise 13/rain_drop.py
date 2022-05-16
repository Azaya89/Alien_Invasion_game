import pygame
from pygame.sprite import Sprite

class Raindrop(Sprite):
    """A class to represent a single raindrop."""

    def __init__(self, rd_game):
        """Initialise the raindrop and set its starting position."""
        super().__init__()
        self.screen = rd_game.screen
        # self.settings = rd_game.settings

        #Load the raindrop image and set its rect attribute.
        self.image = pygame.image.load(r'Exercise 13\image\redu_raindrop.bmp')
        self.rect = self.image.get_rect()

        #Start each new raindrop near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store the raindrop's exact vertical position.
        self.y = float(self.rect.y)

    def blitme(self):
        """Draw the raindrop at its current location."""
        self.screen.blit(self.image, self.rect)


    def check_bottom(self):
        """Return True if raindrop is at bottom of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.top > screen_rect.bottom:
            return True
        else:
            return False
