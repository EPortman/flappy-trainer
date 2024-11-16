import time

from tensorflow.keras.models import Sequential

from flappy_trainer.ai.ai_utils import (
    Action,
    get_curr_pipe_velocity,
    get_distance_to_next_pipe,
    get_nearest_pipe_heights,
)
from flappy_trainer.ai.environment_state import EnvironmentState
from flappy_trainer.ai.knowledge import Knowledge
from flappy_trainer.ai.reinforcement_learning_agent import ReinforcementLearningAgent
from flappy_trainer.game_managers.game_manager import GameManager
from flappy_trainer.utils import GameState


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
        self.replay_interval = 10  # Replay every 10 frames
        self.frame_count = 0  # Count frames since last replay

    def train(self, debug=True, decision_interval=10) -> Sequential:
        """
        Train the agent by running episodes of the game.

        Args:
            debug (bool): If True, includes a delay for real-time visualization.
            decision_interval (int): Number of frames to skip between decisions.
        Returns:
            Sequential: The trained model.
        """
        self.agent.create_model()
        for episode in range(self.episodes):
            self.game_manager.start_game()
            total_reward = 0

            while self.game_manager.state is GameState.RUNNING:
                self.frame_count += 1
                action = Action.NO_FLAP
                # Update game state and draw the frame
                current_state = self._get_current_state()

                # Make a decision only at specified intervals
                if self.frame_count % decision_interval == 0:
                    action = self.agent.choose_action(current_state)
                    self._apply_action(action)

                # Update the game state regardless of decision interval
                self.game_manager.update(1 / 60)
                self.game_manager.draw()

                if debug:
                    time.sleep(1 / 60)

                # Calculate reward and store knowledge
                reward = -100 if self.game_manager.state == GameState.GAME_OVER else 1
                knowledge = self._create_knowledge(current_state, action, reward)
                self.agent.remember(knowledge)
                total_reward += reward

                # Replay synchronously at intervals
                if (
                    self.frame_count % self.replay_interval == 0
                    and len(self.agent.memory) >= self.batch_size
                ):
                    self.agent.replay(self.batch_size)

            print(f"Episode {episode + 1} / {self.episodes}, Total Reward: {total_reward}")
            print(
                f"Q-values: {self.agent.model.predict(
                    current_state.to_numpy_array(include_batch_dim=True), verbose=0
                )}"
            )

        return self.agent.model

    def _apply_action(self, action: Action):
        if action == Action.FLAP:
            self.game_manager.bird.flap()

        delta_time = 1 / 60
        self.game_manager.update(delta_time)

    def _get_current_state(self) -> EnvironmentState:
        distance_to_next_pipe = get_distance_to_next_pipe(self.game_manager)
        nearest_pipe_heights = get_nearest_pipe_heights(self.game_manager)
        if nearest_pipe_heights:
            next_pipe_top_height, next_pipe_bot_height = nearest_pipe_heights
        else:
            next_pipe_top_height, next_pipe_bot_height = None, None

        return EnvironmentState(
            bird_is_alive=self.game_manager.state == GameState.RUNNING,
            bird_vert_pos=self.game_manager.bird.y_pos,
            bird_vert_velocity=self.game_manager.bird.y_velocity,
            pipe_velocity=get_curr_pipe_velocity(self.game_manager),
            distance_to_next_pipe=distance_to_next_pipe,
            next_pipe_top_height=next_pipe_top_height,
            next_pipe_bot_height=next_pipe_bot_height,
        )

    def _create_knowledge(
        self, prev_state: EnvironmentState, action: Action, reward: float
    ) -> Knowledge:
        post_state = self._get_current_state()
        knowledge = Knowledge(prev_state, action, reward, post_state)
        return knowledge
