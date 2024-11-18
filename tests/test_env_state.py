import numpy as np

from flappy_trainer.ai.environment_state import EnvironmentState
from flappy_trainer.config import MAX_BIRD_VELOCITY, MAX_PIPE_VELOCITY, SCREEN_HEIGHT, SCREEN_WIDTH


class TestEnvironmentState:
    def test_initialization_defaults(self):
        """Test that default values are correctly assigned when None is provided."""
        state = EnvironmentState(
            bird_is_alive=True,
            bird_vert_pos=200,
            bird_vert_velocity=10,
            pipe_velocity=5,
            next_pipe_distance=None,
            next_pipe_gap_pos=None,
            next_pipe_gap_height=None,
        )
        assert state.next_pipe_distance == SCREEN_WIDTH
        assert state.next_pipe_gap_pos == SCREEN_HEIGHT // 2
        assert state.next_pipe_gap_height == SCREEN_HEIGHT // 4

    def test_initialization_custom_values(self):
        """Test that provided values are correctly assigned."""
        state = EnvironmentState(
            bird_is_alive=True,
            bird_vert_pos=150,
            bird_vert_velocity=8,
            pipe_velocity=3,
            next_pipe_distance=400,
            next_pipe_gap_pos=250,
            next_pipe_gap_height=100,
        )
        assert state.next_pipe_distance == 400
        assert state.next_pipe_gap_pos == 250
        assert state.next_pipe_gap_height == 100

    def test_to_numpy_array_no_batch(self):
        """Test the `to_numpy_array` method without a batch dimension."""
        state = EnvironmentState(
            bird_is_alive=True,
            bird_vert_pos=300,
            bird_vert_velocity=15,
            pipe_velocity=7,
            next_pipe_distance=500,
            next_pipe_gap_pos=350,
            next_pipe_gap_height=120,
        )
        expected_array = np.array(
            [
                300 / SCREEN_HEIGHT,
                15 / MAX_BIRD_VELOCITY,
                7 / MAX_PIPE_VELOCITY,
                500 / SCREEN_WIDTH,
                350 / SCREEN_HEIGHT,
                120 / SCREEN_HEIGHT,
            ],
            dtype=np.float32,
        )
        result_array = state.to_numpy_array(include_batch_dim=False)
        np.testing.assert_array_almost_equal(result_array, expected_array)

    def test_to_numpy_array_with_batch(self):
        """Test the `to_numpy_array` method with a batch dimension."""
        state = EnvironmentState(
            bird_is_alive=True,
            bird_vert_pos=300,
            bird_vert_velocity=15,
            pipe_velocity=7,
            next_pipe_distance=500,
            next_pipe_gap_pos=350,
            next_pipe_gap_height=120,
        )
        expected_array = np.array(
            [
                [
                    300 / SCREEN_HEIGHT,
                    15 / MAX_BIRD_VELOCITY,
                    7 / MAX_PIPE_VELOCITY,
                    500 / SCREEN_WIDTH,
                    350 / SCREEN_HEIGHT,
                    120 / SCREEN_HEIGHT,
                ]
            ],
            dtype=np.float32,
        )
        result_array = state.to_numpy_array(include_batch_dim=True)
        assert result_array.shape == (1, 6)
        np.testing.assert_array_almost_equal(result_array, expected_array)

    def test_get_num_features(self):
        """Test the `get_num_features` method."""
        assert EnvironmentState.get_num_features() == 6

    def test_normalization_with_extreme_values(self):
        """Test that the normalization works with extreme values."""
        state = EnvironmentState(
            bird_is_alive=True,
            bird_vert_pos=SCREEN_HEIGHT,
            bird_vert_velocity=MAX_BIRD_VELOCITY * -1,
            pipe_velocity=MAX_PIPE_VELOCITY,
            next_pipe_distance=SCREEN_WIDTH,
            next_pipe_gap_pos=SCREEN_HEIGHT,
            next_pipe_gap_height=SCREEN_HEIGHT,
        )
        expected_array = np.array([1.0, -1.0, 1.0, 1.0, 1.0, 1.0], dtype=np.float32)
        result_array = state.to_numpy_array(include_batch_dim=False)
        np.testing.assert_array_equal(result_array, expected_array)

    def test_normalization_with_zero_values(self):
        """Test that the normalization works with zero values."""
        state = EnvironmentState(
            bird_is_alive=True,
            bird_vert_pos=0,
            bird_vert_velocity=0,
            pipe_velocity=0,
            next_pipe_distance=0,
            next_pipe_gap_pos=0,
            next_pipe_gap_height=0,
        )
        expected_array = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float32)
        result_array = state.to_numpy_array(include_batch_dim=False)
        np.testing.assert_array_equal(result_array, expected_array)

    def test_normalization_with_mid_values(self):
        """Test that the normalization works with mid values."""
        state = EnvironmentState(
            bird_is_alive=True,
            bird_vert_pos=SCREEN_HEIGHT / 2,
            bird_vert_velocity=MAX_BIRD_VELOCITY / 2,
            pipe_velocity=MAX_PIPE_VELOCITY / 2,
            next_pipe_distance=SCREEN_WIDTH / 2,
            next_pipe_gap_pos=SCREEN_HEIGHT / 2,
            next_pipe_gap_height=SCREEN_HEIGHT / 2,
        )
        expected_array = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5], dtype=np.float32)
        result_array = state.to_numpy_array(include_batch_dim=False)
        np.testing.assert_array_equal(result_array, expected_array)
