import pygame
from utils import get_env_var_as_int, get_env_var_as_tuple


class Bird:
    def __init__(self):
        """Initialize the bird."""
        self.x = get_env_var_as_int("BIRD_START_X_POS")
        self.y = get_env_var_as_int("BIRD_START_Y_POS")
        self.radius = get_env_var_as_int("BIRD_RADIUS")
        self.color = get_env_var_as_tuple("BIRD_COLOR")
        self.flap_force = get_env_var_as_int("BIRD_FLAP_FORCE")
        self.velocity = 0
        self.is_alive = True

    def update(self):
        """Update the bird's y position based on velocity and gravity."""
        self.velocity += 0.5
        self.y += self.velocity

    def flap(self):
        """Make the bird flap upwards by adjusting the velocity."""
        self.velocity = self.flap_force

    def get_rect(self) -> pygame.Rect:
        """Return the bird's bounding rectangle for collision detection."""
        return pygame.Rect(
            self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2
        )

    def die(self):
        """Kill the bird ending the game"""
        self.is_alive = False

    def draw(self, screen: pygame.Surface):
        """
        Draw the bird on the screen as a circle.
        :param screen: The Pygame surface to draw the bird on
        """
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def reset(self):
        """Reset the bird's position and velocity."""
        self.x = get_env_var_as_int("BIRD_START_X_POS")
        self.y = get_env_var_as_int("BIRD_START_Y_POS")
        self.velocity = 0
        self.is_alive = True
