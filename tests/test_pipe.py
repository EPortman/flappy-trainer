import pygame
import pytest

from flappy_trainer.config import (
    INITIAL_PIPE_SPEED,
    PIPE_MAX_GAP_HEIGHT,
    PIPE_MIN_GAP_HEIGHT,
    PIPE_MIN_HEIGHT,
    PIPE_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from flappy_trainer.game_managers.game_manager import GameManager
from flappy_trainer.game_objects.pipe.pipe import Pipe
from flappy_trainer.utils import PipeColor


class TestPipe:
    def setup_method(self):
        """Set up the test environment before each test."""
        pygame.init()
        self.game_manager = GameManager()
        self.game_manager.start_game()

    def teardown_method(self):
        """Clean up the test environment after each test."""
        pygame.quit()

    def test_pipe_initi_with_defaults(self):
        """Test Pipe initialization with default parameters."""
        self.game_manager._spawn_pipe(PipeColor.GREEN)
        pipe: Pipe = self.game_manager.pipes[0]
        assert pipe.color == PipeColor.GREEN
        assert pipe.x_pos == SCREEN_WIDTH
        assert PIPE_MIN_GAP_HEIGHT <= pipe.gap_height <= PIPE_MAX_GAP_HEIGHT
        assert PIPE_MIN_HEIGHT + (pipe.gap_height // 2) <= pipe.gap_center
        assert pipe.gap_center <= SCREEN_HEIGHT - PIPE_MIN_HEIGHT - (pipe.gap_height // 2)

    def test_pipe_init_with_custom(self):
        """Test Pipe initialization with custom parameters."""
        self.game_manager._spawn_pipe(
            pipe_color=PipeColor.GREEN, x_pos=400, gap_center=300, gap_height=150
        )
        pipe: Pipe = self.game_manager.pipes[0]
        assert pipe.color == PipeColor.GREEN
        assert pipe.x_pos == 400
        assert pipe.gap_center == 300
        assert pipe.gap_height == 150

    def test_pipe_init_with_incorrect(self):
        """Test pipe initialization with incorrect parameters."""
        Pipe(PipeColor.GREEN, 100, 300, 150)

        # Invalid gap height
        with pytest.raises(AssertionError, match="Gap height must be"):
            Pipe(PipeColor.RED, 100, 300, PIPE_MAX_GAP_HEIGHT + 1)

        # Invalid gap center
        with pytest.raises(AssertionError, match="Gap center must be"):
            Pipe(PipeColor.GREEN, 100, PIPE_MIN_HEIGHT, 150)

        # Invalid pipe color
        with pytest.raises(AssertionError, match="Invalid pipe color."):
            Pipe("BLUE", 100, 300, 150)

        # Invalid x position
        with pytest.raises(AssertionError, match="Invalid x pos."):
            Pipe(PipeColor.GREEN, -1, 300, 150)
        with pytest.raises(AssertionError, match="Invalid x pos."):
            Pipe(PipeColor.GREEN, SCREEN_WIDTH + 1, 300, 150)

    def test_update_position(self):
        """Tests if the pipe correctly moves as the game manager updates the game."""
        self.game_manager._spawn_pipe(
            pipe_color=PipeColor.GREEN, x_pos=400, gap_center=300, gap_height=150
        )
        pipe: Pipe = self.game_manager.pipes[0]
        initial_x = pipe.x_pos
        self.game_manager.update(1 / 60)
        assert pipe.x_pos == initial_x - (INITIAL_PIPE_SPEED * 1 / 60)

    def test_is_off_screen(self):
        """Test the `is_off_screen` method."""
        self.game_manager._spawn_pipe(pipe_color=PipeColor.GREEN, x_pos=10)
        pipe: Pipe = self.game_manager.pipes[0]
        for _ in range(5):
            self.game_manager.update(1 / 60)
        assert not pipe.is_off_screen()
        for _ in range(20):
            self.game_manager.update(1 / 60)
        assert pipe.is_off_screen()

    def test_collides_with(self):
        """Test the `collides_with` method."""
        self.game_manager._spawn_pipe(
            pipe_color=PipeColor.GREEN, x_pos=100, gap_center=200, gap_height=150
        )
        pipe: Pipe = self.game_manager.pipes[0]
        bird_rect = pygame.Rect(110, 190, 20, 20)  # Overlaps the gap
        assert not pipe.collides_with(bird_rect)  # Should not collide

        bird_rect = pygame.Rect(110, 0, 20, 20)  # Collides with the top pipe
        assert pipe.collides_with(bird_rect)

        bird_rect = pygame.Rect(110, 400, 20, 20)  # Collides with the bottom pipe
        assert pipe.collides_with(bird_rect)

    def test_gap_height_and_center_correctness(self):
        """Ensure the gap height, center calculations, and rectangles are correct."""
        self.game_manager._spawn_pipe(
            pipe_color=PipeColor.GREEN, x_pos=400, gap_center=300, gap_height=150
        )
        pipe: Pipe = self.game_manager.pipes[0]
        gap_top = pipe.gap_center - (pipe.gap_height // 2)
        gap_bottom = pipe.gap_center + (pipe.gap_height // 2)

        # Verify the pipe heights
        assert pipe.top_pipe_height == gap_top
        assert pipe.bot_pipe_height == SCREEN_HEIGHT - gap_bottom

        # Verify the top pipe rectangle
        assert pipe.top_pipe_rect.x == pipe.x_pos
        assert pipe.top_pipe_rect.y == 0
        assert pipe.top_pipe_rect.width == PIPE_WIDTH
        assert pipe.top_pipe_rect.height == pipe.top_pipe_height

        # Verify the bottom pipe rectangle
        assert pipe.bot_pipe_rect.x == pipe.x_pos
        assert pipe.bot_pipe_rect.y == gap_bottom
        assert pipe.bot_pipe_rect.width == PIPE_WIDTH
        assert pipe.bot_pipe_rect.height == pipe.bot_pipe_height
