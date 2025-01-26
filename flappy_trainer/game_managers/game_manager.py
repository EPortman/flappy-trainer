"""
GameManager

This class manages the main gameplay loop, handling states, objects, and user interactions.
It extends the `BaseGameManager` to implement specific game logic for Flappy Bird.

Key Features:
- Manages game states (Start Menu, Running, Paused, Game Over).
- Handles user input and game object updates (bird, pipes, score, and level).
- Implements collision detection and spawning of pipes.
- Draws game elements, including HUD and menus.
"""

from random import randint

import pygame

from flappy_trainer.config import (
    INITIAL_PIPE_SPEED,
    MAX_PIPE_VELOCITY,
    MAX_TIME_BETWEEN_PIPES,
    MIN_TIME_BETWEEN_PIPES,
    PIPE_MAX_GAP_HEIGHT,
    PIPE_MIN_GAP_HEIGHT,
    PIPE_WIDTH,
    SCREEN_HEIGHT,
    START_LEVEL,
    START_SCORE,
)
from flappy_trainer.game_managers.base_game_manager import BaseGameManager
from flappy_trainer.game_objects.bird.bird import Bird
from flappy_trainer.game_objects.pipe.pipe import Pipe
from flappy_trainer.utils import GameState, PipeColor


class GameManager(BaseGameManager):
    def __init__(
        self,
        is_pipes: bool = True,
        pipe_gap_size_mode: str = "random",  # Options: 'large', 'small', 'random'
        pipe_distance_mode: str = "random",  # Options: 'large', 'random'
        is_pipe_gaps_centered: bool = False,
        is_pipe_gaps_alternating: bool = False,
    ):
        """Initialize the game manager with the initial state and menus."""
        super().__init__()
        self.state = GameState.START_MENU
        self.bird = None
        self.pipes = []
        self.is_pipes_active = is_pipes
        self.pipe_gap_size_mode = pipe_gap_size_mode
        self.pipe_distance_mode = pipe_distance_mode
        self.is_pipe_gaps_centered = is_pipe_gaps_centered
        self.is_pipe_gaps_alternating = is_pipe_gaps_alternating

    def start_game(self):
        """Reset and initialize game objects to start the game."""
        super().reset()
        self.bird = Bird()
        self.pipes = []
        self.state = GameState.RUNNING
        self.level = START_LEVEL
        self.score = START_SCORE
        self.pipe_speed = INITIAL_PIPE_SPEED
        self.next_level_score = self.score + self.score_per_level_up
        self.time_since_last_pipe = 0

        if self.pipe_distance_mode == "large":
            self.time_between_pipes = MAX_TIME_BETWEEN_PIPES
        elif self.pipe_distance_mode == "random":
            self.time_between_pipes = randint(MIN_TIME_BETWEEN_PIPES, MAX_TIME_BETWEEN_PIPES)
        else:
            self.time_between_pipes = MIN_TIME_BETWEEN_PIPES

    def handle_event(self, event: pygame.event.Event):
        """Handle user input events based on the current game state."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.state in {GameState.START_MENU, GameState.GAME_OVER}:
                    self.start_game()
                elif self.state == GameState.PAUSED:
                    self.state = GameState.RUNNING
                elif self.state == GameState.RUNNING:
                    self.bird.flap()
            elif event.key == pygame.K_p and self.state == GameState.RUNNING:
                self.state = GameState.PAUSED

    def update(self, delta_time: float):
        """Update game objects and check collisions if the game is active."""
        if self.state not in {GameState.RUNNING}:
            return

        self.bird.update(delta_time)
        self._check_bird_collision()
        if self.is_pipes_active:
            self._update_pipes(delta_time)

        if self.score >= self.next_level_score:
            self._level_up()

    def draw(self):
        """Draw all game elements on the screen."""
        super().draw_canvas()
        if self.state in {GameState.START_MENU, GameState.GAME_OVER}:
            self.start_menu.draw(self.screen)
        elif self.state == GameState.PAUSED:
            self.pause_menu.draw(self.screen)
        else:
            self.bird.draw(self.screen)
            for pipe in self.pipes:
                pipe.draw(self.screen)
            self._draw_hud()

        pygame.display.flip()

    def _update_pipes(self, delta_time: float):
        """Move pipes and spawn new ones based on time elapsed."""
        for pipe in self.pipes:
            pipe.update_position(self.pipe_speed * delta_time)
            if not pipe.passed and (pipe.x_pos + PIPE_WIDTH) < self.bird.x_pos:
                self.score += 1
                pipe.passed = True

        # Remove pipes that are off-screen
        self.pipes = [pipe for pipe in self.pipes if not pipe.is_off_screen()]

        # Spawn new pipes based on elapsed time
        self.time_since_last_pipe += delta_time * 1000
        if self.time_since_last_pipe >= self.time_between_pipes:
            self._spawn_pipe()
            self.time_since_last_pipe = 0

    def _check_bird_collision(self):
        """Check for collisions between the bird and obstacles."""
        # Check for collisions with screen boundaries
        if self.bird.y_pos - self.bird.radius <= 0 or self.bird.y_pos + self.bird.radius >= SCREEN_HEIGHT:
            self._game_over()
            return

        # Check for collisions with pipes
        bird_rect = self.bird.get_rect()
        for pipe in self.pipes:
            if pipe.collides_with(bird_rect):
                self._game_over()
                break

    def _game_over(self):
        """Handle game-over logic."""
        self.bird.die()
        self.state = GameState.GAME_OVER

    def _level_up(self):
        """Increase level and adjust game difficulty."""
        self.level += 1
        self.pipe_speed = min(self.pipe_speed + self.pipe_speed_increase_per_level_up, MAX_PIPE_VELOCITY)
        self.next_level_score += self.score_per_level_up

    def _draw_hud(self):
        """Draw the HUD with score and level information."""
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        level_text = self.font.render(f"Level: {self.level}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 50))

    def _spawn_pipe(self):
        """Spawn a new pipe and add it to the list of pipes."""
        # Determine gap height based on pipe_gap_size_mode
        if self.pipe_gap_size_mode == "large":
            gap_height = PIPE_MAX_GAP_HEIGHT
        elif self.pipe_gap_size_mode == "small":
            gap_height = PIPE_MIN_GAP_HEIGHT
        else:
            gap_height = randint(PIPE_MIN_GAP_HEIGHT, PIPE_MAX_GAP_HEIGHT)

        # Determine gap center
        if self.is_pipe_gaps_alternating:
            if hasattr(self, "previous_gap_center"):
                gap_center = (
                    SCREEN_HEIGHT // 3
                    if self.previous_gap_center == 3 * SCREEN_HEIGHT // 4
                    else SCREEN_HEIGHT - SCREEN_HEIGHT // 3
                )
            else:
                gap_center = SCREEN_HEIGHT // 3
            self.previous_gap_center = gap_center
        elif self.is_pipe_gaps_centered:
            gap_center = SCREEN_HEIGHT // 2
        else:
            min_center = gap_height // 2 + 50
            max_center = SCREEN_HEIGHT - gap_height // 2 - 50
            gap_center = randint(min_center, max_center)

        # Determine time between pipes based on pipe_distance_mode
        if self.pipe_distance_mode == "large":
            self.time_between_pipes = MAX_TIME_BETWEEN_PIPES
        elif self.pipe_distance_mode == "random":
            self.time_between_pipes = randint(MIN_TIME_BETWEEN_PIPES, MAX_TIME_BETWEEN_PIPES)
        pipe = Pipe(PipeColor.GREEN, gap_center=gap_center, gap_height=gap_height)
        self.pipes.append(pipe)
