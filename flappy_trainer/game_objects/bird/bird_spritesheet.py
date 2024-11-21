"""
BirdSpriteSheet

This class handles loading, managing, and accessing bird animation frames from
a sprite sheet for the Flappy Bird game. It supports frame extraction, cycling through
frames for animations, and retrieving specific frames for bird states.

Key Features:
- Loads and extracts frames from a sprite sheet.
- Provides methods to retrieve specific frames or cycle through animation frames.
- Handles configurable sprite sheet properties like padding and frame dimensions.
"""

import pygame

from flappy_trainer.config import (
    BIRD_SPRITE_SHEET_FRAME_HEIGHT,
    BIRD_SPRITE_SHEET_PADDING_X,
    BIRD_SPRITE_SHEET_PATH,
    BIRD_SPRITE_SHEET_START_Y,
    BIRD_SPRITE_SHEET_TOTAL_FRAMES,
)
from flappy_trainer.utils import BirdFrame


class BirdSpriteSheet:
    def __init__(self) -> None:
        self.sprite_sheet = pygame.image.load(BIRD_SPRITE_SHEET_PATH).convert_alpha()
        self.frames: list[pygame.Surface] = self._load_frames()

    def get_frame(self, frame: BirdFrame) -> pygame.Surface:
        """Retrieve a specific frame from the loaded frames."""
        if 0 <= frame.value < len(self.frames):
            return self.frames[frame.value]
        raise ValueError(
            f"Invalid frame index: {frame.value}. Available frames: 0 to {len(self.frames) - 1}."
        )

    def get_next_frame(
        self, current_frame: BirdFrame, start_frame: BirdFrame, end_frame: BirdFrame
    ) -> BirdFrame:
        """Get the next frame in the animation cycle, wrapping to the start frame if needed."""
        next_value = current_frame.value + 1

        # If next_value exceeds end_frame, wrap around to start_frame
        if next_value > end_frame.value:
            return start_frame

        return BirdFrame(next_value)

    def get_idle_frame(self) -> BirdFrame:
        """Retrieve the frame for the bird's idle state."""
        return BirdFrame.FLAPPING_TOP

    def _load_frames(self) -> list[pygame.Surface]:
        """Extract and load all animation frames from the sprite sheet."""
        return [self._extract_frame(index) for index in range(BIRD_SPRITE_SHEET_TOTAL_FRAMES)]

    def _extract_frame(self, index: int) -> pygame.Surface:
        """Extract an individual frame from the sprite sheet."""
        x = (
            index * (BIRD_SPRITE_SHEET_FRAME_HEIGHT + BIRD_SPRITE_SHEET_PADDING_X)
            + BIRD_SPRITE_SHEET_PADDING_X
        )
        frame_rect = pygame.Rect(
            x,
            BIRD_SPRITE_SHEET_START_Y,
            BIRD_SPRITE_SHEET_FRAME_HEIGHT,
            BIRD_SPRITE_SHEET_FRAME_HEIGHT,
        )
        return self.sprite_sheet.subsurface(frame_rect).copy()
