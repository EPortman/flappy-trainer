from tensorflow.keras.models import Sequential

from flappy_trainer.ai.environment_state import EnvironmentState
from flappy_trainer.ai.reinforcement_learning_agent import ReinforcementLearningAgent
from flappy_trainer.game_managers.game_manager import GameManager


class AITrainer:
    def __init__(self):
        self.game_manager = GameManager()
        self.agent = ReinforcementLearningAgent()
        self.initial_state = EnvironmentState
        self.episodes = 100
        self.batch_size = 32

    def get_model(self) -> Sequential:
        for episode in range(self.episodes):
            self.game_manager.start_game()
            current_state = EnvironmentState.get_initial_game_state()
            action = self.agent.choose_action(current_state)
            reward, next_state, is_game_over = self.game_manager.ai_apply_action(action)
