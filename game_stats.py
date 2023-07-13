class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize game statistics."""
        self.settings = ai_game.settings
        self._reset_stats()
        # High score should never be reset.
        self.high_score = 0

    # We want to be able to reset stats every time player starts a new game.
    # (Not only when the program starts.)
    def _reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        # Reset score each time a new game starts
        self.score = 0
        # Player's level
        self.level = 1 # start at 1