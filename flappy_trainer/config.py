from dotenv import load_dotenv

from flappy_trainer.utils import get_env_var_as_float, get_env_var_as_int, get_env_var_as_string, get_env_var_as_tuple

load_dotenv()

DEBUG = True

# Screen, Background, and Border
SCREEN_HEIGHT = get_env_var_as_int("SCREEN_HEIGHT")
SCREEN_WIDTH = get_env_var_as_int("SCREEN_WIDTH")
BACKGROUND_COLOR = get_env_var_as_tuple("BACKGROUND_COLOR")
BORDER_THICKNESS = get_env_var_as_int("BORDER_THICKNESS")
BORDER_COLOR = get_env_var_as_tuple("BORDER_COLOR")

# Game Management
START_LEVEL = get_env_var_as_int("START_LEVEL")
START_SCORE = get_env_var_as_int("START_SCORE")
SCORE_PER_LEVEL_UP = get_env_var_as_int("SCORE_PER_LEVEL_UP")
PIPE_SPEED_INCREASE_PER_LEVEL_UP = get_env_var_as_int("PIPE_SPEED_INCREASE_PER_LEVEL_UP")

# Pipe SpriteSheet
PIPE_SPRITE_SHEET_PATH = get_env_var_as_string("PIPE_SPRITE_SHEET_PATH")
PIPE_SPRITE_SHEET_FRAME_WIDTH = get_env_var_as_int("PIPE_SPRITE_SHEET_FRAME_WIDTH")
PIPE_SPRITE_SHEET_FRAME_HEIGHT = get_env_var_as_int("PIPE_SPRITE_SHEET_FRAME_HEIGHT")
PIPE_SPRITE_SHEET_SCALE_FACTOR = get_env_var_as_float("PIPE_SPRITE_SHEET_SCALE_FACTOR")

# Pipe Physics
INITIAL_PIPE_SPEED = get_env_var_as_int("PIPE_SPEED")
PIPE_SPEED_INCREASE_PER_LEVEL_UP = get_env_var_as_int("PIPE_SPEED_INCREASE_PER_LEVEL_UP")
MAX_PIPE_VELOCITY = get_env_var_as_int("MAX_PIPE_SPEED")
PIPE_WIDTH = get_env_var_as_int("PIPE_WIDTH")
PIPE_MIN_HEIGHT = get_env_var_as_int("PIPE_MIN_HEIGHT")
PIPE_MIN_GAP_HEIGHT = get_env_var_as_int("PIPE_MIN_GAP_HEIGHT")
PIPE_MAX_GAP_HEIGHT = get_env_var_as_int("PIPE_MAX_GAP_HEIGHT")
PIPE_DEFAULT_GAP_HEIGHT = 150
PIPE_DEFAULT_Y_POS = 150
MIN_TIME_BETWEEN_PIPES = get_env_var_as_int("MIN_TIME_BETWEEN_PIPES")
MAX_TIME_BETWEEN_PIPES = get_env_var_as_int("MAX_TIME_BETWEEN_PIPES")

# Bird SpriteSheet
BIRD_SPRITE_SHEET_PATH = get_env_var_as_string("BIRD_SPRITE_SHEET_PATH")
BIRD_SPRITE_SHEET_TOTAL_FRAMES = get_env_var_as_int("BIRD_SPRITE_SHEET_TOTAL_FRAMES")
BIRD_SPRITE_SHEET_FRAME_WIDTH = get_env_var_as_int("BIRD_SPRITE_SHEET_FRAME_WIDTH")
BIRD_SPRITE_SHEET_FRAME_HEIGHT = get_env_var_as_int("BIRD_SPRITE_SHEET_FRAME_HEIGHT")
BIRD_SPRITE_SHEET_START_Y = get_env_var_as_int("BIRD_SPRITE_SHEET_START_Y")
BIRD_SPRITE_SHEET_PADDING_X = get_env_var_as_int("BIRD_SPRITE_SHEET_PADDING_X")

# Bird Physics
BIRD_START_X_POS = get_env_var_as_int("BIRD_START_X_POS")
BIRD_START_Y_POS = get_env_var_as_int("BIRD_START_Y_POS")
BIRD_RADIUS = get_env_var_as_int("BIRD_RADIUS")
BIRD_COLOR = get_env_var_as_tuple("BIRD_COLOR")
BIRD_GRAVITY = get_env_var_as_float("BIRD_GRAVITY")
BIRD_FLAP_FORCE = get_env_var_as_int("BIRD_FLAP_FORCE")
BIRD_FLAP_DECAY_FORCE = get_env_var_as_float("BIRD_FLAP_DECAY_FORCE")
MAX_BIRD_VELOCITY = get_env_var_as_int("BIRD_MAX_Y_VELOCITY")
BIRD_ANIMATION_TIME = 0.05


AGENT_MAX_MEMORY = get_env_var_as_int("AGENT_MAX_MEMORY")
