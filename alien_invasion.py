import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet


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
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")
        # Set the background color of the window (using RGB)
        self.bg_color = self.settings.bg_color
        # Instantiate the Ship class, passing the game to the constructor
        self.ship = Ship(self)
        # Greate a group for the bullets
        self.bullets = pygame.sprite.Group()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events (Event loop).
            self._check_events()

            # Update the ship position
            self.ship.update()

            # Update the position of the bullets (call .update() for each bullet in the group).
            self.bullets.update()

            # Update the screen
            self._update_screen()

            # Make the loop run 60 times per second
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Move the ship to the left
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        new_bullet = Bullet(self) # Pass the ai_game instance to the constructor.
        self.bullets.add(new_bullet)

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            # Move the ship to the left
            self.ship.moving_left = False

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Paint the screen on each iteration, using the bg_color
        self.screen.fill(self.bg_color)
        # Paint all the bullets in the screen.
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # Paint the ship
        self.ship.blitme()
        # Make the most recently drawn screen visible.
        pygame.display.flip()


if __name__ == "__main__":
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
