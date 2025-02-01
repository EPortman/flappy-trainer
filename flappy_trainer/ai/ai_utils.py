import csv
import os
from dataclasses import dataclass
from enum import Enum

from flappy_trainer.ai.environment_state import EnvironmentState
from flappy_trainer.config import INITIAL_PIPE_SPEED, PIPE_SPEED_INCREASE_PER_LEVEL_UP, PIPE_WIDTH
from flappy_trainer.game_managers.game_manager import GameManager
from flappy_trainer.game_objects.pipe.pipe import Pipe
from flappy_trainer.utils import GameState


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


def get_current_state(game_manager: GameManager) -> EnvironmentState:
    bird_is_alive = game_manager.state == GameState.RUNNING
    bird_vert_pos = game_manager.bird.y_pos
    bird_vert_velocity = game_manager.bird.y_velocity
    pipe_velocity = get_curr_pipe_velocity(game_manager)
    dist_to_first_pipe, first_pipe_gap_pos, first_pipe_gap_height = get_nearest_pipe_details(game_manager)
    dist_to_sec_pipe, sec_pipe_gap_pos, sec_pipe_gap_height = get_second_nearest_pipe_details(game_manager)

    return EnvironmentState(
        bird_is_alive=bird_is_alive,
        bird_vert_pos=bird_vert_pos,
        bird_vert_velocity=bird_vert_velocity,
        pipe_velocity=pipe_velocity,
        next_pipe_distance=dist_to_first_pipe,
        next_pipe_gap_pos=first_pipe_gap_pos,
        next_pipe_gap_height=first_pipe_gap_height,
        second_pipe_distance=dist_to_sec_pipe,
        second_pipe_gap_pos=sec_pipe_gap_pos,
        second_pipe_gap_height=sec_pipe_gap_height,
    )


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


def record_training_output(
    episode_num: int, exploration_rate: float, frames_survived: int, file_name: str, curricula_num: int = 0
):
    # Print the episode output to the console
    print(f"Episode: {episode_num}, Explore Rate: {exploration_rate:.2f}, frames: {frames_survived}")

    # Record the episode output to a csv file
    csv_file = os.path.join("flappy_trainer/ai/training_logs", f"{file_name}-{curricula_num}.csv")

    is_first_entry = episode_num == 1 and file_name
    with open(csv_file, mode="w" if is_first_entry else "a", newline="") as file:
        writer = csv.writer(file)
        if is_first_entry:
            writer.writerow(["Episode", "Explore Rate", "Frames Survived"])
        writer.writerow([episode_num, f"{exploration_rate:.3f}", frames_survived])
