import sys

import pygame

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create the game resources."""
        pygame.init()
        # The clock controls the frame rate of the game
        self.clock = pygame.time.Clock()
        # Set the size of the window
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Alien Invasion")
        # Set the background color of the window (using RGB)
        self.bg_color = (100, 100, 100)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events (Event loop).
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Paint the screen on each iteration, using the bg_color
            self.screen.fill(self.bg_color)
            # Make the most recently drawn screen visible.
            pygame.display.flip()
            # Make the loop run 60 times per second
            self.clock.tick(60)

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()