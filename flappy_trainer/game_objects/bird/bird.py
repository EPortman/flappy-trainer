"""
Bird

This class represents the playable bird in the Flappy Bird game. It extends the `BaseBird`
abstract class to implement specific gameplay mechanics such as movement, animations,
and state transitions. The `Bird` class manages its position, velocity, and game state
(e.g., alive or dead).

Key Features:
- Updates position and velocity based on gravity and player input.
- Manages animation states and frame updates for visual feedback.
- Provides collision representation for game mechanics.
- Supports resetting bird state for a new game.
"""

import pygame

from flappy_trainer.config import BIRD_START_X_POS, BIRD_START_Y_POS, DEBUG
from flappy_trainer.game_objects.bird.bird_base import BaseBird
from flappy_trainer.utils import BirdFrame, BirdState


class Bird(BaseBird):
    FLAPPING_UP_THRESHOLD = -5  # Velocity threshold for transitioning to flapping-up animation
    NOSE_DIVE_THRESHOLD = 6  # Velocity threshold for transitioning to nose-dive animation

    def __init__(self):
        super().__init__()
        self.y_velocity = 0
        self.is_alive = True

    def update(self, delta_time: float):
        """Update the bird's position, velocity, and animation state."""
        self._update_y_velocity(delta_time)
        self._update_y_position()
        self._update_animation_state()
        super().update_bird_frame(delta_time)

    def flap(self):
        """Make the bird flap upwards, adjusting its velocity and animation state."""
        self.y_velocity = -self.flap_force
        self.animation_state = BirdState.FLAPPING_UP

    def die(self):
        """End the game by marking the bird as no longer alive."""
        self.is_alive = False

    def draw(self, screen: pygame.Surface):
        """Render the bird's current sprite on the screen."""
        # Draw the bird's sprite
        current_image = self.sprite_sheet.get_frame(self.current_frame)
        screen.blit(current_image, (self.x_pos, self.y_pos))

        # Draw the collision radius as a circle (debugging)
        if DEBUG:
            bird_center = (
                self.x_pos + current_image.get_width() // 2,
                self.y_pos + current_image.get_height() // 2,
            )
            pygame.draw.circle(screen, (255, 0, 0), bird_center, self.radius, 3)

    def reset(self):
        """Reset the bird's position, velocity, and state for a new game."""
        self.x_pos = BIRD_START_X_POS
        self.y_pos = BIRD_START_Y_POS
        self.y_velocity = 0
        self.is_alive = True
        self.current_frame = BirdFrame.FLAPPING_TOP
        self.animation_state = BirdState.IDLE

    def _update_y_velocity(self, delta_time: float):
        """Update the bird's vertical velocity based on gravity, flap decay, and delta time."""
        if self.animation_state == BirdState.FLAPPING_UP:
            self.y_velocity *= self.flap_decay
        self.y_velocity += self.gravity * delta_time

    def _update_y_position(self):
        """Adjust the bird's vertical position based on its velocity."""
        self.y_pos += self.y_velocity

    def _update_animation_state(self):
        """Determine the bird's animation state based on its current velocity."""
        if self.y_velocity < self.FLAPPING_UP_THRESHOLD:
            new_state = BirdState.FLAPPING_UP
        elif self.FLAPPING_UP_THRESHOLD <= self.y_velocity < 0:
            new_state = BirdState.TRANSITION
        elif self.y_velocity > self.NOSE_DIVE_THRESHOLD:
            new_state = BirdState.NOSE_DIVE
        elif self.y_velocity > 0:
            new_state = BirdState.DESCENDING
        else:
            new_state = BirdState.IDLE

        # Update the animation state if it has changed
        if new_state != self.animation_state:
            self.animation_state = new_state
