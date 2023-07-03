import pygame

class Ship:
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        # Default size for the ship image
        self.default_size = (40, 40)

        # Load the ship image and get its rect.
        self.image = pygame.image.load('assets/images/ship.png')
        # Scale the image to your needed size
        self.image = pygame.transform.scale(self.image, self.default_size)
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Movement flags; start with a motionless ship.
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_right:
            self.rect.x += 1
        if self.moving_left:
            self.rect.x -= 1

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)