from random import randint

import pygame

from flappy_trainer.config import (
    PIPE_MAX_GAP_HEIGHT,
    PIPE_MIN_GAP_HEIGHT,
    PIPE_MIN_HEIGHT,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from flappy_trainer.game_objects.pipe.pipe_base import PipeBase
from flappy_trainer.utils import PipeColor


class Pipe(PipeBase):
    def __init__(self, pipe_color: PipeColor, x_pos=None, gap_center=None, gap_height=None):
        self._assert_correct_parameters(pipe_color, x_pos, gap_center, gap_height)
        height_of_gap = (
            gap_height
            if gap_height is not None
            else randint(PIPE_MIN_GAP_HEIGHT, PIPE_MAX_GAP_HEIGHT)
        )
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
        """Determine if the pipe has collided with the given bird's rectangle."""
        return bird_rect.colliderect(self.top_pipe_rect) or bird_rect.colliderect(
            self.bot_pipe_rect
        )

    def is_off_screen(self) -> bool:
        """Determine if the pipe has moved completely off the left side of the screen."""
        return self.x_pos + self.width < 0

    def update_position(self, speed: int) -> None:
        """Move the pipe horizontally left by the speed and update its collision boundaries."""
        self.x_pos -= speed
        self.update_rects()

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the top and bottom pipes onto the provided screen surface."""
        self.draw_pipe(screen, is_top=True)
        self.draw_pipe(screen, is_top=False)

    @staticmethod
    def _assert_correct_parameters(
        pipe_color: PipeColor, x_pos: int, gap_center: int, gap_height: int
    ):
        """Validate parameters for creating a pipe."""
        if pipe_color is not None:
            assert (
                pipe_color == PipeColor.RED or pipe_color == PipeColor.GREEN
            ), "Pipe color must be either green or red."
        if gap_height is not None:
            assert (
                PIPE_MIN_GAP_HEIGHT <= gap_height <= PIPE_MAX_GAP_HEIGHT
            ), f"Gap height must be between {PIPE_MIN_GAP_HEIGHT} and {PIPE_MAX_GAP_HEIGHT}."

        if gap_center is not None and gap_height is not None:
            half_gap = gap_height // 2
            min_center = PIPE_MIN_HEIGHT + half_gap
            max_center = SCREEN_HEIGHT - PIPE_MIN_HEIGHT - half_gap
            assert (
                min_center <= gap_center <= max_center
            ), f"Gap center must be between {min_center} and {max_center}. Provided: {gap_center}"

        if x_pos is not None:
            assert x_pos >= 0, f"x_pos must be a non-negative integer. Provided: {x_pos}"
