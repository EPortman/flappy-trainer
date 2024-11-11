import numpy as np


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
