# Standard library modules
import sys
from time import sleep

# 3rd party library modules
import pygame

# Our modules
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star
from button import Button
from scoreboard import Scoreboard

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
        # Instantiate the GameStats before the ship and other elements
        self.stats = GameStats(self)
        # Instantiate Scoreboard to show the stats
        self.sb = Scoreboard(self)
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
        # Start Alien Invasion in an inactive state.
        self.game_active = False
        # Instantiate a Button object
        self.play_button = Button(self, 'Play')

    def _ship_hit(self):
        """Handle the ship being hit by an alien."""
        # Play explosion sound (do it at the top to avoid sound delay.)
        pygame.mixer.Sound.play(self.settings.explosion)

        if self.stats.ships_left > 0:
            # Decrement ships left.
            self.stats.ships_left -= 1
            # Update scoreboard to show ships left.
            self.sb.prep_ships_left()

            # Remove remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create new fleet and center the ship.
            self._create_fleet()
            self.ship._center_ship()

            # Pause
            sleep(2.5)
        else:
            # Play game over sound
            pygame.mixer.Sound.play(self.settings.game_over)
            self.game_active = False
            # Show the cursor again (we need it to click Play!)
            pygame.mouse.set_visible(True)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break # As soon as one alien touches, we change direction.
    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed

        self.settings.fleet_direction *= -1 # Toggle the fleet_direction(1 or -1)

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
        while current_y < (self.settings.screen_height - 5 * alien_height):
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

            if self.game_active:
                # Update the ship position
                self.ship.update()

                # Update the position of the bullets.
                self._update_bullets()
                
                # Update the aliens position
                self._update_aliens()

            # Update the screen
            self._update_screen()

            # Make the loop run 60 times per second
            self.clock.tick(60)

    def _update_aliens(self):
        """
        Check if the fleet touches the screen edge and update the position of
        the alien fleet.
        """
        self._check_fleet_edges()

        # We call update on the aliens group, which internally calls each
        # individual alien update method.
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print('Ship hit!!!') # For now...
            # Restart the game:
            # - Delete all remaining aliens and bullets.
            # - Recenter the ship.
            # - Create new fleet.
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()  # Call .update() for each bullet in the group).

        # Get rid of the bullets that dissapear over the top of the screen (x == 0).
        for bullet in self.bullets.copy():  # The copy is a reference to the same list.
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Check for any bullets that have hit aliens.
        # In case of collision, remove both the bullet and the alien.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        print(collisions)

        # If we hit an alien.
        if collisions: # collisions is a dictionary (empty if no collisions)
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()    # Actually write it to the screen.
            # Update high score in case current score is greater
            self.sb.prep_high_score()
            pygame.mixer.Sound.play(self.settings.boom)

        # If there's no aliens left, repopulate the fleet!
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase the level when alien fleet is anihilated
            self.stats.level += 1
            self.sb.prep_level()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit by alien.
                self._ship_hit()
                break

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks the 'Play' button."""
        button_clicked = self.play_button.btn_rect.collidepoint(mouse_pos)
        # Disable the button when the game is active
        if button_clicked and not self.game_active:
            # Reset the game settings (speed).
            self.settings.initialize_dynamic_settings()
            self._start_game()
    
    def _start_game(self):
        # Play sound
        pygame.mixer.Sound.play(self.settings.start)

        # Reset the game statistics.
        self.stats._reset_stats()   # reset stats
        self.sb.prep_score()        # draw stats to scoreboard
        self.sb.prep_level()        # draw the level
        self.sb.prep_ships_left()   # draw the ships a player have left
        self.game_active = True

        # Remove remaining bullets and aliens.
        self.bullets.empty()
        self.aliens.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship._center_ship()

        # Hide the mouse cursor when the game is active.
        pygame.mouse.set_visible(False)

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
        elif event.key == pygame.K_p:
            self._start_game()

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            # Play laser sound
            pygame.mixer.Sound.play(self.settings.laser)
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

        # Draw the scoreboard
        self.sb.show_score()

        # Paint the button(if the game is inactive) on top of everything else!
        if not self.game_active:
            self.play_button.draw_button()
        # Make the most recently drawn screen visible.
        pygame.display.flip()


if __name__ == "__main__":
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
