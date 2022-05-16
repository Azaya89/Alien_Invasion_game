from ast import Index
import sys
import pygame
from rain_drop import Raindrop

class SteadyRain:
    """Overall class to manage assets and behaviour."""

    def __init__(self):
        """Initialise the game, and create game resources."""
        pygame.init()
        self.screen_width = 1200
        self.screen_height = 750
        self.bg_color = (255, 255, 255)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        # self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        # self.screen_width = self.screen.get_rect().width
        # self.screen_height = self.screen.get_rect().height
        self.raindrop = Raindrop(self)
        self.rain_drops = pygame.sprite.Group()
        self.raindrop_speed = 1
        self._create_rain()
        pygame.display.set_caption("Rain drops")

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.bg_color)
        self.rain_drops.draw(self.screen)
        self.raindrop.blitme()
        # Make the most recently drawn screen visible.
        pygame.display.flip()


    def _check_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_END:
                    sys.exit()

    def _create_raindrop(self, raindrop_number, row_number):
        """Create a raindrop and place it in a row"""
        raindrop = Raindrop(self)
        raindrop_width, raindrop_height = raindrop.rect.size
        raindrop.rect.x = raindrop_width * raindrop_number
        raindrop.rect.y = raindrop_height * row_number

        self.rain_drops.add(raindrop)

    def _create_rain(self):
        """Create rain."""
        #Make a raindrop and find the number of raindrops in a row.
        raindrop = Raindrop(self)
        raindrop_width, raindrop_height = raindrop.rect.size
        available_space_x = self.screen_width
        self.number_raindrops_x = available_space_x // raindrop_width

        #Determine the number of rows of raindrops that fit on the screen.
        available_space_y = self.screen_height // 2
        number_rows = available_space_y // raindrop_height

        for row_number in range(number_rows):
        #Create the first row of raindrops.
            self._create_row(row_number)

    def _create_row(self, row_number):
        """create a single row of raindrops"""
        for raindrop_number in range(self.number_raindrops_x):
        #Create the first row of raindrops.
            self._create_raindrop(raindrop_number, row_number)

    
    def _start_rainfall(self):
        """"Make raindrops fall to bottom of screen and disappear."""
        for raindrop in self.rain_drops.sprites():
            raindrop.rect.y += self.raindrop_speed

    def _update_raindrops(self):
        """Update position of raindrops."""
        self._start_rainfall()
        make_new_drops = False
        for raindrop in self.rain_drops.copy():
            if raindrop.check_bottom():
                self.rain_drops.remove(raindrop)
                make_new_drops = True

        if make_new_drops:
            self._create_row(0)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self._update_raindrops()
            self._update_screen()


rd = SteadyRain()
rd.run_game()
