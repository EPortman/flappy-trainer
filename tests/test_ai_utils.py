import pygame

from flappy_trainer.ai.ai_utils import get_curr_pipe_velocity, get_nearest_pipe_details
from flappy_trainer.config import (
    BIRD_START_X_POS,
    INITIAL_PIPE_SPEED,
    PIPE_SPEED_INCREASE_PER_LEVEL_UP,
    PIPE_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from flappy_trainer.game_managers.game_manager import GameManager
from flappy_trainer.utils import PipeColor


class TestAIUtils:
    """Test suite for AI utility functions used in Flappy Bird."""

    def setup_method(self):
        """Set up the test environment before each test."""
        pygame.init()
        self.game_manager = GameManager()
        self.game_manager.start_game()

    def teardown_method(self):
        """Clean up the test environment after each test."""
        pygame.quit()

    def test_get_curr_pipe_velocity(self):
        """Test the `get_curr_pipe_velocity` function."""
        self.game_manager.level = 0
        assert get_curr_pipe_velocity(self.game_manager) == INITIAL_PIPE_SPEED

        self.game_manager.level = 5
        expected_velocity = INITIAL_PIPE_SPEED + (5 * PIPE_SPEED_INCREASE_PER_LEVEL_UP)
        assert get_curr_pipe_velocity(self.game_manager) == expected_velocity

    def test_get_nearest_pipe_details_no_pipes(self):
        """Test `get_nearest_pipe_details` when no pipes exist."""
        details = get_nearest_pipe_details(self.game_manager)
        assert details == (SCREEN_WIDTH, SCREEN_HEIGHT // 2, SCREEN_HEIGHT // 4)

    def test_get_nearest_pipe_details_with_pipes(self):
        """Test `get_nearest_pipe_details` with pipes present."""
        self.game_manager._spawn_pipe(pipe_color=PipeColor.GREEN, x_pos=300, gap_center=250, gap_height=150)
        self.game_manager._spawn_pipe(pipe_color=PipeColor.GREEN, x_pos=500, gap_center=350, gap_height=200)
        details = get_nearest_pipe_details(self.game_manager)
        assert details == (300 + PIPE_WIDTH - BIRD_START_X_POS, 250, 150)

    def test_get_nearest_pipe_details_with_passed_pipes(self):
        """Test `get_nearest_pipe_details` with passed pipes."""
        self.game_manager._spawn_pipe(pipe_color=PipeColor.GREEN, x_pos=50, gap_center=400, gap_height=200)
        self.game_manager._spawn_pipe(pipe_color=PipeColor.GREEN, x_pos=250, gap_center=300, gap_height=130)
        self.game_manager.pipes[0].passed = True
        details = get_nearest_pipe_details(self.game_manager)
        assert details == (250 + PIPE_WIDTH - BIRD_START_X_POS, 300, 130)

    def test_get_nearest_pipe_details_all_passed(self):
        """Test `get_nearest_pipe_details` when all pipes are passed."""
        self.game_manager._spawn_pipe(pipe_color=PipeColor.GREEN, x_pos=50, gap_center=400, gap_height=200)
        self.game_manager._spawn_pipe(pipe_color=PipeColor.GREEN, x_pos=250, gap_center=300, gap_height=130)
        self.game_manager.pipes[0].passed = True
        self.game_manager.pipes[1].passed = True
        details = get_nearest_pipe_details(self.game_manager)
        assert details == (SCREEN_WIDTH, SCREEN_HEIGHT // 2, SCREEN_HEIGHT // 4)
