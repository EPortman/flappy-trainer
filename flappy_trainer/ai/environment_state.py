import numpy as np

from flappy_trainer.config import MAX_BIRD_VELOCITY, MAX_PIPE_VELOCITY, SCREEN_HEIGHT, SCREEN_WIDTH


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

    def to_numpy_array(self, include_batch_dim: bool = False) -> np.array:
        """
        Converts the current state to a normalized numpy array for TensorFlow compatibility.

        Args:
            include_batch_dim (bool): If True, adds a batch dimension (shape: [1, num_features])
                                      for compatibility with TensorFlow models.

        Returns:
            np.array: Normalized feature array representing the current environment state.
        """
        relative_pos_to_top = self.bird_vert_pos - self.next_pipe_top_height
        relative_pos_to_bottom = self.bird_vert_pos - self.next_pipe_bot_height
        pipe_gap_size = self.next_pipe_bot_height - self.next_pipe_top_height
        time_until_collision = (
            self.distance_to_next_pipe / self.pipe_velocity if self.pipe_velocity > 0 else 1
        )

        data = np.array(
            [
                1 if self.bird_is_alive else 0,
                self.bird_vert_pos / SCREEN_HEIGHT,
                self.bird_vert_velocity / MAX_BIRD_VELOCITY,
                self.pipe_velocity / MAX_PIPE_VELOCITY,
                self.distance_to_next_pipe / SCREEN_WIDTH,
                relative_pos_to_top / SCREEN_HEIGHT,
                relative_pos_to_bottom / SCREEN_HEIGHT,
                pipe_gap_size / SCREEN_HEIGHT,
                time_until_collision / SCREEN_WIDTH,
            ],
            dtype=np.float32,  # Ensure compatibility with tensorflow operations
        )
        if include_batch_dim:
            return data.reshape(1, -1)  # Shape: [1, num_features]
        return data  # Shape: [num_features]

    @classmethod
    def get_num_features(cls) -> int:
        """Retrieves the number of features used in the environment state representation."""
        dummy_instance = cls(
            bird_is_alive=True,
            bird_vert_pos=SCREEN_HEIGHT // 2,
            bird_vert_velocity=MAX_BIRD_VELOCITY // 2,
            distance_to_next_pipe=SCREEN_WIDTH // 2,
            next_pipe_top_height=SCREEN_HEIGHT // 3,
            next_pipe_bot_height=(SCREEN_HEIGHT * 2) // 3,
            pipe_velocity=MAX_PIPE_VELOCITY // 2,
        )
        return len(dummy_instance.to_numpy_array())
