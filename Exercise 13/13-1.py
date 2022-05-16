import sys
import pygame
from star import Star
from settings import Settings
from random import randint

class Stars:
    """Overall class to manage assets and behaviour."""

    def __init__(self):
        """Initialise the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Stars")
        self.star = Star(self)
        self.stars = pygame.sprite.Group()
        self._create_fleet()
        
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._update_screen()
            self._check_events()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.star.blitme()
        self.stars.draw(self.screen)


        #Make the most recently drawn screen visible.
        pygame.display.flip()

    def _check_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_END:
                    sys.exit()

    def _create_fleet(self):
        """Create a fleet of stars."""
        #Make an star and find the number of stars in a row.
        #Spacing between each star is equal to one star width.
        star = Star(self)
        star_width, star_height = star.rect.size
        available_space_x = self.settings.screen_width - (4*star_width)
        number_stars_x = available_space_x // (2 * star_width)

        #Determine the number of rows of stars that fit on the screen.
        available_space_y = (self.settings.screen_height - (4* star_height))
        number_rows = available_space_y // (2 * star_height)

        #Create the full fleet of stars.
        for row_number in range(number_rows):
        #Create the first row of stars.
            for star_number in range(number_stars_x):
            #Create the first row of stars.
                self._create_star(star_number, row_number)

    def _create_star(self, star_number, row_number):
        """Create an star and place it in a row"""
        random_number = randint(-10, 10)
        star = Star(self)
        star_width, star_height = star.rect.size
        star.rect.x = 2 *star_width + (2 * star_width) * star_number
        star.rect.y = 2 *star_height + (2 * star_height) * row_number

        star.rect.x += random_number
        star.rect.y += random_number

        self.stars.add(star)      


star = Stars()
star.run_game()