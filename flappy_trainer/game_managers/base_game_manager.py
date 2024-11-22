"""
BaseGameManager Abstract Class

This class provides a foundational structure for managing the core game logic and lifecycle
in the Flappy Bird game. It defines shared functionality for rendering the game screen,
handling menus, and setting up game parameters. Concrete game managers should extend
this class to implement specific game mechanics and behaviors.

Key Features:
- Initializes and manages the game screen and basic configurations.
- Supports start and pause menus.
- Provides methods for rendering the game canvas and managing pipe timing.
- Abstract methods enforce implementation of game-specific logic in subclasses.
"""

from abc import ABC, abstractmethod

import pygame

from flappy_trainer.config import (
    BACKGROUND_COLOR,
    BORDER_COLOR,
    BORDER_THICKNESS,
    INITIAL_PIPE_SPEED,
    PIPE_SPEED_INCREASE_PER_LEVEL_UP,
    SCORE_PER_LEVEL_UP,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from flappy_trainer.game_menus.pause_menu import PauseMenu
from flappy_trainer.game_menus.start_menu import StartMenu


class BaseGameManager(ABC):
    def __init__(self):
        # Screen Setup
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.fill(BACKGROUND_COLOR)
        self.font = pygame.font.Font(None, 36)
        pygame.display.set_caption("Flappy Trainer")

        # Game Parameters
        self.pipe_speed = INITIAL_PIPE_SPEED
        self.score_per_level_up = SCORE_PER_LEVEL_UP
        self.pipe_speed_increase_per_level_up = PIPE_SPEED_INCREASE_PER_LEVEL_UP

        # Timers and Game Clock
        self.pipe_timer = 0
        self.time_since_last_pipe = 0
        self.clock = pygame.time.Clock()

        # Menus
        self.start_menu = StartMenu()
        self.pause_menu = PauseMenu()

    def draw_canvas(self):
        """Render the game canvas and draw the screen borders."""
        # Fill the background
        self.screen.fill(BACKGROUND_COLOR)

        # Draw top and bottom borders
        pygame.draw.rect(
            self.screen,
            BORDER_COLOR,
            pygame.Rect(0, 0, SCREEN_WIDTH, BORDER_THICKNESS),
        )
        pygame.draw.rect(
            self.screen,
            BORDER_COLOR,
            pygame.Rect(
                0,
                SCREEN_HEIGHT - BORDER_THICKNESS,
                SCREEN_WIDTH,
                BORDER_THICKNESS,
            ),
        )

    @abstractmethod
    def start_game(self):
        """Start the game. This must be implemented in subclasses."""
        pass

    @abstractmethod
    def handle_event(self):
        """Handle user input events. This must be implemented in subclasses."""
        pass

    @abstractmethod
    def update(self):
        """Update game logic, such as positions and states. This must be implemented in subclasses."""
        pass
