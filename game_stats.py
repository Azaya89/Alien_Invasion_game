class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialise statistics."""
        self.settings = ai_game.settings
        # Start Alien Invasion in an active state.
        self.game_active = False
        #High score should never be reset.
        with open("High_Score.txt") as hs:
            high_score = hs.read()
        self.high_score = int(high_score)
        self.reset_stats()


    def reset_stats(self):
        """Initialise statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1