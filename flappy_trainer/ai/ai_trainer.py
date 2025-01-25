import time

from tensorflow.keras.models import Sequential

from flappy_trainer.ai.ai_utils import Action, get_alignment_reward, get_curr_pipe_velocity, get_nearest_pipe_details
from flappy_trainer.ai.environment_state import EnvironmentState
from flappy_trainer.ai.knowledge import Knowledge
from flappy_trainer.ai.reinforcement_learning_agent import ReinforcementLearningAgent
from flappy_trainer.game_managers.game_manager import GameManager
from flappy_trainer.utils import GameState
from flappy_trainer.config import SCREEN_HEIGHT


class AITrainer:
    """
    Trainer for the Flappy Bird AI. Handles running episodes, managing game states,
    and training the reinforcement learning agent.
    """

    def __init__(self):
        self.game_manager = GameManager()
        self.agent = ReinforcementLearningAgent()
        self.episodes = 10000
        self.batch_size = 32
        self.decision_interval = 20
        self.replay_interval = self.decision_interval * 3
        self.frame_count = 0

    def train(self, debug=True) -> Sequential:
        """
        Train the agent by running episodes of the game.

        Args:
            debug (bool): If True, includes a delay for real-time visualization.
            decision_interval (int): Number of frames to skip between decisions.
        Returns:
            Sequential: The trained model.
        """
        for episode in range(self.episodes):
            self.game_manager.start_game()
            total_reward = 0

            while self.game_manager.state is GameState.RUNNING:
                # Update the game (60 fps)
                self.game_manager.update(1 / 60)
                self.game_manager.draw_canvas()
                self.frame_count += 1
                total_reward += 1

                # Choose action and calculate reward from action
                if self.frame_count % self.decision_interval == 0:
                    current_state = self._get_current_state()
                    action = self.agent.choose_action(current_state)
                    self._apply_action(action)
                    reward, knowledge = self._calculate_reward(current_state, action)
                    if knowledge:
                        self.agent.remember(knowledge)
                    total_reward += reward

                if debug:
                    time.sleep(1 / 60)

                # Replay synchronously at intervals
                if self.frame_count % self.replay_interval == 0:
                    self.agent.replay(self.batch_size)

            print(f"Episode {episode + 1} / {self.episodes}, Total Reward: {total_reward}")
            print(
                f"Q-values: {self.agent.model.predict(current_state.to_numpy_array(include_batch_dim=True), verbose=0)}"
            )
        return self.agent.model

    def _calculate_reward(self, current_state, action) -> tuple[float, Knowledge] | tuple[float, None]:
        reward = -10 if self.game_manager.state == GameState.GAME_OVER else 0
        if self.game_manager.state == GameState.RUNNING and current_state.next_pipe_gap_pos is not None:
            pipe_center = current_state.next_pipe_gap_pos
            distance_to_center = abs(current_state.bird_vert_pos - pipe_center)
            max_distance = SCREEN_HEIGHT  # Normalize by screen height
            alignment_reward = 1 - (distance_to_center / max_distance)  # Reward inversely proportional to distance
            reward += alignment_reward * 10  # Scale the reward for impact
            knowledge = self._create_knowledge(current_state, action, reward)
            return (reward, knowledge)
        return (reward, None)

    def _apply_action(self, action: Action):
        if action == Action.FLAP:
            self.game_manager.bird.flap()

        delta_time = 1 / 60
        self.game_manager.update(delta_time)

    def _get_current_state(self) -> EnvironmentState:
        bird_is_alive = self.game_manager.state == GameState.RUNNING
        bird_vert_pos = self.game_manager.bird.y_pos
        bird_vert_velocity = self.game_manager.bird.y_velocity
        pipe_velocity = get_curr_pipe_velocity(self.game_manager)
        distance_to_next_pipe, next_pipe_gap_pos, next_pipe_gap_height = get_nearest_pipe_details(self.game_manager)

        return EnvironmentState(
            bird_is_alive=bird_is_alive,
            bird_vert_pos=bird_vert_pos,
            bird_vert_velocity=bird_vert_velocity,
            pipe_velocity=pipe_velocity,
            next_pipe_distance=distance_to_next_pipe,
            next_pipe_gap_pos=next_pipe_gap_pos,
            next_pipe_gap_height=next_pipe_gap_height,
        )

    def _create_knowledge(self, prev_state: EnvironmentState, action: Action, reward: float) -> Knowledge:
        post_state = self._get_current_state()
        knowledge = Knowledge(prev_state, action, reward, post_state)
        return knowledge
