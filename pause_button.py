import pygame.font

class PauseButton():
    """Create a set of buttons"""

    def __init__(self, ai_game, msg):
        """Initialise button attributes."""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        # Set the dimenasions and properties of the button.
        self.width, self.height = 180, 45
        self.button_color = (30, 30, 230)
        self.text_color = (230, 230, 230)
        self.font = pygame.font.SysFont(None, 45)
        # Build the button's rect object and position it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midleft = self.screen_rect.midleft
        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)