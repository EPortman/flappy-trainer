import pygame

from flappy_trainer.ai.ai_utils import get_distance_to_next_pipe
from flappy_trainer.config import SCREEN_WIDTH
from flappy_trainer.game_managers.game_manager import GameManager
from flappy_trainer.game_objects.pipe.pipe import Pipe
from flappy_trainer.utils import PipeColor


class TestGetDistanceToNextPipe:
    def setup_method(self):
        """Set up the test environment before each test."""
        pygame.init()
        self.game_manager = GameManager()
        self.game_manager.start_game()

    def teardown_method(self):
        """Clean up the test environment after each test."""
        pygame.quit()

    def test_no_pipes(self):
        """Test function returns SCREEN_WIDTH when no pipes are present."""
        calc_distance_to_next_pipe = get_distance_to_next_pipe(self.game_manager)
        assert calc_distance_to_next_pipe == SCREEN_WIDTH

    def test_one_pipe(self):
        """Test function calculates the distance to a single pipe correctly."""
        self.game_manager.pipes.append(Pipe(PipeColor.GREEN, x_pos=400))
        calc_distance_to_next_pipe = get_distance_to_next_pipe(self.game_manager)
        actual_distance_to_next_pipe = 400 - self.game_manager.bird.x_pos
        assert calc_distance_to_next_pipe == actual_distance_to_next_pipe

    def test_multiple_pipes(self):
        """Test function calculates the distance to the nearest pipe when multiple pipes exist."""
        self.game_manager.pipes.append(Pipe(PipeColor.GREEN, x_pos=400))
        self.game_manager.pipes.append(Pipe(PipeColor.GREEN, x_pos=600))
        calc_distance_to_next_pipe = get_distance_to_next_pipe(self.game_manager)
        actual_distance_to_next_pipe = 400 - self.game_manager.bird.x_pos
        assert calc_distance_to_next_pipe == actual_distance_to_next_pipe

    def test_pipes_passed(self):
        """Test function ignores pipes that are already passed."""
        self.game_manager.pipes.append(Pipe(PipeColor.GREEN, x_pos=10))
        self.game_manager.pipes[0].passed = True
        calc_distance_to_next_pipe = get_distance_to_next_pipe(self.game_manager)
        assert calc_distance_to_next_pipe == SCREEN_WIDTH
