import sys

import pygame

from flappy_trainer.game_managers.game_manager import GameManager

try:
    pygame.init()
    game_manager = GameManager(
        is_pipes=True,
        pipe_gap_size_mode="large",
        pipe_distance_mode="large",
        is_pipe_gaps_centered=False,
        is_pipe_gaps_alternating=True,
    )
    clock = pygame.time.Clock()
except EnvironmentError as e:
    print(f"Error in .env: {e}")
    pygame.quit()
    sys.exit(1)

while True:
    delta_time = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        game_manager.handle_event(event)

    game_manager.update(delta_time)
    game_manager.draw()

    # Cap the frame rate
    game_manager.clock.tick(60)
