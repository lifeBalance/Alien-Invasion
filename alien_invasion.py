import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star

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
        # Create a group for the stars
        self.stars = pygame.sprite.Group()
        self._create_stars()
        # The aliens are here!
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row."""
        new_alien = Alien(self)  # Create an Alien instance
        new_alien.x = x_position  # Set its x coordinate
        new_alien.rect.x = x_position  # Set the position of the rectangle horizontally.
        new_alien.rect.y = y_position  # Set the position of the rectangle vertically.
        self.aliens.add(new_alien)  # Add it to the group

    def _create_stars(self):
        """Create a group (list) of 1000 stars of random sizes at random positions."""
        i = 0
        while i < 1000:
            new_star = Star(self)
            self.stars.add(new_star) # Add star to the group
            i += 1
    
    def _create_fleet(self):
        """Create the fleet of aliens."""

        # Instantiate an Alien just to take its dimensions (not created).
        alien = Alien(self)  # Pass an AlienInvasion instance to the Alien constructor.
        # Unpacking the width and height of the first Alien instance.
        alien_width, alien_height = alien.rect.size

        # We'll use these dimensions to separate the aliens.
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y) # CREATE THE ALIEN!
                current_x += 2 * alien_width  # Increment x coord. for next alien
            # Finished a row; reset x coordinates, and increment y coordinates.
            current_x = alien_width # Next row starts at the beginning.
            current_y += 2 * alien_height


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events (Event loop).
            self._check_events()

            # Update the ship position
            self.ship.update()

            # Update the position of the bullets.
            self._update_bullets()

            # Update the screen
            self._update_screen()

            # Make the loop run 60 times per second
            self.clock.tick(60)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()  # Call .update() for each bullet in the group).

        # Get rid of the bullets that dissapear over the top of the screen (x == 0).
        for bullet in self.bullets.copy():  # The copy is a reference to the same list.
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
            # print(len(self.bullets)) # testing (check console)

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
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)  # Pass the ai_game instance to the constructor.
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
        
        # Paint the sky
        for star in self.stars.sprites():
            star.draw_star()

        # Paint the ship
        self.ship.blitme()
        # Paint the aliens
        self.aliens.draw(self.screen)
        # Make the most recently drawn screen visible.
        pygame.display.flip()


if __name__ == "__main__":
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
