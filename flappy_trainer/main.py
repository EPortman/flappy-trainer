import sys

import pygame
from game_managers.game_manager import GameManager

pygame.init()

try:
    game_manager = GameManager()
except EnvironmentError as e:
    print(f"Error in .env: {e}")
    pygame.quit()
    sys.exit(1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        game_manager.handle_event(event)

    game_manager.update()
    game_manager.draw()

    # Cap the frame rate
    game_manager.clock.tick(60)
