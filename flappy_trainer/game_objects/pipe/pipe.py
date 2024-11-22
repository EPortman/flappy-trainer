"""
Pipe

This class represents an individual pipe in the Flappy Bird game, including its
position, dimensions, and collision detection logic. It extends the `PipeBase` class,
which handles shared functionality like drawing and updating collision boundaries.

Key Features:
- Dynamically generates gap size and position if not provided.
- Tracks whether the pipe has been passed by the bird.
- Provides public methods for collision detection, position updates, and rendering.
"""

from random import randint

import pygame

from flappy_trainer.config import (
    PIPE_MAX_GAP_HEIGHT,
    PIPE_MIN_GAP_HEIGHT,
    PIPE_MIN_HEIGHT,
    PIPE_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from flappy_trainer.game_objects.pipe.pipe_base import PipeBase
from flappy_trainer.utils import PipeColor


class Pipe(PipeBase):
    def __init__(self, pipe_color: PipeColor, x_pos=None, gap_center=None, gap_height=None):
        self._assert_correct_parameters(pipe_color, x_pos, gap_center, gap_height)
        height_of_gap = gap_height if gap_height is not None else randint(PIPE_MIN_GAP_HEIGHT, PIPE_MAX_GAP_HEIGHT)
        location_of_gap = (
            gap_center
            if gap_center is not None
            else randint(
                PIPE_MIN_HEIGHT + (height_of_gap // 2),
                SCREEN_HEIGHT - PIPE_MIN_HEIGHT - (height_of_gap // 2),
            )
        )
        x_location = x_pos if x_pos is not None else SCREEN_WIDTH
        super().__init__(pipe_color, x_location, location_of_gap, height_of_gap)
        self.passed = False

    def collides_with(self, bird_rect: pygame.Rect) -> bool:
        """Check if the pipe collides with the bird's rectangle."""
        return bird_rect.colliderect(self.top_pipe_rect) or bird_rect.colliderect(self.bot_pipe_rect)

    def is_off_screen(self) -> bool:
        """Check if the pipe has moved off the left side of the screen."""
        return self.x_pos + PIPE_WIDTH < 0

    def update_position(self, distance: int) -> None:
        """Move the pipe left by the specified distance (px) and update its boundaries."""
        self.x_pos -= distance
        self.update_rects()

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the pipe (both top and bottom) onto the screen."""
        self.draw_pipe(screen, is_top=True)
        self.draw_pipe(screen, is_top=False)

    @staticmethod
    def _assert_correct_parameters(pipe_color: PipeColor, x_pos: int, gap_center: int, gap_height: int):
        """Validate the pipe parameters."""
        if not isinstance(pipe_color, PipeColor):
            raise AssertionError("Invalid pipe color. Must be PipeColor.RED or PipeColor.GREEN.")
        if gap_height:
            assert (
                PIPE_MIN_GAP_HEIGHT <= gap_height <= PIPE_MAX_GAP_HEIGHT
            ), f"Gap height must be {PIPE_MIN_GAP_HEIGHT}-{PIPE_MAX_GAP_HEIGHT}."
        if gap_center and gap_height:
            half_gap = gap_height // 2
            min_center = PIPE_MIN_HEIGHT + half_gap
            max_center = SCREEN_HEIGHT - PIPE_MIN_HEIGHT - half_gap
            assert (
                min_center <= gap_center <= max_center
            ), f"Gap center must be {min_center}-{max_center}. Got: {gap_center}."
        if x_pos:
            assert 0 <= x_pos <= SCREEN_WIDTH, "Invalid x pos."
