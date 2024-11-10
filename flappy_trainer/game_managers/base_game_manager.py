import pygame
from game_menus.pause_menu import PauseMenu
from game_menus.start_menu import StartMenu
from utils import get_env_var_as_int, get_env_var_as_tuple


class BaseGameManager:
    def __init__(self):
        """Initialize the base game manager."""
        self.SCREEN_WIDTH = get_env_var_as_int("SCREEN_WIDTH")
        self.SCREEN_HEIGHT = get_env_var_as_int("SCREEN_HEIGHT")
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.screen.fill(get_env_var_as_tuple("BACKGROUND_COLOR"))
        self.border_thickness = get_env_var_as_int("BORDER_THICKNESS")
        self.border_color = get_env_var_as_tuple("BORDER_COLOR")
        self.pipe_speed = get_env_var_as_int("PIPE_SPEED")
        self.time_between_pipes = get_env_var_as_int("START_TIME_BETWEEN_PIPES")
        self.pipe_timer = 0
        self.time_since_last_pipe = 0
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Flappy Trainer")
        self.start_menu = StartMenu()
        self.pause_menu = PauseMenu()

    def draw(self):
        """Draw the basic game canvas."""
        self.screen.fill(get_env_var_as_tuple("BACKGROUND_COLOR"))
        pygame.draw.rect(
            self.screen,
            self.border_color,
            pygame.Rect(0, 0, self.SCREEN_WIDTH, self.border_thickness),
        )
        pygame.draw.rect(
            self.screen,
            self.border_color,
            pygame.Rect(
                0,
                self.SCREEN_HEIGHT - self.border_thickness,
                self.SCREEN_WIDTH,
                self.border_thickness,
            ),
        )
