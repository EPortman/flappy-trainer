import pygame

from flappy_trainer.utils import (
    PipeColor,
    get_env_var_as_float,
    get_env_var_as_int,
    get_env_var_as_string,
)


class PipeSpriteSheet:
    def __init__(self) -> None:
        """Initialize the pipe sprite sheet, load frames, and apply scaling."""
        self._load_configuration()
        self._load_sprite_sheet()
        self._extract_and_scale_frames()

    def get_pipe_frame(self, color: PipeColor, is_top: bool) -> pygame.Surface:
        """
        Get a pipe frame of a given color, flipping it if required based on its position.

        Args:
            color (PipeColor): The color of the pipe (red or green).
            is_top (bool): Whether the pipe is positioned at the top or bottom.

        Returns:
            pygame.Surface: The appropriate pipe frame.
        """
        frame = self._get_frame_by_color(color)
        return self._flip_frame_if_needed(frame, color, is_top)

    def _load_configuration(self) -> None:
        """Load configuration values for pipe sprite sheet."""
        self.sprite_sheet_path = get_env_var_as_string("PIPE_SPRITE_SHEET_PATH")
        self.frame_width_px = get_env_var_as_int("PIPE_SPRITE_SHEET_FRAME_WIDTH")
        self.frame_height_px = get_env_var_as_int("PIPE_SPRITE_SHEET_FRAME_HEIGHT")
        self.scaling_factor = get_env_var_as_float("PIPE_SPRITE_SHEET_SCALE_FACTOR")

    def _load_sprite_sheet(self) -> None:
        """Load the sprite sheet from the specified path."""
        try:
            self.sprite_sheet = pygame.image.load(self.sprite_sheet_path).convert_alpha()
        except pygame.error as e:
            raise FileNotFoundError(
                f"Failed to load sprite sheet from '{self.sprite_sheet_path}': {e}"
            )

    def _extract_and_scale_frames(self) -> None:
        """Extract frames for red and green pipes from the sprite sheet, and scale them."""
        self.red_pipe_frame = self._extract_frame(0)
        self.green_pipe_frame = self._extract_frame(self.frame_width_px)

        self.red_pipe_frame = self._scale_frame(self.red_pipe_frame)
        self.green_pipe_frame = self._scale_frame(self.green_pipe_frame)

    def _extract_frame(self, x_offset: int) -> pygame.Surface:
        """Extract a pipe frame from the sprite sheet given an x-coordinate offset."""
        frame_rect = pygame.Rect(x_offset, 0, self.frame_width_px, self.frame_height_px)
        return self.sprite_sheet.subsurface(frame_rect).copy()

    def _scale_frame(self, frame: pygame.Surface) -> pygame.Surface:
        """Scale a frame by the scaling factor provided in the configuration."""
        new_dimensions = (
            int(self.frame_width_px * self.scaling_factor),
            int(self.frame_height_px * self.scaling_factor),
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
