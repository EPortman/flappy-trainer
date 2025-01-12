import os
import sys
from enum import Enum, auto


class GameState(Enum):
    START_MENU = auto()
    RUNNING = auto()
    PAUSED = auto()
    GAME_OVER = auto()


class BirdState(Enum):
    NONE = auto()
    IDLE = auto()
    FLAPPING_UP = auto()
    TRANSITION = auto()
    DESCENDING = auto()
    NOSE_DIVE = auto()


class BirdFrame(Enum):
    FLAPPING_TOP = 0
    DESCENDING_START = 1
    DESCENDING_MID = 2
    DESCENDING_END = 3
    DESCENDING_FINAL = 4
    NOSE_DIVE = 5
    FLAPPING_START = 6
    FLAPPING_MID_1 = 7
    FLAPPING_MID_2 = 8
    FLAPPING_MID_3 = 9
    FLAPPING_END = 10


class PipeColor(Enum):
    GREEN = "GREEN"
    RED = "RED"


def get_env_var_as_int(var_name):
    """Retrieve an env variable as an integer. Throws Env Error if not available."""
    value = os.getenv(var_name)
    if value is None:
        raise EnvironmentError(f"Missing required environment variable: {var_name}")
    return int(value)


def get_env_var_as_float(var_name):
    """Retrieve an env variable as a float. Throws Env Error if not available."""
    value = os.getenv(var_name)
    if value is None:
        raise EnvironmentError(f"Missing required environment variable: {var_name}")
    return float(value)


def get_env_var_as_string(var_name: str) -> str:
    """Retrieve an environment variable as a string. Throws EnvironmentError if not available."""
    value = os.getenv(var_name)
    if value is None:
        raise EnvironmentError(f"Missing required environment variable: {var_name}")
    return value


def get_env_var_as_tuple(var_name):
    """Retrieve an env variable as a tuple of integers. Throws Env Error if not available."""
    value = os.getenv(var_name)
    if value is None:
        raise EnvironmentError(f"Missing required environment variable: {var_name}")
    return tuple(map(int, value.split(",")))
