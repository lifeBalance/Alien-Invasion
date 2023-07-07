import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then correct its position.
        self.rect = pygame.Rect(
            # Rect takes:
            # - coordinates of left corner of the rectangle: 0, 0
            # - width of the rectangle (defined in settings)
            # - height of the rectangle (defined in settings)
            0,
            0,
            self.settings.bullet_width,
            self.settings.bullet_height,
        )
        # The midtop of the bullet matches the midtop of the ship!
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position as float.
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen."""
        # Update the y coordinate of the bullet (vertically in straight line).
        self.y -= self.settings.bullet_speed  # Going up, decrease y!
        # Update the y coordinate of the rectangle position using the y property 
        # of the bullet.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
