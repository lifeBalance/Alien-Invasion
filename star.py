import pygame
from pygame.sprite import Sprite
from random import randint


class Star(Sprite):
    def __init__(self, ai_game):
        """Create a star object at a random position within the screen."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.width = randint(1, 3) # move to settings?
        self.height = randint(1, 3) # move to settings?
        self.x_coord = randint(0, self.settings.screen_width) # move to settings?
        self.y_coord = randint(0, self.settings.screen_height) # move to settings?
        self.color = (255, 255, 255)
        self.rect = pygame.Rect(self.x_coord, self.y_coord, self.width, self.height)
    
    def draw_star(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
