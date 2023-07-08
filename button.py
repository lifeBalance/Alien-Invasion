import pygame.font # Module to render text on the screen.

class Button:
    """A class to build buttons for the game."""

    def __init__(self, ai_game, msg):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50   # Button size.
        self.bg_color = (255, 255, 255)     # Dark grey background.
        self.button_color = (90, 90, 90)     # Dark grey background.
        self.text_color = (255, 255, 255)   # White text.
        self.font = pygame.font.SysFont(None, 48)

        # Build the button (made up by 2 rectangles) and center it.
        # In order to draw a thin border on the button, we had to create a
        # slightly bigger rectangle behind the button rectangle.
        self.bg_rect = pygame.Rect(0, 0, self.width + 2, self.height + 2)
        self.btn_rect = pygame.Rect(0, 0, self.width, self.height)
        # Center the rectangles.
        self.btn_rect.center = self.screen_rect.center
        self.bg_rect.center = self.screen_rect.center

        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        # Convert the text in the msg parameter to an image (True = antialiasing).
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.btn_rect.center

    def draw_button(self):
        """Draw blank button and then draw the message."""
        # Draw the background rectangle (stored in self.bg_rect) before the btn.
        self.screen.fill(self.bg_color, self.bg_rect)
        # Draw the button rectangle (stored in self.bg_rect) on top of it.
        self.screen.fill(self.button_color, self.btn_rect)
        # Draw the text image on top of the button.
        self.screen.blit(self.msg_image, self.msg_image_rect)