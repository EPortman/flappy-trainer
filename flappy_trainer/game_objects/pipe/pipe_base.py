"""
PipeBase Abstract Class

This class abstracts the basic functionality and logic for managing pipes in the
Flappy Bird game. It provides methods to handle drawing pipes and managing
their dimensions and collision areas using the PipeSpriteSheet class.

Key Features:
- Abstracts common pipe behavior like rendering and collision rectangle updates.
- Handles the logic for tiling (drawing) pipe segments vertically.
- Designed to be extended by specific pipe implementations.
"""

from abc import ABC, abstractmethod

import pygame

from flappy_trainer.config import DEBUG, PIPE_WIDTH, SCREEN_HEIGHT
from flappy_trainer.game_objects.pipe.pipe_spritesheet import PipeSpriteSheet
from flappy_trainer.utils import PipeColor


class PipeBase(ABC):
    def __init__(self, pipe_color: PipeColor, x_pos: int, gap_center: int, gap_height: int):
        self.spritesheet = PipeSpriteSheet()
        self.color = pipe_color
        self.x_pos = x_pos
        self.gap_height = gap_height
        self.gap_center = gap_center
        self.top_pipe_height, self.bot_pipe_height = self._generate_pipe_heights()
        self.update_rects()

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """Abstract method to enforce rendering logic in child classes."""
        pass

    def update_rects(self) -> None:
        """Update the collision rectangles based on x-position."""
        self.top_pipe_rect = pygame.Rect(self.x_pos, 0, PIPE_WIDTH, self.top_pipe_height)
        self.bot_pipe_rect = pygame.Rect(
            self.x_pos, self.gap_center + (self.gap_height // 2), PIPE_WIDTH, self.bot_pipe_height
        )

    def draw_pipe(self, screen: pygame.Surface, is_top: bool) -> None:
        """
        Draw a pipe (top or bottom) by tiling its segments vertically.

        Args:
            screen (pygame.Surface): The display surface to draw the pipe on.
            is_top (bool): Whether this is the top pipe (True) or bottom pipe (False).
        """
        # Get the pipe sprite and segment height
        pipe_frame = self.spritesheet.get_pipe_frame(self.color, is_top)
        segment_height = pipe_frame.get_height()

        if is_top:
            # Draw the top pipe starting at the bottom of the top pipe's height
            current_y = self.top_pipe_height
            while current_y > 0:
                part_height = min(segment_height, current_y)
                source_rect = (0, pipe_frame.get_height() - part_height, PIPE_WIDTH, part_height)
                pipe_segment = pipe_frame.subsurface(source_rect)
                screen.blit(pipe_segment, (self.x_pos, current_y - part_height))
                current_y -= part_height
                if DEBUG:
                    pygame.draw.rect(screen, (255, 0, 0), self.top_pipe_rect, 2)
        else:
            # Draw the bottom pipe starting at its top and moving downwards
            current_y = SCREEN_HEIGHT - self.bot_pipe_height
            while current_y < SCREEN_HEIGHT:
                part_height = min(segment_height, SCREEN_HEIGHT - current_y)
                source_rect = (0, 0, PIPE_WIDTH, part_height)
                pipe_segment = pipe_frame.subsurface(source_rect)
                screen.blit(pipe_segment, (self.x_pos, current_y))
                current_y += part_height
                if DEBUG:
                    pygame.draw.rect(screen, (255, 0, 0), self.bot_pipe_rect, 2)

        if DEBUG:
            self._draw_gap(screen)

    def _draw_gap(self, screen: pygame.Surface):
        """Visualizes the gap in the pipes, used for debugging."""
        gap_center_x = self.x_pos + (PIPE_WIDTH // 2)
        gap_top_y = self.gap_center - (self.gap_height // 2)
        gap_bottom_y = self.gap_center + (self.gap_height // 2)
        pygame.draw.circle(screen, (0, 255, 0), (gap_center_x, self.gap_center), 5)
        pygame.draw.line(screen, (0, 255, 0), (gap_center_x, gap_top_y), (gap_center_x, gap_bottom_y), 2)

    def _generate_pipe_heights(self) -> tuple[int, int]:
        """Generate px heights for the pipes using screen height and gap location."""
        half_gap = self.gap_height // 2
        top_pipe_height = self.gap_center - half_gap
        bot_pipe_height = SCREEN_HEIGHT - (self.gap_center + half_gap)
        return top_pipe_height, bot_pipe_height
