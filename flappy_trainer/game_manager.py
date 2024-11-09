import os

import pygame
from dotenv import load_dotenv

load_dotenv()


class GameManager:
    def __init__(self):
        self.SCREEN_WIDTH = int(os.getenv("SCREEN_WIDTH", 800))
        self.SCREEN_HEIGHT = int(os.getenv("SCREEN_HEIGHT", 600))
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Flappy Trainer")

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
