from enum import Enum

from flappy_trainer.game_managers.game_manager import GameManager
from flappy_trainer.utils import get_env_var_as_int


class Action(Enum):
    FLAP = 1
    NO_FLAP = 0


def get_distance_to_next_pipe(game_manager: GameManager) -> int | None:
    unpassed_pipes = [pipe for pipe in game_manager.pipes if pipe.passed is False]
    if not unpassed_pipes:
        return None
    closest_pipe = min(unpassed_pipes, key=lambda pipe: pipe.x_pos)
    distance_to_pipe = closest_pipe.x_pos - game_manager.bird.x_pos
    return distance_to_pipe


def get_nearest_pipe_heights(game_manager: GameManager) -> tuple[int, int] | None:
    unpassed_pipes = [pipe for pipe in game_manager.pipes if pipe.passed is False]
    if not unpassed_pipes:
        return None
    closest_pipe = min(unpassed_pipes, key=lambda pipe: pipe.x_pos)
    return (closest_pipe.top_height, closest_pipe.bottom_height)


def get_curr_pipe_velocity(game_manager: GameManager) -> int:
    pipe_base_speed = get_env_var_as_int("PIPE_SPEED")
    pipe_speed_increase_per_level_up = get_env_var_as_int("PIPE_SPEED_INCREASE_PER_LEVEL_UP")
    delta_time = 1 / 60

    curr_pipe_velocity = (
        pipe_base_speed + (game_manager.level * pipe_speed_increase_per_level_up) * delta_time
    )
    return curr_pipe_velocity
