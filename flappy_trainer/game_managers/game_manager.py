import pygame
from game_managers.base_game_manager import BaseGameManager
from game_objects.bird import Bird
from game_objects.pipe import Pipe


class GameManager(BaseGameManager):
    def __init__(self):
        """Initialize the game manager."""
        super().__init__()
        self.bird = Bird()
        self.pipes = []
        self.is_game_paused = False

    def handle_event(self, event: pygame.event.Event):
        """Handle user input events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.bird.flap()

    def update(self, delta_time: float):
        """Update game objects and check collisions."""
        if self.bird.is_alive and not self.is_game_paused:
            self.bird.update()
            self.check_bird_collision()
            self.update_pipes(delta_time)

    def update_pipes(self, delta_time: float):
        """Move pipes and spawn new ones based on time elapsed."""
        for pipe in self.pipes:
            pipe.update_position(self.pipe_speed * delta_time)
        self.pipes = [pipe for pipe in self.pipes if not pipe.is_off_screen()]

        self.time_since_last_pipe += delta_time * 1000
        if self.time_since_last_pipe >= self.time_between_pipes:
            self.pipes.append(Pipe(self.SCREEN_WIDTH))
            self.time_since_last_pipe = 0

    def check_bird_collision(self):
        """Check for collisions between the bird and obstacles."""
        top_collision = self.bird.y - self.bird.radius <= 0
        bottom_collision = self.bird.y + self.bird.radius >= self.SCREEN_HEIGHT

        if top_collision or bottom_collision:
            self.bird.die()
            self.is_game_over = True
            return

        bird_rect = self.bird.get_rect()
        for pipe in self.pipes:
            if pipe.collides_with(bird_rect):
                self.bird.die()
                self.is_game_over = True
                break

    def draw(self):
        """Draw all game objects onto the screen."""
        super().draw()

        self.bird.draw(self.screen)
        for pipe in self.pipes:
            pipe.draw(self.screen)

        pygame.display.flip()
