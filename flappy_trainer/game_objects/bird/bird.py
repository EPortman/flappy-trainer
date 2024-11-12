import pygame

from flappy_trainer.game_objects.bird.bird_base import BaseBird
from flappy_trainer.utils import BirdFrame, BirdState, get_env_var_as_int


class Bird(BaseBird):
    FLAPPING_UP_THRESHOLD = -5
    NOSE_DIVE_THRESHOLD = 6

    def __init__(self):
        super().__init__()
        self.y_velocity = 0
        self.is_alive = True

    def update(self, delta_time) -> None:
        """Update the bird's y position and animation frame."""
        self._update_y_velocity(delta_time)
        self._update_y_position()
        self._update_animation_state()
        super().update_bird_frame(delta_time)

    def flap(self) -> None:
        """Make the bird flap upwards by adjusting the velocity."""
        self.y_velocity = -self.flap_force
        self.animation_state = BirdState.FLAPPING_UP

    def die(self) -> None:
        """Kill the bird ending the game."""
        self.is_alive = False

    def get_rect(self) -> pygame.Rect:
        """Get the rectangle representing the bird for collision detection."""
        current_frame_image = self.sprite_sheet.get_frame(self.current_frame)
        return current_frame_image.get_rect(topleft=(self.x_pos, self.y_pos))

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the bird on the screen and show its hit radius for debugging."""
        # Draw the bird's current sprite
        current_image = self.sprite_sheet.get_frame(self.current_frame)
        screen.blit(current_image, (self.x_pos, self.y_pos))
        
        # Calculate the center of the bird for the hit radius
        bird_center = (
            self.x_pos + current_image.get_width() // 2,
            self.y_pos + current_image.get_height() // 2
        )
        
        # Draw the hit radius as a circle (for debugging)
        pygame.draw.circle(screen, (255, 0, 0), bird_center, self.radius, 3)

    def reset(self) -> None:
        """Reset the bird's position, velocity, and state."""
        self.x_pos = get_env_var_as_int("BIRD_START_X_POS")
        self.y_pos = get_env_var_as_int("BIRD_START_Y_POS")
        self.y_velocity = 0
        self.is_alive = True
        self.current_frame = BirdFrame.FLAPPING_TOP
        self.set_animation_state(BirdState.IDLE)

    def _update_y_velocity(self, delta_time: float) -> None:
        """Update position based on gravity, velocity, delta_time, and flap decay."""
        if self.animation_state == BirdState.FLAPPING_UP:
            self.y_velocity *= self.flap_decay
        self.y_velocity += self.gravity * delta_time

    def _update_y_position(self) -> None:
        """Update the bird's position based on the current y velocity."""
        self.y_pos += self.y_velocity

    def _update_animation_state(self) -> None:
        """Update the bird's animation state based on its velocity."""
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

        if new_state != self.animation_state:
            self.animation_state = new_state
