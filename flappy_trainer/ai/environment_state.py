import numpy as np


class EnvironmentState:
    def __init__(
        self,
        bird_is_alive: bool,
        bird_vert_pos: int,
        bird_vert_velocity: int,
        distance_to_next_pipe: int,
        next_pipe_top_height: int,
        next_pipe_bot_height: int,
        pipe_velocity: int,
    ):
        self.bird_is_alive = bird_is_alive
        self.bird_vert_pos = bird_vert_pos
        self.bird_vert_velocity = bird_vert_velocity
        self.distance_to_next_pipe = distance_to_next_pipe
        self.next_pipe_top_height = next_pipe_top_height
        self.next_pipe_bot_height = next_pipe_bot_height
        self.pipe_velocity = pipe_velocity

    def to_numpy_array(self) -> np.array:
        return np.array(
            [
                self.bird_is_alive,
                self.bird_vert_pos,
                self.bird_vert_velocity,
                self.distance_to_next_pipe,
                self.next_pipe_top_height,
                self.next_pipe_bot_height,
                self.pipe_velocity,
            ]
        )
