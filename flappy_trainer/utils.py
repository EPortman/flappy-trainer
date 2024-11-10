import os
from enum import Enum, auto


class GameState(Enum):
    START_MENU = auto()
    RUNNING = auto()
    PAUSED = auto()
    GAME_OVER = auto()


def get_env_var_as_int(var_name):
    """Retrieve an env variable as an integer. Throws Env Error if not available."""
    value = os.getenv(var_name)
    if value is None:
        raise EnvironmentError(f"Missing required environment variable: {var_name}")
    return int(value)


def get_env_var_as_tuple(var_name):
    """Retrieve an env variable as a tuple of integers. Throws Env Error if not available."""
    value = os.getenv(var_name)
    if value is None:
        raise EnvironmentError(f"Missing required environment variable: {var_name}")
    return tuple(map(int, value.split(",")))
