from flappy_trainer.game_objects.bird.bird_spritesheet import BirdSpriteSheet
from flappy_trainer.utils import (
    BirdFrame,
    BirdState,
    get_env_var_as_float,
    get_env_var_as_int,
    get_env_var_as_tuple,
)


class BaseBird:
    def __init__(self) -> None:
        """Initialize the base bird."""
        self._initialize_position()
        self._initialize_physics()
        self._initialize_animation()

    def update_bird_frame(self, delta_time: float) -> None:
        """Update the bird's animation frame based on its current state and delta time."""
        self.time_since_animation_change += delta_time

        if self.time_since_animation_change >= self.animation_time:
            self._update_animation_frame()
            self.time_since_animation_change = 0

    def _initialize_position(self) -> None:
        """Initialize the bird's position-related properties."""
        self.x_pos = get_env_var_as_int("BIRD_START_X_POS")
        self.y_pos = get_env_var_as_int("BIRD_START_Y_POS")
        self.radius = get_env_var_as_int("BIRD_RADIUS")
        self.color = get_env_var_as_tuple("BIRD_COLOR")

    def _initialize_physics(self) -> None:
        """Initialize the bird's physics-related properties."""
        self.gravity = get_env_var_as_float("BIRD_GRAVITY")
        self.flap_force = get_env_var_as_int("BIRD_FLAP_FORCE")
        self.flap_decay = get_env_var_as_float("BIRD_FLAP_DECAY_FORCE")

    def _initialize_animation(self) -> None:
        """Initialize the bird's animation-related properties."""
        self.sprite_sheet = BirdSpriteSheet()
        self.previous_state = BirdState.NONE
        self.animation_state = BirdState.IDLE
        self.current_frame = BirdFrame.FLAPPING_TOP
        self.animation_time = 0.05  # Time between frames in seconds
        self.time_since_animation_change = 0

    def _update_animation_frame(self) -> None:
        """Update the current animation frame based on the bird's animation state."""
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
        """Handle the animation frames for when the bird is flapping up."""
        self.current_frame = self.sprite_sheet.get_next_frame(
            current_frame=self.current_frame,
            start_frame=BirdFrame.FLAPPING_START,
            end_frame=BirdFrame.FLAPPING_END,
        )

    def _handle_descending_animation(self) -> None:
        """Handle the animation frames for when the bird is descending."""
        if self.current_frame != BirdFrame.DESCENDING_END:
            self.current_frame = self.sprite_sheet.get_next_frame(
                current_frame=self.current_frame,
                start_frame=BirdFrame.DESCENDING_START,
                end_frame=BirdFrame.DESCENDING_END,
            )
        else:
            self.current_frame = BirdFrame.DESCENDING_END
