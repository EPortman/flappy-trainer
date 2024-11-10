import pygame
from utils import get_env_var_as_tuple


class StartMenu:
    def __init__(self):
        """Initialize the start menu."""
        self.background_color = get_env_var_as_tuple("MENU_BACKGROUND_COLOR")
        self.text_color = get_env_var_as_tuple("MENU_TEXT_COLOR")
        self.font = pygame.font.Font(None, 40)

    def draw(self, screen: pygame.Surface):
        """Draw the start menu onto the screen."""
        screen.fill(self.background_color)
        text = self.font.render("Press SPACE to Start", True, self.text_color)
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)
