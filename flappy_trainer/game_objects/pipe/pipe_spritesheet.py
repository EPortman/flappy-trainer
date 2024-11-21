"""
PipeSpriteSheet

This module defines the `PipeSpriteSheet` class, which handles loading and managing the
pipe sprite sheet for the Flappy Bird game. The class extracts and scales frames for red
and green pipes, providing utilities to retrieve the appropriate pipe frames for rendering,
including flipping frames based on their position (top or bottom).

Key Features:
- Loads sprite sheet from the specified file path.
- Extracts and scales frames for red and green pipes.
- Provides methods to fetch pipe frames based on color and position.
- Handles configuration dynamically via environment variables.
"""

import pygame

from flappy_trainer.config import (
    PIPE_SPRITE_SHEET_FRAME_HEIGHT,
    PIPE_SPRITE_SHEET_FRAME_WIDTH,
    PIPE_SPRITE_SHEET_PATH,
    PIPE_SPRITE_SHEET_SCALE_FACTOR,
)
from flappy_trainer.utils import PipeColor


class PipeSpriteSheet:
    def __init__(self) -> None:
        """Initialize the pipe sprite sheet, load frames, and apply scaling."""
        self.sprite_sheet = pygame.image.load(PIPE_SPRITE_SHEET_PATH).convert_alpha()
        self._extract_and_scale_frames()

    def get_pipe_frame(self, color: PipeColor, is_top: bool) -> pygame.Surface:
        """
        Retrieve the appropriate pipe frame based on color and position.

        Args:
            color: The color of the pipe (red or green).
            is_top: Indicates whether the pipe is positioned at the top or bottom.

        Returns:
            pygame.Surface: The requested pipe frame, flipped if necessary.
        """
        frame = self._get_frame_by_color(color)
        return self._flip_frame_if_needed(frame, color, is_top)

    def _extract_and_scale_frames(self) -> None:
        """Extract frames for red and green pipes from the sprite sheet, and scale them."""
        self.red_pipe_frame = self._extract_frame(0)
        self.green_pipe_frame = self._extract_frame(PIPE_SPRITE_SHEET_FRAME_WIDTH)
        self.red_pipe_frame = self._scale_frame(self.red_pipe_frame)
        self.green_pipe_frame = self._scale_frame(self.green_pipe_frame)

    def _extract_frame(self, x_offset: int) -> pygame.Surface:
        """Extract a pipe frame from the sprite sheet given an x-coordinate offset."""
        frame_rect = pygame.Rect(
            x_offset, 0, PIPE_SPRITE_SHEET_FRAME_WIDTH, PIPE_SPRITE_SHEET_FRAME_HEIGHT
        )
        return self.sprite_sheet.subsurface(frame_rect).copy()

    def _scale_frame(self, frame: pygame.Surface) -> pygame.Surface:
        """Scale a frame by the scaling factor provided in the configuration."""
        new_dimensions = (
            int(PIPE_SPRITE_SHEET_FRAME_WIDTH * PIPE_SPRITE_SHEET_SCALE_FACTOR),
            int(PIPE_SPRITE_SHEET_FRAME_HEIGHT * PIPE_SPRITE_SHEET_SCALE_FACTOR),
        )
        return pygame.transform.scale(frame, new_dimensions)

    def _get_frame_by_color(self, color: PipeColor) -> pygame.Surface:
        """Return the correct frame based on pipe color"""
        if color == PipeColor.RED:
            return self.red_pipe_frame
        elif color == PipeColor.GREEN:
            return self.green_pipe_frame
        else:
            raise ValueError(f"Invalid pipe color specified: '{color}'. Must be 'red' or 'green'.")

    @staticmethod
    def _flip_frame_if_needed(
        frame: pygame.Surface, color: PipeColor, is_top: bool
    ) -> pygame.Surface:
        """Flip the frame vertically if required based on the pipe's color and position."""
        if (color == PipeColor.RED and is_top) or (color == PipeColor.GREEN and not is_top):
            return pygame.transform.flip(frame, False, True)
        return frame
