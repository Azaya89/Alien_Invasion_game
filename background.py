import pygame
from pygame.sprite import Sprite

class GameBackground(Sprite):
    """Add background image to the game."""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images\space-triangle.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = 0,0