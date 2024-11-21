"""
BaseBird Abstract Class

This class provides the foundation for managing bird behavior and animations in Flappy Bird.
It defines shared functionality such as position, physics, and animation handling. Concrete bird
implementations, like `Bird`, should extend this class and provide additional logic for gameplay.

Key Features:
- Manages bird position, physics (gravity and flap), and animation states.
- Handles frame updates based on animation state and time elapsed.
- Designed to be extended by specific bird implementations.
"""

from abc import ABC, abstractmethod

import pygame

from flappy_trainer.config import (
    BIRD_ANIMATION_TIME,
    BIRD_COLOR,
    BIRD_FLAP_DECAY_FORCE,
    BIRD_FLAP_FORCE,
    BIRD_GRAVITY,
    BIRD_RADIUS,
    BIRD_START_X_POS,
    BIRD_START_Y_POS,
)
from flappy_trainer.game_objects.bird.bird_spritesheet import BirdSpriteSheet
from flappy_trainer.utils import BirdFrame, BirdState


class BaseBird(ABC):
    def __init__(self) -> None:
        self._initialize_position()
        self._initialize_physics()
        self._initialize_animation()

    def update_bird_frame(self, delta_time: float) -> None:
        """Update the bird's animation frame based on its current state and delta time."""
        self.time_since_animation_change += delta_time

        if self.time_since_animation_change >= self.animation_time:
            self._update_animation_frame()
            self.time_since_animation_change = 0

    def get_rect(self) -> pygame.Rect:
        """Get the rectangle representing the bird for collision detection."""
        current_frame_image = self.sprite_sheet.get_frame(self.current_frame)
        return current_frame_image.get_rect(topleft=(self.x_pos, self.y_pos))

    @abstractmethod
    def update(self, delta_time: float) -> None:
        """Update the bird's state based on game logic."""
        pass

    @abstractmethod
    def flap(self) -> None:
        """Handle bird flapping logic."""
        pass

    @abstractmethod
    def die(self) -> None:
        """Handle bird death logic."""
        pass

    @abstractmethod
    def draw(self, screen) -> None:
        """Render the bird to the screen."""
        pass

    def _initialize_position(self) -> None:
        """Set initial position-related properties."""
        self.x_pos = BIRD_START_X_POS
        self.y_pos = BIRD_START_Y_POS
        self.radius = BIRD_RADIUS
        self.color = BIRD_COLOR

    def _initialize_physics(self) -> None:
        """Set initial physics-related properties."""
        self.gravity = BIRD_GRAVITY
        self.flap_force = BIRD_FLAP_FORCE
        self.flap_decay = BIRD_FLAP_DECAY_FORCE

    def _initialize_animation(self) -> None:
        """Set initial animation-related properties."""
        self.sprite_sheet = BirdSpriteSheet()
        self.previous_state = BirdState.NONE
        self.animation_state = BirdState.IDLE
        self.current_frame = BirdFrame.FLAPPING_TOP
        self.animation_time = BIRD_ANIMATION_TIME  # Time between frames in seconds
        self.time_since_animation_change = 0

    def _update_animation_frame(self) -> None:
        """Update the current frame based on the animation state."""
        if self.animation_state == BirdState.FLAPPING_UP:
            self._handle_flapping_up_animation()
        elif self.animation_state == BirdState.TRANSITION:
            self.current_frame = BirdFrame.DESCENDING_START
        elif self.animation_state == BirdState.DESCENDING:
            self._handle_descending_animation()
        elif self.animation_state == BirdState.NOSE_DIVE:
            self.current_frame = BirdFrame.NOSE_DIVE
        else:
            self.current_frame = BirdFrame.FLAPPING_TOP

    def _handle_flapping_up_animation(self) -> None:
        """Cycle through flapping frames for the upward flap animation."""
        self.current_frame = self.sprite_sheet.get_next_frame(
            current_frame=self.current_frame,
            start_frame=BirdFrame.FLAPPING_START,
            end_frame=BirdFrame.FLAPPING_END,
        )

    def _handle_descending_animation(self) -> None:
        """Cycle through descending frames as the bird falls."""
        if self.current_frame != BirdFrame.DESCENDING_END:
            self.current_frame = self.sprite_sheet.get_next_frame(
                current_frame=self.current_frame,
                start_frame=BirdFrame.DESCENDING_START,
                end_frame=BirdFrame.DESCENDING_END,
            )
        else:
            self.current_frame = BirdFrame.DESCENDING_END
