import pygame
from game_managers.base_game_manager import BaseGameManager
from game_objects.bird import Bird
from game_objects.pipe import Pipe


class GameManager(BaseGameManager):
    def __init__(self):
        super().__init__()
        self.bird = Bird()
        self.pipes = []
        self.is_game_paused = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.bird.flap()

    def update(self, delta_time):
        if self.bird.is_alive and not self.is_game_paused:
            self.bird.update()
            self.check_bird_collision()
            self.update_pipes(delta_time)

    def update_pipes(self, delta_time):
        # Move pipes and remove any that have gone off-screen
        for pipe in self.pipes:
            pipe.update_position(self.pipe_speed * delta_time)
        self.pipes = [pipe for pipe in self.pipes if not pipe.is_off_screen()]

        # Add new pipe
        self.time_since_last_pipe += delta_time * 1000
        if self.time_since_last_pipe >= self.time_between_pipes:
            self.pipes.append(Pipe(self.SCREEN_WIDTH))
            self.time_since_last_pipe = 0

    def check_bird_collision(self):
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
        super().draw()

        # Draw game objects
        self.bird.draw(self.screen)
        for pipe in self.pipes:
            pipe.draw(self.screen)

        # Update the display
        pygame.display.flip()
