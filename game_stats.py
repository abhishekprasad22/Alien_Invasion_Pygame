class GameStats:
    """Track statistics for alien invasion."""

    def __init__(self, ai_game):
        """Initialize ststistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        # Start alien invasion in an inactive state
        self.game_active = False
        # High score should never be reset.
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can ahange during the game."""
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1