import pygame
from utils import BirdFrame, get_env_var_as_int, get_env_var_as_string


class BirdSpriteSheet:
    def __init__(self) -> None:
        """Load the sprite sheet from the given path."""
        self.sprite_sheet_path = get_env_var_as_string("BIRD_SPRITE_SHEET_PATH")
        self.total_frames = get_env_var_as_int("BIRD_SPRITE_SHEET_TOTAL_FRAMES")
        self.frame_width_px = get_env_var_as_int("BIRD_SPRITE_SHEET_FRAME_WIDTH")
        self.frame_height_px = get_env_var_as_int("BIRD_SPRITE_SHEET_FRAME_HEIGHT")
        self.frame_start_y = get_env_var_as_int("BIRD_SPRITE_SHEET_START_Y")
        self.frame_padding_px = get_env_var_as_int("BIRD_SPRITE_SHEET_PADDING_X")
        self.sprite_sheet = pygame.image.load(self.sprite_sheet_path).convert_alpha()
        self.frames = self._load_frames()

    def _load_frames(self) -> list[pygame.Surface]:
        """Load specific frames from a given row in the sprite sheet."""
        return [
            self._extract_frame(
                index,
                self.frame_start_y,
                self.frame_width_px,
                self.frame_height_px,
                self.frame_padding_px,
            )
            for index in range(self.total_frames)
        ]

    def _extract_frame(
        self, index: int, start_y: int, width: int, height: int, padding: int
    ) -> pygame.Surface:
        """Extract an individual frame from the sprite sheet."""
        x = index * (width + padding) + padding
        frame_rect = pygame.Rect(x, start_y, width, height)
        return self.sprite_sheet.subsurface(
            frame_rect
        ).copy()  # Use .copy() to prevent referencing issues

    def get_frame(self, frame: BirdFrame) -> pygame.Surface:
        """Return the specific frame based on the given BirdFrame enum."""
        if 0 <= frame.value < len(self.frames):
            return self.frames[frame.value]
        raise ValueError(
            f"Invalid frame index: {frame.value}. Available frames: 0 to {len(self.frames) - 1}."
        )

    def get_next_frame(
        self, current_frame: BirdFrame, start_frame: BirdFrame, end_frame: BirdFrame
    ) -> BirdFrame:
        """Cycle through frames in a given range based on BirdFrame enum."""
        next_value = current_frame.value + 1

        # If next_value exceeds end_frame, wrap around to start_frame
        if next_value > end_frame.value:
            return start_frame

        return BirdFrame(next_value)

    def get_idle_frame(self) -> BirdFrame:
        """Return the frame for idle state."""
        return BirdFrame.FLAPPING_TOP
