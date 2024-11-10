import pygame
from utils import get_env_var_as_int, get_env_var_as_tuple


class Bird:
    def __init__(self):
        """Initialize the bird."""
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
        self.flap_force = get_env_var_as_int("BIRD_FLAP_FORCE")
        self.gravity = 0.5
        self.velocity = 0
        self.is_alive = True
        self.animation_time = 0.05  # Time between frames in seconds for faster animation
        self.current_time = 0  # Track elapsed time for frame switching

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

    def update(self, delta_time):
        """Update the bird's position based on gravity and velocity."""
        # Update position
        self.velocity += self.gravity
        self.y += self.velocity

        # Update animation frame based on movement
        if self.velocity < 0:  # Bird is moving upwards
            # Cycle through frames 7 to 10 as the bird flaps upwards
            self.current_time += delta_time
            if self.current_time >= self.animation_time:
                if self.current_frame < 7 or self.current_frame > 10:
                    self.current_frame = 7
                else:
                    self.current_frame = (self.current_frame + 1) if self.current_frame < 10 else 7
                self.current_time = 0
        elif self.velocity > 0:  # Bird is moving downwards
            if self.velocity > 5:  # Arbitrary threshold for a nosedive
                self.current_frame = 6
            else:
                self.current_time += delta_time
                if self.current_time >= self.animation_time:
                    if self.current_frame < 2 or self.current_frame > 5:
                        self.current_frame = 2
                    else:
                        self.current_frame = (
                            (self.current_frame + 1) if self.current_frame < 5 else 2
                        )
                    self.current_time = 0
        else:  # Bird is at the peak of the arc (velocity is near zero)
            self.current_frame = 1  # Frame 1 represents the top position

    def flap(self):
        """Make the bird flap upwards by adjusting the velocity."""
        self.velocity = self.flap_force
        self.current_frame = 7  # Start the upward flap animation

    def get_rect(self):
        """Get the rectangle representing the bird for collision detection."""
        return self.frames[self.current_frame].get_rect(topleft=(self.x, self.y))

    def die(self):
        """Kill the bird ending the game"""
        self.is_alive = False

    def draw(self, screen):
        """Draw the bird on the screen."""
        current_image = self.frames[self.current_frame]
        screen.blit(current_image, (self.x, self.y))

    def reset(self):
        """Reset the bird's position and velocity."""
        self.x = get_env_var_as_int("BIRD_START_X_POS")
        self.y = get_env_var_as_int("BIRD_START_Y_POS")
        self.velocity = 0
        self.is_alive = True
        self.current_frame = 0  # Reset the frame to the initial frame
