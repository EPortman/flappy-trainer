import os

import pygame
from dotenv import load_dotenv

load_dotenv()


class Bird:
    def __init__(self):
        """
        Initialize the bird.
        """
        try:
            self.x = int(os.getenv("BIRD_START_X_POS"))
            self.y = int(os.getenv("BIRD_START_Y_POS"))
            self.radius = int(os.getenv("BIRD_RADIUS"))
            self.color = tuple(map(int, os.getenv("BIRD_COLOR").split(",")))
            self.velocity = 0
        except TypeError:
            raise EnvironmentError(
                "One or more required environment variables are missing: "
                "BIRD_START_X_POS, BIRD_START_Y_POS, BIRD_RADIUS, BIRD_COLOR"
            )

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
