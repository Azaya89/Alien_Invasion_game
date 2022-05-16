class Settings:
    """A class to store all settings for Alien Invasion."""
    def __init__(self):
        """Initialise the game's settings."""
        #Screen settings
        self.screen_width = 750
        self.screen_height = 750
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_speed = 1.0

        # Bullet settings
        self.bullet_speed = 0.5
        # self.bullet_width = 3
        self.bullet_width = 15
        # self.bullet_height = 15
        self.bullet_height = 3
        self.bullet_color = (60, 60, 60)
        # self.bullets_allowed = 4