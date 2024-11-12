from tensorflow.keras.models import Sequential

from flappy_trainer.ai.game_state import GameState
from flappy_trainer.ai.reinforcement_learning_agent import ReinforcementLearningAgent
from flappy_trainer.game_managers.game_manager import GameManager


class AITrainer:
    def __init__(self):
        self.game_manager = GameManager()
        self.agent = ReinforcementLearningAgent()
        self.initial_state = GameState
        self.episodes = 100
        self.batch_size = 32

    def get_model(self) -> Sequential:
        for episode in range(self.episodes):
            current_state = GameState.get_initial_game_state()
