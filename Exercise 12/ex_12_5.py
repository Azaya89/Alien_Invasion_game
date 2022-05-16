import pygame
import sys

class GameFile:
    """Game file that prints words when keys are pressed."""

    def __init__(self):
        """Initialising attributes of the game file."""
        pygame.init()
        self.bg_color = (255, 255, 255)
        # self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((900, 600))
        pygame.display.set_caption("Game File")

    def run_game(self):
        """Starts the main loop for the game"""
        while True:
            self._check_events()
            self.screen.fill(self.bg_color)
            pygame.display.flip()

    def _check_events(self):
        """Controls key presses"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                print(event.key)
                if event.key == pygame.K_DOWN:
                     print("The DOWN key is being pressed.")              
                if event.key == pygame.K_UP:
                     print("The UP key is being pressed.")
                if event.key == pygame.K_END:
                    sys.exit()

gf = GameFile()
gf.run_game()