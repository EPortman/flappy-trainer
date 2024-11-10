import pygame
from utils import get_env_var_as_int, get_env_var_as_tuple


class Bird:
    def __init__(self):
        """
        Initialize the bird.
        """
        self.x = get_env_var_as_int("BIRD_START_X_POS")
        self.y = get_env_var_as_int("BIRD_START_Y_POS")
        self.radius = get_env_var_as_int("BIRD_RADIUS")
        self.color = get_env_var_as_tuple("BIRD_COLOR")
        self.velocity = 0
        self.is_alive = True

    def update(self):
        """
        Update the bird's position based on velocity and gravity.
        """
        self.velocity += 0.5  # Gravity effect
        self.y += self.velocity

    def flap(self):
        """
        Make the bird flap upwards by adjusting the velocity.
        """
        self.velocity = -8  # Move the bird upwards

    def get_rect(self):
        """Return the bird's bounding rectangle for collision detection."""
        return pygame.Rect(
            self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2
        )

    def die(self):
        self.is_alive = False

    def draw(self, screen):
        """
        Draw the bird on the screen as a circle.
        :param screen: The Pygame surface to draw the bird on
        """
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def reset(self, x, y):
        """
        Reset the bird's position and velocity.
        :param x: New x position
        :param y: New y position
        """
        self.x = x
        self.y = y
        self.velocity = 0
