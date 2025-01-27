import os
import random
import pygame

from flappy_trainer.ai.ai_trainer import AITrainer

MODELS_DIR = "flappy_trainer/ai/models"
MODEL_PATH = os.path.join(MODELS_DIR, "flappy_trainer_model.keras")
random.seed(42)

pygame.init()
trainer = AITrainer()
model = trainer.train()
model.save(MODEL_PATH)
print(f"Model saved to {MODEL_PATH}")
pygame.quit()
