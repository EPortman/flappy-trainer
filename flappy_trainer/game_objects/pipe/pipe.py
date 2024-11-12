from random import randint

import pygame

from flappy_trainer.game_objects.pipe.pipe_spritesheet import PipeSpriteSheet
from flappy_trainer.utils import PipeColor, get_env_var_as_int


class Pipe:
    def __init__(self, pipe_color: PipeColor) -> None:
        self.pipe_color = pipe_color
        self.screen_height = get_env_var_as_int("SCREEN_HEIGHT")
        self.min_height = get_env_var_as_int("PIPE_MIN_HEIGHT")
        self.gap_height = randint(
            get_env_var_as_int("PIPE_MIN_GAP_HEIGHT"), get_env_var_as_int("PIPE_MAX_GAP_HEIGHT")
        )
        self.top_height, self.bottom_height = self._generate_pipe_heights()
        self.x_pos = get_env_var_as_int("SCREEN_WIDTH")
        self.width = get_env_var_as_int("PIPE_WIDTH")
        self.passed = False
        self.spritesheet = PipeSpriteSheet()
        self._update_rects()

    def collides_with(self, bird_rect: pygame.Rect) -> bool:
        """Determine if the pipe has collided with the given bird's rectangle."""
        return bird_rect.colliderect(self.top_rect) or bird_rect.colliderect(self.bottom_rect)

    def is_off_screen(self) -> bool:
        """Determine if the pipe has moved completely off the left side of the screen."""
        return self.x_pos + self.width < 0

    def update_position(self, speed: int) -> None:
        """Move the pipe horizontally left by the speed and update its collision boundaries."""
        self.x_pos -= speed
        self._update_rects()

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the top and bottom pipes onto the provided screen surface."""
        self._draw_pipe(screen, self.x_pos, self.top_height, is_top=True, height=self.top_height)
        self._draw_pipe(
            screen,
            self.x_pos,
            self.bottom_height,
            is_top=False,
            height=self.screen_height - self.bottom_height,
        )

    def _draw_pipe(
        self, screen: pygame.Surface, x_pos: int, y_pos: int, is_top: bool, height: int
    ) -> None:
        """
        Draw the pipe using the sprite frame, tiling segments vertically to fill the given height.

        Args:
            screen (pygame.Surface): The display surface to draw the pipe onto.
            x_pos (int): The horizontal position of the pipe.
            y_pos (int): The vertical starting position for drawing the pipe.
            is_top (bool): Whether the pipe is the top (True) or bottom (False) portion.
            height (int): The total height of the pipe to draw, to create the required visual gap.
        """
        pipe_frame = self.spritesheet.get_pipe_frame(self.pipe_color, is_top)
        segment_height = pipe_frame.get_height()

        if is_top:
            current_y = y_pos - segment_height
            while current_y + segment_height > y_pos - height:
                part_height = min(segment_height, y_pos - current_y)
                if part_height > 0:
                    pipe_segment = pipe_frame.subsurface(
                        (0, segment_height - part_height, pipe_frame.get_width(), part_height)
                    )
                    screen.blit(pipe_segment, (x_pos, current_y))
                current_y -= segment_height
        else:
            current_y = y_pos
            while current_y < y_pos + height:
                part_height = min(segment_height, y_pos + height - current_y)
                if part_height > 0:
                    pipe_segment = pipe_frame.subsurface(
                        (0, 0, pipe_frame.get_width(), part_height)
                    )
                    screen.blit(pipe_segment, (x_pos, current_y))
                current_y += segment_height

    def _generate_pipe_heights(self) -> tuple[int, int]:
        """Generate random heights for the top and bottom pipes."""
        max_top_height = self.screen_height - self.gap_height - self.min_height
        top_height = randint(self.min_height, max_top_height)
        bottom_height = top_height + self.gap_height
        return top_height, bottom_height

    def _update_rects(self) -> None:
        """Update the collision rectangles based on their current positions."""
        self.top_rect = pygame.Rect(self.x_pos, 0, self.width, self.top_height)
        self.bottom_rect = pygame.Rect(
            self.x_pos,
            self.bottom_height,
            self.width,
            pygame.display.get_surface().get_height() - self.bottom_height,
        )
