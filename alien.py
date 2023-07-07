import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__() # Call constructor of Sprite (parent class)
        self.screen = ai_game.screen

        # Load the settings from ai_game
        self.settings = ai_game.settings

        # Default size for the alien image TODO: ADD TO SETTINGS
        self.default_size = (40, 40)
        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('assets/images/alien.png')
        # Scale the image to your needed size
        self.image = pygame.transform.scale(self.image, self.default_size)

        # Create a rectangle for the image.
        self.rect = self.image.get_rect()

        # Place each new aliean near the top left corner of the screen.
        self.rect.x = self.rect.width # Leave space to the left (alien width)
        self.rect.y = self.rect.height # Leave space at the top (alien height)

        # Store the alien's exact horizontal position (using a float for its x-coord).
        self.x = float(self.rect.x)
    
    def update(self):
        """Move the alien to the right or left (depending on fleet_direction)."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x    # Move the alien rectangle using the x prop.

    def check_edges(self):
        """Return True if alien is at the edge of the screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
