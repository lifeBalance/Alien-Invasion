import pygame

class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (69, 69, 69)

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 255, 255) # Color white
        self.bullets_allowed = 3

        # Alien settings
        self.fleet_drop_speed = 10

        # General setting for controlling speeds (increases with levels)
        self.speedup_scale = 1.0

        # Sounds
        self.boom = pygame.mixer.Sound('assets/sounds/boom.wav')
        self.laser = pygame.mixer.Sound('assets/sounds/laser.wav')
        self.explosion = pygame.mixer.Sound('assets/sounds/explosion.wav')
        self.start = pygame.mixer.Sound('assets/sounds/start2.wav')
        self.game_over = pygame.mixer.Sound('assets/sounds/game_over.wav')

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 2.5
        self.bullet_speed = 5.0
        self.alien_speed = 1.0
        # We'll multiply by 1 to go to the right; and by -1 to go to the left.
        self.fleet_direction = 1
        
        # Scoring settings
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings of all movable game elements."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale