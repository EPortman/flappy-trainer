import pygame

from flappy_trainer.config import DEBUG, PIPE_WIDTH, SCREEN_HEIGHT
from flappy_trainer.game_objects.pipe.pipe_spritesheet import PipeSpriteSheet
from flappy_trainer.utils import PipeColor


class PipeBase:
    def __init__(self, pipe_color: PipeColor, x_pos: int, gap_center: int, gap_height: int):
        self.spritesheet = PipeSpriteSheet()
        self.screen_height = SCREEN_HEIGHT
        self.color = pipe_color
        self.width = PIPE_WIDTH
        self.x_pos = x_pos
        self.gap_height = gap_height
        self.gap_center = gap_center
        self.top_pipe_height, self.bot_pipe_height = self._generate_pipe_heights()
        self.update_rects()

    def update_rects(self) -> None:
        """Update the collision rectangles based on x-position."""
        self.top_pipe_rect = pygame.Rect(self.x_pos, 0, self.width, self.top_pipe_height)
        self.bot_pipe_rect = pygame.Rect(
            self.x_pos, self.gap_center + (self.gap_height // 2), self.width, self.bot_pipe_height
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
                source_rect = (0, pipe_frame.get_height() - part_height, self.width, part_height)
                pipe_segment = pipe_frame.subsurface(source_rect)
                screen.blit(pipe_segment, (self.x_pos, current_y - part_height))
                current_y -= part_height
                if DEBUG:
                    pygame.draw.rect(screen, (255, 0, 0), self.top_pipe_rect, 2)
        else:
            # Draw the bottom pipe starting at its top and moving downwards
            current_y = self.screen_height - self.bot_pipe_height
            while current_y < self.screen_height:
                part_height = min(segment_height, self.screen_height - current_y)
                source_rect = (0, 0, self.width, part_height)
                pipe_segment = pipe_frame.subsurface(source_rect)
                screen.blit(pipe_segment, (self.x_pos, current_y))
                current_y += part_height
                if DEBUG:
                    pygame.draw.rect(screen, (255, 0, 0), self.bot_pipe_rect, 2)

        # Visualize the gap center and gap height
        if DEBUG:
            self._draw_gap(screen)

    def _draw_gap(self, screen: pygame.Surface):
        """Visualizes the gap in the pipes, used for debugging."""
        gap_center_x = self.x_pos + (self.width // 2)
        gap_top_y = self.gap_center - (self.gap_height // 2)
        gap_bottom_y = self.gap_center + (self.gap_height // 2)
        pygame.draw.circle(screen, (0, 255, 0), (gap_center_x, self.gap_center), 5)
        pygame.draw.line(
            screen, (0, 255, 0), (gap_center_x, gap_top_y), (gap_center_x, gap_bottom_y), 2
        )

    def _generate_pipe_heights(self) -> tuple[int, int]:
        """Generate heights for the top and bottom pipes."""
        half_gap = self.gap_height // 2
        top_pipe_height = self.gap_center - half_gap
        bot_pipe_height = self.screen_height - (self.gap_center + half_gap)
        return top_pipe_height, bot_pipe_height
