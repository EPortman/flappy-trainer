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

    def move(self, speed):
        self.x_pos -= speed

    def draw(self, screen):
        pygame.draw.rect(
            screen, self.color, pygame.Rect(self.x_pos, 0, self.width, self.top_height)
        )
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(
                self.x_pos, self.bottom_height, self.width, screen.get_height() - self.bottom_height
            ),
        )

    def is_off_screen(self):
        return self.x_pos + self.width < 0
