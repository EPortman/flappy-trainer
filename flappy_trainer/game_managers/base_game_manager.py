import os

import pygame
from dotenv import load_dotenv

load_dotenv()


class BaseGameManager:
    def __init__(self):
        self.SCREEN_WIDTH = int(os.getenv("SCREEN_WIDTH", 800))
        self.SCREEN_HEIGHT = int(os.getenv("SCREEN_HEIGHT", 600))
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Flappy Trainer")
