import os
import random
import time

import pygame

from flappy_trainer.ai.ai_trainer import AITrainer  # noqa: F401
from flappy_trainer.ai.ai_utils import Action, get_current_state
from flappy_trainer.ai.reinforcement_learning_agent import ReinforcementLearningAgent
from flappy_trainer.game_managers.game_manager import GameManager
from flappy_trainer.utils import GameState

"""############################### OBSERVE AN EXISTING MODEL ################################"""
MODELS_DIR = "flappy_trainer/ai/models"
NAME_OF_MODEL = "flappy_trainer_model.keras"
MODEL_PATH = os.path.join(MODELS_DIR, NAME_OF_MODEL)
random.seed(42)
pygame.init()
agent = ReinforcementLearningAgent(MODEL_PATH)
agent.set_exploration_rate(0.0)
game_manager = GameManager(True, "random", "random", "random")

while True:
    game_manager.start_game()
    current_frame = 0
    start_time = time.time()

    while game_manager.state is GameState.RUNNING:
        frame_start = time.time()
        game_manager.draw()
        game_manager.update(1 / 60)
        current_frame += 1

        if current_frame == 1 or current_frame % 15 == 0:
            current_state = get_current_state(game_manager)
            action = agent.choose_action(current_state)
            if action == Action.FLAP:
                game_manager.bird.flap()

        # Maintain 60 FPS
        elapsed = time.time() - frame_start
        time.sleep(max(0, (1 / 60) - elapsed))


"""################################ TRAIN AN EXISTING MODEL #################################"""
# MODELS_DIR = "flappy_trainer/ai/models"
# NAME_OF_MODEL = "existing_model.keras"
# MODEL_PATH = os.path.join(MODELS_DIR, NAME_OF_MODEL)
# OUTPUT_FILE = "full-game-training-output"
# random.seed(42)
# pygame.init()

# trainer = AITrainer(MODEL_PATH)
# trainer.train_full_game(
#     num_curricula=3,
#     episodes_per_curricula=600,
#     init_explore_rate=0.5,
#     explore_rate_decay=0.996,
#     min_explore_rate=0.15,
#     csv_file_name=OUTPUT_FILE
# )
# model = trainer.agent.model

# model.save(MODEL_PATH)
# print(f"Model saved to {MODEL_PATH}")
# pygame.quit()


"""########################## TRAIN A NEW MODEL GRAVITY FROM SCRATCH ##########################"""
# MODELS_DIR = "flappy_trainer/ai/models"
# NAME_OF_MODEL = "my_new_model.keras"
# MODEL_PATH = os.path.join(MODELS_DIR, NAME_OF_MODEL)
# OUTPUT_FILE = "gravity-training-output"
# random.seed(42)
# pygame.init()

# trainer = AITrainer()
# trainer.train_gravity(OUTPUT_FILE)
# model = trainer.agent.model

# model.save(MODEL_PATH)
# print(f"Model saved to {MODEL_PATH}")
# pygame.quit()


"""###################### TRAIN A NEW MODEL ON EVERYTHING FROM SCRATCH ######################"""
# MODELS_DIR = "flappy_trainer/ai/models"
# NAME_OF_MODEL = "my_new_model.keras"
# MODEL_PATH = os.path.join(MODELS_DIR, NAME_OF_MODEL)
# OUTPUT_FILE_GRAVITY = "gravity-training-output"
# OUTPUT_FILE_FULL = "full-training-output"
# random.seed(42)
# pygame.init()

# trainer = AITrainer()
# trainer.train_gravity(OUTPUT_FILE_GRAVITY)
# trainer.train_full_game(
#     num_curricula=3,
#     episodes_per_curricula=1,
#     init_explore_rate=0.5,
#     explore_rate_decay=0.996,
#     min_explore_rate=0.15,
#     csv_file_name=OUTPUT_FILE_FULL
# )
# model = trainer.agent.model

# model.save(MODEL_PATH)
# print(f"Model saved to {MODEL_PATH}")
# pygame.quit()
