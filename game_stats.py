class GameStats:
    """Track statistics for alien invasion."""

    def __init__(self, ai_game):
        """Initialize ststistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        # Start alien invasion in an active state
        self.game_active = True

    def reset_stats(self):
        """Initialize statistics that can ahange during the game."""
        self.ship_left = self.settings.ship_limit