from random import randint

import pygame
from game_managers.base_game_manager import BaseGameManager
from game_objects.bird.bird import Bird
from game_objects.pipe import Pipe
from utils import GameState


class GameManager(BaseGameManager):
    def __init__(self):
        """Initialize the game manager with the initial state and menus."""
        super().__init__()
        self.state = GameState.START_MENU
        self.bird = None
        self.pipes = []
        self.time_between_pipes = randint(self.min_time_between_pipes, self.max_time_between_pipes)

    def start_game(self):
        """Initialize game objects and start the game."""
        self.bird = Bird()
        self.pipes = []
        self.state = GameState.RUNNING
        self.level = self.start_level
        self.score = self.start_score
        self.next_level_score = self.score + self.score_per_level_up

    def handle_event(self, event: pygame.event.Event):
        """Handle user input events based on the current game state."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.state == GameState.START_MENU:
                    self.start_game()
                elif self.state == GameState.GAME_OVER:
                    self.start_game()
                elif self.state == GameState.PAUSED:
                    self.state = GameState.RUNNING
                elif self.state == GameState.RUNNING:
                    self.bird.flap()
            elif event.key == pygame.K_p and self.state == GameState.RUNNING:
                self.state = GameState.PAUSED

    def update(self, delta_time: float):
        """Update game objects and check collisions if game is live."""
        if (
            self.state == GameState.START_MENU
            or self.state == GameState.GAME_OVER
            or self.state == GameState.PAUSED
        ):
            return
        self.bird.update(delta_time)
        self.check_bird_collision()
        self.update_pipes(delta_time)
        if self.score >= self.next_level_score:
            self.level += 1
            self.pipe_speed += self.pipe_speed_increase_per_level_up
            self.next_level_score += self.score_per_level_up

    def update_pipes(self, delta_time: float):
        """Move pipes and spawn new ones based on time elapsed."""
        for pipe in self.pipes:
            pipe.update_position(self.pipe_speed * delta_time)
            if not pipe.passed and (pipe.x_pos + pipe.width) < self.bird.x_pos:
                self.score += 1
                pipe.passed = True
        self.pipes = [pipe for pipe in self.pipes if not pipe.is_off_screen()]

        self.time_since_last_pipe += delta_time * 1000
        if self.time_since_last_pipe >= self.time_between_pipes:
            self.pipes.append(Pipe(self.SCREEN_WIDTH))
            self.time_since_last_pipe = 0
            self.time_between_pipes = randint(
                self.min_time_between_pipes, self.max_time_between_pipes
            )

    def check_bird_collision(self):
        """Check for collisions between the bird and obstacles."""
        top_collision = self.bird.y_pos - self.bird.radius <= 0
        bottom_collision = self.bird.y_pos + self.bird.radius >= self.SCREEN_HEIGHT

        if top_collision or bottom_collision:
            self.bird.die()
            self.state = GameState.GAME_OVER
            return

        bird_rect = self.bird.get_rect()
        for pipe in self.pipes:
            if pipe.collides_with(bird_rect):
                self.bird.die()
                self.state = GameState.GAME_OVER
                break

    def draw_hud(self):
        """Draw the HUD with score and level."""
        # Render score and level text
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        level_text = self.font.render(f"Level: {self.level}", True, (255, 255, 255))

        # Set the positions of the text
        score_rect = score_text.get_rect(topleft=(10, 10))
        level_rect = level_text.get_rect(topleft=(10, 50))

        # Draw text on the screen
        self.screen.blit(score_text, score_rect)
        self.screen.blit(level_text, level_rect)

    def draw(self):
        """Draw all game objects onto the screen."""
        super().draw()
        if self.state == GameState.START_MENU or self.state == GameState.GAME_OVER:
            self.start_menu.draw(self.screen)
        elif self.state == GameState.PAUSED:
            self.pause_menu.draw(self.screen)
        else:
            self.bird.draw(self.screen)
            for pipe in self.pipes:
                pipe.draw(self.screen)
            self.draw_hud()

        pygame.display.flip()
