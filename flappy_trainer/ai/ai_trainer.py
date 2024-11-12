from tensorflow.keras.models import Sequential

from flappy_trainer.ai.ai_utils import Action
from flappy_trainer.ai.environment_state import EnvironmentState
from flappy_trainer.ai.knowledge import Knowledge
from flappy_trainer.ai.reinforcement_learning_agent import ReinforcementLearningAgent
from flappy_trainer.game_managers.game_manager import GameManager
from flappy_trainer.utils import GameState


class AITrainer:
    def __init__(self):
        self.game_manager = GameManager()
        self.agent = ReinforcementLearningAgent()
        self.episodes = 100
        self.batch_size = 32

    def train(self) -> Sequential:
        for episode in range(self.episodes):
            total_reward = 0
            self.game_manager.start_game()

            while self.game_manager.state is GameState.RUNNING:
                current_state = self._get_current_state()
                action = self.agent.choose_action(current_state)
                self._apply_action(action)
                reward = -1 if self.game_manager.state == GameState.GAME_OVER else 1

                knowledge = self._create_knowledge(current_state, action, reward)
                self.agent.remember(knowledge)
                total_reward += reward

                if len(self.agent.memory) >= self.batch_size:
                    self.agent.replay(self.batch_size)
                if self.game_manager.state == GameState.GAME_OVER:
                    break
        print(f"Episode {episode+1}/{self.episodes}, Total Reward: {total_reward}")

    def _apply_action(self, action: Action):
        if action == Action.FLAP:
            self.game_manager.bird.flap()

        delta_time = 1 / 60
        self.game_manager.update(delta_time)

    def _get_current_state(self) -> EnvironmentState:
        distance_to_next_pipe = self._get_distance_to_next_pipe()
        nearest_pipe_heights = self._get_nearest_pipe_heights()
        if nearest_pipe_heights:
            next_pipe_top_height, next_pipe_bot_height = nearest_pipe_heights
        else:
            next_pipe_top_height, next_pipe_bot_height = None, None

        return EnvironmentState(
            bird_vert_pos=self.game_manager.bird.y_pos,
            bird_vert_velocity=self.game_manager.bird.y_velocity,
            distance_to_next_pipe=distance_to_next_pipe,
            next_pipe_top_height=next_pipe_top_height,
            next_pipe_bot_height=next_pipe_bot_height,
            pipe_velocity=self._get_curr_pipe_velocity(),
        )

    def _create_knowledge(
        self, prev_state: EnvironmentState, action: Action, reward: float
    ) -> Knowledge:
        post_state = self._get_current_state()
        knowledge = Knowledge(prev_state, action, reward, post_state)
        return knowledge
