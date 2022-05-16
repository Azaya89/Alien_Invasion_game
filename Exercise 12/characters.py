import pygame

class Character:
    """A class to manage characters."""

    def __init__(self, fg_game):
        """Initialise the character characteristics."""
        self.screen = fg_game.screen
        self.screen_rect = fg_game.screen.get_rect()
        self.settings = fg_game.settings

        #Load the character image and get its rect.
        self.image = pygame.image.load('Exercise 12\images\sub_zero_redu.bmp')
        self.rect = self.image.get_rect()

        #Place image at center of screen.
        self.rect.center = self.screen_rect.center

        #Store a value for the ship's horizontal and vertical position.
        self.x = self.rect.x
        self.y = self.rect.y

        #Movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False


    def update(self):
        """Update the character's position based on movement flags."""
        #Update the character's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.character_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.character_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.character_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.character_speed
        
        self.rect.x = self.x
        self.rect.y = self.y



    def blitme(self):
        """Draw image at its current location."""
        self.screen.blit(self.image, self.rect)