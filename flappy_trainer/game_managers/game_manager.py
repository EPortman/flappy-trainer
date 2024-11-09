import pygame
from game_managers.base_game_manager import BaseGameManager
from game_objects.bird import Bird


class GameManager(BaseGameManager):
    def __init__(self):
        super().__init__()
        self.bird = Bird()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass

    def update(self):
        pass

    def draw(self):
        self.screen.fill((135, 206, 250))  # Sky blue

        # Draw game objects
        self.bird.draw(self.screen)

        # Update the display
        pygame.display.flip()
