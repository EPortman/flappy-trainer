from dataclasses import dataclass
from enum import Enum

from flappy_trainer.ai.environment_state import EnvironmentState
from flappy_trainer.config import INITIAL_PIPE_SPEED, PIPE_SPEED_INCREASE_PER_LEVEL_UP, PIPE_WIDTH
from flappy_trainer.game_managers.game_manager import GameManager
from flappy_trainer.game_objects.pipe.pipe import Pipe


class Action(Enum):
    FLAP = 1
    NO_FLAP = 0


@dataclass
class Knowledge:
    pre_state: EnvironmentState
    action: Action
    reward: float
    post_state: EnvironmentState

    def as_tuple(self) -> tuple:
        return tuple(self.pre_state, self.action, self.reward, self.post_state)


def get_curr_pipe_velocity(game_manager: GameManager) -> int:
    return INITIAL_PIPE_SPEED + (game_manager.level * PIPE_SPEED_INCREASE_PER_LEVEL_UP)


def get_nearest_pipe_details(game_manager: GameManager) -> tuple[int, int, int]:
    unpassed_pipes = [pipe for pipe in game_manager.pipes if pipe.passed is False]
    if not unpassed_pipes:
        return (None, None, None)
    else:
        pipe: Pipe = min(unpassed_pipes, key=lambda pipe: pipe.x_pos)
        next_pipe_distance = (pipe.x_pos + PIPE_WIDTH) - game_manager.bird.x_pos
        next_pipe_gap_pos = pipe.gap_center
        next_pipe_gap_height = pipe.gap_height
    return (next_pipe_distance, next_pipe_gap_pos, next_pipe_gap_height)


def get_second_nearest_pipe_details(game_manager: GameManager) -> tuple[int, int, int]:
    unpassed_pipes = [pipe for pipe in game_manager.pipes if pipe.passed is False]
    if len(unpassed_pipes) < 2:
        return (None, None, None)
    else:
        second_pipe = sorted(unpassed_pipes, key=lambda pipe: pipe.x_pos)[1]
        second_pipe_distance = (second_pipe.x_pos + PIPE_WIDTH) - game_manager.bird.x_pos
        second_pipe_gap_pos = second_pipe.gap_center
        second_pipe_gap_height = second_pipe.gap_height

    return (second_pipe_distance, second_pipe_gap_pos, second_pipe_gap_height)


def print_debug_output(
    episode_num: int,
    total_episodes: int,
    exploration_rate: float,
    frames_survived: int,
    action_tick: int,
    target_frames: int,
):
    if frames_survived < target_frames:
        print(
            f"\tEpisode {episode_num + 1} / {total_episodes}, Exploration: {(exploration_rate):.2f} @ {(60 / action_tick):.0f}/sec ---> 💀 at {frames_survived} Frames"  # noqa: E501
        )
    else:
        print(f"\tEpisode {episode_num + 1} / {total_episodes}, ✅ SURVIVE!!")
