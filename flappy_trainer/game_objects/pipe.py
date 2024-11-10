from random import randint

import pygame
from utils import get_env_var_as_int, get_env_var_as_tuple


class Pipe:
    def __init__(self, x_pos=get_env_var_as_int("SCREEN_WIDTH")):
        self.x_pos = x_pos
        self.width = get_env_var_as_int("PIPE_WIDTH")
        self.min_gap_height = get_env_var_as_int("PIPE_MIN_GAP_HEIGHT")
        self.max_gap_height = get_env_var_as_int("PIPE_MAX_GAP_HEIGHT")
        self.color = get_env_var_as_tuple("PIPE_COLOR")
        self.gap_height = randint(self.min_gap_height, self.max_gap_height)
        max_top_height = get_env_var_as_int("SCREEN_HEIGHT") - self.gap_height - 50
        self.top_height = randint(50, max_top_height)
        self.bottom_height = self.top_height + self.gap_height
        self.update_rects()

    def update_position(self, speed):
        """Move the pipe left by a certain speed and update its rectangles."""
        self.x_pos -= speed
        self.update_rects()

    def update_rects(self):
        """Update the position of the top and bottom rectangles based on current x_pos."""
        self.top_rect = pygame.Rect(self.x_pos, 0, self.width, self.top_height)
        self.bottom_rect = pygame.Rect(
            self.x_pos,
            self.bottom_height,
            self.width,
            pygame.display.get_surface().get_height() - self.bottom_height,
        )

    def collides_with(self, bird_rect):
        return bird_rect.colliderect(self.top_rect) or bird_rect.colliderect(self.bottom_rect)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.top_rect)
        pygame.draw.rect(screen, self.color, self.bottom_rect)

    def is_off_screen(self):
        return self.x_pos + self.width < 0
