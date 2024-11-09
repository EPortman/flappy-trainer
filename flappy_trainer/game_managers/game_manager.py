import pygame
from game_managers.base_game_manager import BaseGameManager
from game_objects.bird import Bird


class GameManager(BaseGameManager):
    def __init__(self):
        super().__init__()
        self.bird = Bird()
        self.is_game_paused = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.bird.flap()

    def update(self):
        if self.bird.is_alive and not self.is_game_paused:
            self.bird.update()
            self.check_bird_collision()

    def check_bird_collision(self):
        top_collision = self.bird.y - self.bird.radius <= 0
        bottom_collision = self.bird.y + self.bird.radius >= self.SCREEN_HEIGHT

        if top_collision or bottom_collision:
            self.bird.die()
            self.is_game_over = True

    def draw(self):
        super().draw()

        # Draw game objects
        self.bird.draw(self.screen)

        # Update the display
        pygame.display.flip()
