import pygame

from flappy_trainer.config import (
    INITIAL_PIPE_SPEED,
    PIPE_DEFAULT_GAP_HEIGHT,
    PIPE_DEFAULT_Y_POS,
    PIPE_WIDTH,
    SCREEN_HEIGHT,
    START_LEVEL,
    START_SCORE,
)
from flappy_trainer.game_managers.game_manager import GameManager
from flappy_trainer.game_objects.bird.bird import Bird
from flappy_trainer.game_objects.pipe.pipe import Pipe
from flappy_trainer.utils import GameState


class TestGameManager:
    def setup_method(self):
        """Set up the test environment."""
        pygame.init()
        self.game_manager = GameManager()
        self.game_manager.start_game()

    def teardown_method(self):
        """Clean up the test environment."""
        pygame.quit()

    def test_initialization(self):
        """Test that GameManager initializes with the correct default state."""
        assert self.game_manager.state == GameState.RUNNING
        assert isinstance(self.game_manager.bird, Bird)
        assert isinstance(self.game_manager.pipes, list)
        assert len(self.game_manager.pipes) == 0
        assert self.game_manager.pipe_speed == INITIAL_PIPE_SPEED
        assert self.game_manager.level == START_LEVEL
        assert self.game_manager.score == START_SCORE
        assert self.game_manager.is_pipes_active is True
        assert self.game_manager.is_pipe_spawns_consistent is False
        assert self.game_manager.is_pipe_gaps_centered is False
        assert self.game_manager.pipe_gap_height == PIPE_DEFAULT_GAP_HEIGHT
        assert self.game_manager.pipe_gap_y_pos == PIPE_DEFAULT_Y_POS

    def test_start_game(self):
        """Test that starting the game resets state correctly."""
        self.game_manager.start_game()
        assert self.game_manager.state == GameState.RUNNING
        assert self.game_manager.level == START_LEVEL
        assert self.game_manager.score == START_SCORE
        assert len(self.game_manager.pipes) == 0

    def test_handle_event_space_key(self):
        """Test handling the space key during different game states."""
        self.game_manager.state = GameState.START_MENU
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
        self.game_manager.handle_event(event)
        assert self.game_manager.state == GameState.RUNNING

        self.game_manager.state = GameState.GAME_OVER
        self.game_manager.handle_event(event)
        assert self.game_manager.state == GameState.RUNNING

    def test_handle_event_pause_key(self):
        """Test toggling between paused and running states."""
        self.game_manager.state = GameState.RUNNING
        pause_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_p})
        space_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
        self.game_manager.handle_event(pause_event)
        assert self.game_manager.state == GameState.PAUSED
        self.game_manager.handle_event(space_event)
        assert self.game_manager.state == GameState.RUNNING

    def test_update_running_state(self):
        """Test updating the game during the RUNNING state."""
        initial_score = self.game_manager.score
        self.game_manager._spawn_pipe()
        self.game_manager.pipes[0].x_pos = self.game_manager.bird.x_pos - PIPE_WIDTH
        self.game_manager.update(0.1)
        self.game_manager.update(0.1)
        assert self.game_manager.score == initial_score + 1

    def test_pipe_heights_consistent(self):
        """Test that pipe gap heights remain consistent when enabled."""
        self.game_manager.is_pipe_gap_heights_consistent = True
        self.game_manager.pipe_gap_height = 200
        self.game_manager._spawn_pipe()
        self.game_manager.update(0.1)
        self.game_manager._spawn_pipe()
        self.game_manager.update(0.1)
        self.game_manager.update(0.1)
        first_pipe: Pipe = self.game_manager.pipes[0]
        second_pipe: Pipe = self.game_manager.pipes[1]
        assert first_pipe.gap_height == second_pipe.gap_height == 200

    def test_pipe_gaps_centered(self):
        """Test that pipe gaps are centered when enabled."""
        self.game_manager.is_pipe_gaps_centered = True
        self.game_manager._spawn_pipe()
        pipe: Pipe = self.game_manager.pipes[0]
        assert pipe.gap_center == SCREEN_HEIGHT // 2

    def test_pipe_removal(self):
        """Test that pipes are removed once they move off-screen."""
        self.game_manager._spawn_pipe()
        pipe: Pipe = self.game_manager.pipes[0]
        pipe.x_pos = -PIPE_WIDTH
        self.game_manager.update(0.1)
        self.game_manager.update(0.1)
        assert pipe not in self.game_manager.pipes

    def test_disable_pipes(self):
        """Test that no pipes spawn when pipes_active is False."""
        self.game_manager.time_between_pipes = 0.2
        self.game_manager.is_pipes_active = False
        self.game_manager.update(0.1)
        self.game_manager.update(0.2)
        self.game_manager.draw()
        assert len(self.game_manager.pipes) == 0

    def test_gap_height_adjustment(self):
        """Test that pipes spawn with a custom gap height."""
        self.game_manager.is_pipe_gap_heights_consistent = True
        custom_gap_height = 200
        self.game_manager.pipe_gap_height = custom_gap_height
        self.game_manager._spawn_pipe()
        pipe: Pipe = self.game_manager.pipes[0]
        assert pipe.gap_height == custom_gap_height

    def test_game_over_on_boundary_collision(self):
        """Test that the game transitions to GAME_OVER when the bird hits boundaries."""
        self.game_manager.bird.y_pos = -10  # Simulate the bird going above the screen
        self.game_manager.update(0.1)
        assert self.game_manager.state == GameState.GAME_OVER

    def test_collision_with_pipe(self):
        """Test that the game ends when the bird collides with a pipe."""
        self.game_manager.is_pipe_gap_heights_consistent = True
        self.game_manager.pipe_gap_height = 120
        self.game_manager.pipe_gap_y_pos = 150
        self.game_manager._spawn_pipe()
        pipe: Pipe = self.game_manager.pipes[0]
        pipe.x_pos = self.game_manager.bird.x_pos + PIPE_WIDTH
        self.game_manager.draw()
        self.game_manager.update(0.2)
        self.game_manager.update(0.1)
        self.game_manager.draw()
        assert self.game_manager.state == GameState.GAME_OVER

    def test_level_up(self):
        """Test that the game levels up and increases difficulty."""
        self.game_manager.score = self.game_manager.next_level_score - 1
        self.game_manager._spawn_pipe()
        self.game_manager.pipes[0].x_pos = self.game_manager.bird.x_pos - PIPE_WIDTH
        self.game_manager.update(0.1)
        assert self.game_manager.level == START_LEVEL + 1
        assert self.game_manager.pipe_speed > INITIAL_PIPE_SPEED

    def test_random_pipe_spawns(self):
        """Test that pipes spawn randomly when no consistency flags are enabled."""
        self.game_manager.is_pipe_spawns_consistent = False
        self.game_manager.is_pipe_gaps_centered = False
        self.game_manager.is_pipe_gap_heights_consistent = False
        self.game_manager._spawn_pipe()
        self.game_manager._spawn_pipe()
        assert len(self.game_manager.pipes) == 2
        assert self.game_manager.pipes[0].gap_height != self.game_manager.pipes[1].gap_height

    def test_pipe_gap_heights_consistent(self):
        """Test that pipe gap heights remain consistent when enabled."""
        self.game_manager.is_pipe_gap_heights_consistent = True
        self.game_manager.pipe_gap_height = 150
        self.game_manager._spawn_pipe()
        self.game_manager._spawn_pipe()
        assert all(pipe.gap_height == 150 for pipe in self.game_manager.pipes)
