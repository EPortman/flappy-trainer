import pygame
from utils import get_env_var_as_int, get_env_var_as_tuple


class BaseBird:
    def __init__(self):
        """Initialize the base bird."""
        sprite_sheet_path = "assets/sprites/bird_spritesheet.png"
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.frames = self.load_frames(
            start_y=75, frame_width=57, frame_height=57, num_frames=11, padding=2
        )
        self.current_frame = 0
        self.x = get_env_var_as_int("BIRD_START_X_POS")
        self.y = get_env_var_as_int("BIRD_START_Y_POS")
        self.radius = get_env_var_as_int("BIRD_RADIUS")
        self.color = get_env_var_as_tuple("BIRD_COLOR")
        self.animation_time = 0.05
        self.current_time = 0

        # Animation state
        self.animation_state = "idle"

    def load_frames(self, start_y, frame_width, frame_height, num_frames, padding):
        """Load specific frames from a given row in a sprite sheet."""
        frames = []
        for i in range(num_frames):
            # Add an initial margin of 2 pixels before the first frame and add pad between frames
            x = (
                i * (frame_width + padding)
            ) + padding  # Shift all frames to account for the initial margin
            y = start_y

            # Make sure the extracted frame is precise
            frame_rect = pygame.Rect(x, y, frame_width, frame_height)
            frame = self.sprite_sheet.subsurface(
                frame_rect
            ).copy()  # Use .copy() to prevent referencing issues

            # Add the frame to the list
            frames.append(frame)
        return frames

    def set_animation_state(self, state):
        """Set the animation state for the bird."""
        self.animation_state = state

    def update(self, delta_time):
        """Update the bird's animation frame based on its current state."""
        # Update the animation frame based on the current state
        self.current_time += delta_time
        if self.current_time >= self.animation_time:
            if self.animation_state == "flapping_up":
                self.current_frame = self._cycle_frames(7, 10)
            elif self.animation_state == "nosedive":
                self.current_frame = 6
            elif self.animation_state == "descending":
                self.current_frame = self._cycle_frames(2, 5)
            elif self.animation_state == "idle":
                self.current_frame = 1
            self.current_time = 0

    def _cycle_frames(self, start_frame, end_frame):
        """Cycle through the frames in a given range."""
        if self.current_frame < start_frame or self.current_frame > end_frame:
            return start_frame
        return (self.current_frame + 1) if self.current_frame < end_frame else start_frame

    def get_rect(self):
        """Get the rectangle representing the bird for collision detection."""
        return self.frames[self.current_frame].get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        """Draw the bird on the screen."""
        current_image = self.frames[self.current_frame]
        screen.blit(current_image, (self.x, self.y))
