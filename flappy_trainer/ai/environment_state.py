import numpy as np

from flappy_trainer.config import MAX_BIRD_VELOCITY, MAX_PIPE_VELOCITY, SCREEN_HEIGHT, SCREEN_WIDTH


class EnvironmentState:
    def __init__(
        self,
        bird_is_alive: bool,
        bird_vert_pos: int,
        bird_vert_velocity: int,
        pipe_velocity: int,
        next_pipe_distance: int | None = None,
        next_pipe_gap_pos: int | None = None,
        next_pipe_gap_height: int | None = None,
    ):
        """
        Initializes the environment state. If pipe-related values are None,
        defaults are set to ensure meaningful training data.
        """
        self.bird_is_alive = bird_is_alive
        self.bird_vert_pos = bird_vert_pos
        self.bird_vert_velocity = bird_vert_velocity
        self.pipe_velocity = pipe_velocity
        self.next_pipe_distance = SCREEN_WIDTH if next_pipe_distance is None else next_pipe_distance
        self.next_pipe_gap_pos = (
            SCREEN_HEIGHT // 2 if next_pipe_gap_pos is None else next_pipe_gap_pos
        )
        self.next_pipe_gap_height = (
            SCREEN_HEIGHT // 4 if next_pipe_gap_height is None else next_pipe_gap_height
        )

    def to_numpy_array(self, include_batch_dim: bool = False) -> np.ndarray:
        """
        Converts the current state to a normalized numpy array for TensorFlow compatibility.

        Args:
            include_batch_dim (bool): If True, adds a batch dimension (shape: [1, num_features])
                                      for compatibility with TensorFlow models.

        Returns:
            np.array: Normalized feature array representing the current environment state.
        """
        data = np.array(
            [
                self.bird_vert_pos / SCREEN_HEIGHT,
                self.bird_vert_velocity / MAX_BIRD_VELOCITY,
                self.pipe_velocity / MAX_PIPE_VELOCITY,
                self.next_pipe_distance / SCREEN_WIDTH,
                self.next_pipe_gap_pos / SCREEN_HEIGHT,
                self.next_pipe_gap_height / SCREEN_HEIGHT,
            ],
            dtype=np.float32,  # Ensure compatibility with tensorflow operations
        )
        if include_batch_dim:
            return data.reshape(1, -1)  # Shape: [1, num_features]
        return data  # Shape: [num_features]

    @classmethod
    def get_num_features(cls) -> int:
        """Retrieves the number of features used in the environment state representation."""
        return 6
