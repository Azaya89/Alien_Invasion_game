import sys
import pygame
from settings_12_5 import Settings
from characters import Character

class FightGame:
    """Overall class to manage assets and behaviour."""

    def __init__(self):
        """Initialise the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Fight Game")
        self.character = Character(self)
        
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.character.update()
            self._update_screen()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.character.blitme()

        #Make the most recently drawn screen visible.
        pygame.display.flip()

    def _check_events(self):
        """Respond to key presses."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT:
            self.character.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.character.moving_left = True
        elif event.key == pygame.K_UP:
            self.character.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.character.moving_down = True
        elif event.key == pygame.K_END:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key presses"""
        if event.key == pygame.K_RIGHT:
            self.character.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.character.moving_left = False
        if event.key == pygame.K_UP:
            self.character.moving_up = False
        if event.key == pygame.K_DOWN:
            self.character.moving_down = False

    
if __name__ == '__main__':
    #Make a game instance, and run the game.
    fg = FightGame()
    fg.run_game()

