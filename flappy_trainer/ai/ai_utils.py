from enum import Enum

from flappy_trainer.config import (
    INITIAL_PIPE_SPEED,
    PIPE_SPEED_INCREASE_PER_LEVEL_UP,
    PIPE_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from flappy_trainer.game_managers.game_manager import GameManager
from flappy_trainer.game_objects.pipe.pipe import Pipe
from flappy_trainer.utils import get_env_var_as_int


class Action(Enum):
    FLAP = 1
    NO_FLAP = 0


def update_game(game_manager: GameManager, frames: int, debug: bool = False):
    game_manager.update(1 / 60)
    if debug:
        game_manager.draw_canvas()

def print_debug_output(debug: bool, episode_num: int, total_episodes: int, exploration_rate: float, frames_survived):
    if debug:
        print(
            f"\nEpisode {episode_num + 1} / {total_episodes}, Percent Random moves: {(exploration_rate * 100):.1f}"
        )
    if frames_survived < 1200:
        print(f"   - Death! Frames Survived: {frames_survived}")
    else:
        print("   - Survived!")


def get_curr_pipe_velocity(game_manager: GameManager) -> int:
    return INITIAL_PIPE_SPEED + (game_manager.level * PIPE_SPEED_INCREASE_PER_LEVEL_UP)


def get_nearest_pipe_details(game_manager: GameManager) -> tuple[int, int, int]:
    unpassed_pipes = [pipe for pipe in game_manager.pipes if pipe.passed is False]
    if not unpassed_pipes:
        next_pipe_distance = SCREEN_WIDTH
        next_pipe_gap_pos = SCREEN_HEIGHT // 2
        next_pipe_gap_height = SCREEN_HEIGHT // 4
    else:
        pipe: Pipe = min(unpassed_pipes, key=lambda pipe: pipe.x_pos)
        next_pipe_distance = (pipe.x_pos + PIPE_WIDTH) - game_manager.bird.x_pos
        next_pipe_gap_pos = pipe.gap_center
        next_pipe_gap_height = pipe.gap_height
    return (next_pipe_distance, next_pipe_gap_pos, next_pipe_gap_height)


def get_alignment_reward(state):
    pipe_center = (state.next_pipe_top_height + state.next_pipe_bot_height) / 2
    distance_to_center = abs(state.bird_vert_pos - pipe_center)
    max_distance = get_env_var_as_int("SCREEN_HEIGHT")
    alignment_reward = 1 - (distance_to_center / max_distance)
    reward += alignment_reward * 10
