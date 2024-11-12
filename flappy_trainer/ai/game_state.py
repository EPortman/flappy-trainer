import numpy as np

from flappy_trainer.utils import get_env_var_as_int


class GameState:
    def __init__(
        self,
        bird_vert_pos: int,
        bird_vert_velocity: int,
        distance_to_next_pipe: int,
        next_pipe_top_open_pos: int,
        next_pipe_bot_open_pos: int,
        pipe_velocity: int,
    ):
        self.bird_vert_pos = bird_vert_pos
        self.bird_vert_velocity = bird_vert_velocity
        self.distance_to_next_pipe = distance_to_next_pipe
        self.next_pipe_top_open_pos = next_pipe_top_open_pos
        self.next_pipe_bot_open_pos = next_pipe_bot_open_pos
        self.pipe_velocity = pipe_velocity

    def to_numpy_array(self) -> np.array:
        return np.array(
            [
                self.bird_vert_pos,
                self.bird_vert_velocity,
                self.distance_to_next_pipe,
                self.next_pipe_top_open_pos,
                self.next_pipe_bot_open_pos,
                self.pipe_velocity,
            ]
        )

    @classmethod
    def get_initial_game_state(cls) -> "GameState":
        init_bird_vert_pos = get_env_var_as_int("BIRD_START_Y_POS")
        init_bird_vert_velocity = get_env_var_as_int("BIRD_START_Y_VELOCITY")
        init_pipe_speed = get_env_var_as_int("PIPE_SPEED") * (1 / 60)

        return cls(
            bird_vert_pos=init_bird_vert_pos,
            bird_vert_velocity=init_bird_vert_velocity,
            distance_to_next_pipe=None,
            next_pipe_top_open_pos=None,
            next_pipe_bot_open_pos=None,
            pipe_velocity=init_pipe_speed,
        )
