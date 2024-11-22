import pygame
import pytest

from flappy_trainer.config import BIRD_ANIMATION_TIME, BIRD_START_X_POS, BIRD_START_Y_POS
from flappy_trainer.game_managers.game_manager import GameManager
from flappy_trainer.game_objects.bird.bird import Bird
from flappy_trainer.utils import BirdFrame, BirdState


class TestBird:
    def setup_method(self):
        """Set up the test environment before each test."""
        pygame.init()
        self.game_manager = GameManager()
        self.game_manager.start_game()
        self.bird: Bird = self.game_manager.bird

    def teardown_method(self):
        """Clean up the test environment after each test."""
        pygame.quit()

    def test_initialization(self):
        """Test that the bird initializes with correct default properties."""
        assert self.bird.x_pos == BIRD_START_X_POS
        assert self.bird.y_pos == BIRD_START_Y_POS
        assert self.bird.y_velocity == 0
        assert self.bird.is_alive is True
        assert self.bird.animation_state == BirdState.IDLE
        assert self.bird.current_frame == BirdFrame.FLAPPING_TOP

    def test_flap(self):
        """Test that the bird flaps correctly."""
        self.bird.flap()
        assert self.bird.y_velocity == -self.bird.flap_force
        assert self.bird.animation_state == BirdState.FLAPPING_UP

    def test_die(self):
        """Test that the bird dies correctly."""
        self.bird.die()
        assert self.bird.is_alive is False

    def test_reset(self):
        """Test that the bird resets its state correctly."""
        self.bird.flap()
        self.bird.die()
        self.bird.reset()
        assert self.bird.x_pos == BIRD_START_X_POS
        assert self.bird.y_pos == BIRD_START_Y_POS
        assert self.bird.y_velocity == 0
        assert self.bird.is_alive is True
        assert self.bird.animation_state == BirdState.IDLE
        assert self.bird.current_frame == BirdFrame.FLAPPING_TOP

    def test_update_y_velocity(self):
        """Test that the bird's velocity updates correctly."""
        initial_velocity = self.bird.y_velocity
        self.bird.update(0.1)
        assert self.bird.y_velocity == initial_velocity + self.bird.gravity * 0.1

    def test_update_y_position_flapping_up(self):
        """Test the bird's position updates correctly while flapping up."""
        self.bird.animation_state = BirdState.FLAPPING_UP
        self.bird.y_velocity = -1.0
        initial_y = self.bird.y_pos
        delta_time = 0.1
        expected_velocity = self.bird.y_velocity * self.bird.flap_decay + (self.bird.gravity * delta_time)
        expected_y = initial_y + expected_velocity
        self.bird.update(delta_time)
        assert self.bird.y_pos == expected_y

    def test_update_y_position_descending(self):
        """Test the bird's position updates correctly while descending."""
        self.bird.animation_state = BirdState.DESCENDING
        self.bird.y_velocity = 2.0
        initial_y = self.bird.y_pos
        delta_time = 0.1
        expected_velocity = self.bird.y_velocity + (self.bird.gravity * delta_time)
        expected_y = initial_y + expected_velocity
        self.bird.update(delta_time)
        assert self.bird.y_pos == expected_y

    def test_gravity_applied_over_time(self):
        """Test that gravity consistently affects the bird's velocity over time."""
        initial_velocity = self.bird.y_velocity
        delta_time = 0.1
        self.bird.update(delta_time)
        self.bird.update(delta_time)
        expected_velocity = initial_velocity + 2 * (self.bird.gravity * delta_time)
        assert self.bird.y_velocity == pytest.approx(expected_velocity)

    def test_update_animation_state(self):
        """Test that the bird's animation state updates based on its velocity."""
        self.bird.y_velocity = -6
        self.bird._update_animation_state()
        assert self.bird.animation_state == BirdState.FLAPPING_UP

        self.bird.y_velocity = -1
        self.bird._update_animation_state()
        assert self.bird.animation_state == BirdState.TRANSITION

        self.bird.y_velocity = 7
        self.bird._update_animation_state()
        assert self.bird.animation_state == BirdState.NOSE_DIVE

        self.bird.y_velocity = 2
        self.bird._update_animation_state()
        assert self.bird.animation_state == BirdState.DESCENDING

        self.bird.y_velocity = 0
        self.bird._update_animation_state()
        assert self.bird.animation_state == BirdState.IDLE

    def test_draw(self):
        """Test that the bird's draw method renders without error."""
        screen = pygame.Surface((800, 600))  # Mock screen for testing
        try:
            self.bird.draw(screen)
        except Exception as e:
            pytest.fail(f"Bird.draw() raised an exception: {e}")

    def test_get_rect(self):
        """Test that the bird's collision rectangle matches its position and frame."""
        rect = self.bird.get_rect()
        current_frame_image = self.bird.sprite_sheet.get_frame(self.bird.current_frame)
        expected_rect = current_frame_image.get_rect(topleft=(self.bird.x_pos, self.bird.y_pos))
        assert rect == expected_rect

    def test_animation_frame_updates(self):
        """Test that the bird's animation frame updates correctly."""
        initial_frame = self.bird.current_frame
        self.bird.animation_state = BirdState.FLAPPING_UP
        self.bird.update_bird_frame(BIRD_ANIMATION_TIME)
        assert self.bird.current_frame != initial_frame
