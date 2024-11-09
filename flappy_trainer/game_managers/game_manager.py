import pygame
from dotenv import load_dotenv
from game_managers.base_game_manager import BaseGameManager

load_dotenv()


class GameManager(BaseGameManager):
    def __init__(self):
        super().__init__()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass

    def update(self):
        pass

    def draw(self):
        pygame.display.set_caption("Flappy Trainer")
        self.screen.fill((135, 206, 250))  # Sky blue

        # Draw game objects

        # Update the display
        pygame.display.flip()
