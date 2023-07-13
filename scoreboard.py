import pygame.font


class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information
        self.text_color = (124, 252, 0)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score image.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()

    def prep_level(self):
        """Turn the level into a rendered image."""
        # Capture the string into a variable
        level_str = str(self.stats.level)
        # Create an image out ouf the string
        self.level_image = self.font.render(
            level_str, True, self.text_color, self.settings.bg_color
        )

        # Place the level indicator below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"{high_score:,}"
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.settings.bg_color
        )

        # Display the high score at the top center of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        # Use the horizontal center of the screen to center the high score
        self.high_score_rect.centerx = self.screen_rect.centerx
        # Use the top of the 'score' to position the 'high score'
        self.high_score_rect.top = self.score_rect.top

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1)  # round to nearest 10
        # In the f-string below, we use a format specifier (:,) is to insert
        # commas to separate thousands.
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color
        )

        # Display the scoreboard at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        # Leave 20 pixels to the right (it will expand to the left)
        self.score_rect.right = self.screen_rect.right - 20
        # Leave 10 pixels at the top
        self.score_rect.top = 10

    def show_score(self):
        """Draw score and level to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
