from utils import get_env_var_as_int
from game_objects.base_bird import BaseBird


class Bird(BaseBird):
    def __init__(self):
        """Initialize the bird."""
        super().__init__()
        self.flap_force = get_env_var_as_int("BIRD_FLAP_FORCE")
        self.gravity = 0.5
        self.velocity = 0
        self.is_alive = True
        self.previous_state = None  # Track the previous state to avoid resetting frames unnecessarily

    def update(self, delta_time):
        """Update the bird's position based on gravity and velocity."""
        # Update position
        self.velocity += self.gravity
        self.y += self.velocity

        # Determine the animation state based on the bird's velocity
        new_state = None

        if self.velocity < 0:  # Bird is moving upwards
            new_state = "flapping_up"
        elif self.velocity > 6:  # Bird is falling quickly (nosedive)
            new_state = "nosedive"
        elif self.velocity > 0:  # Bird is descending normally
            new_state = "descending"
        else:  # Bird is idle (velocity near zero)
            new_state = "idle"

        # Only update the animation state if it has changed
        if new_state != self.previous_state:
            self.set_animation_state(new_state)
            self.previous_state = new_state

        # Call the base update to handle the animation
        super().update(delta_time)

    def flap(self):
        """Make the bird flap upwards by adjusting the velocity."""
        self.velocity = self.flap_force
        self.set_animation_state("flapping_up")
        self.previous_state = "flapping_up"

    def die(self):
        """Kill the bird ending the game."""
        self.is_alive = False

    def reset(self):
        """Reset the bird's position and velocity."""
        self.x = get_env_var_as_int("BIRD_START_X_POS")
        self.y = get_env_var_as_int("BIRD_START_Y_POS")
        self.velocity = 0
        self.is_alive = True
        self.current_frame = 0  # Reset the frame to the initial frame
        self.set_animation_state("idle")
        self.previous_state = "idle"

