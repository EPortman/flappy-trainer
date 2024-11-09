import pygame
import sys
from game_manager import GameManager

pygame.init()
game_manager = GameManager()

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
