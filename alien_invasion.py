import sys
import pygame
from settings import Settings
from ship import Ship

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create the game resources."""
        pygame.init()
        # The clock controls the frame rate of the game
        self.clock = pygame.time.Clock()
        # Instantiate the Settings class
        self.settings = Settings()
        # Set the size of the window (using the settings)
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")
        # Set the background color of the window (using RGB)
        self.bg_color = (self.settings.bg_color)
        # Instantiate the Ship class, passing the game to the constructor
        self.ship = Ship(self)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events (Event loop).
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Paint the screen on each iteration, using the bg_color
            self.screen.fill(self.bg_color)
            # Paint the ship
            self.ship.blitme()
            # Make the most recently drawn screen visible.
            pygame.display.flip()
            # Make the loop run 60 times per second
            self.clock.tick(60)


if __name__ == "__main__":
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
