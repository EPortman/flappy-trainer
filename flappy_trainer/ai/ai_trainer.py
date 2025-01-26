import time

from tensorflow.keras.models import Sequential

from flappy_trainer.ai.ai_utils import (
    Action,
    get_alignment_reward,
    get_curr_pipe_velocity,
    get_nearest_pipe_details,
    update_game,
    print_debug_output
)
from flappy_trainer.ai.environment_state import EnvironmentState
from flappy_trainer.ai.knowledge import Knowledge
from flappy_trainer.ai.reinforcement_learning_agent import ReinforcementLearningAgent
from flappy_trainer.config import SCREEN_HEIGHT
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
        self.action_tick = 20
        self.replay_interval = self.action_tick * 3

    def train(self, debug=True) -> Sequential:
        for episode in range(self.episodes):
            self.game_manager.start_game()
            current_frame = 0
            pending_knowledge = []

            while self.game_manager.state is GameState.RUNNING and current_frame < 1200:
                # Update the game (60 fps)
                update_game(self.game_manager, frames=1, debug=True)
                current_frame += 1

                # Assess game every 20 frames
                if current_frame % self.action_tick == 0:
                    # Agent makes an action and it is stored for later
                    current_state = self._get_current_state()
                    action = self.agent.choose_action(current_state)
                    self._apply_action(action)
                    pending_knowledge.append((current_state, action, current_frame))

                    # If 20 frames have passed since the action, create and store knowledge
                    for action_made in pending_knowledge[:]:
                        pre_state, action, action_frame = action_made
                        if current_frame - action_frame >= self.action_tick:
                            post_state = self._get_current_state()
                            knowledge = self._create_knowledge(pre_state, action, post_state)
                            self.agent.remember(knowledge)
                            pending_knowledge.remove(action_made)

                # Train the agent on the memories every second
                if current_frame % self.replay_interval == 0:
                    self.agent.replay(self.batch_size)

            # Always remember the move that caused death
            if current_frame < 1200 and pending_knowledge is not None:
                pre_state, action, action_frame = pending_knowledge[-1]
                knowledge = self._create_knowledge(pre_state, action, None)
                self.agent.remember(knowledge)

            print_debug_output(debug, episode, self.episodes, self.agent.exploration_rate, current_frame)

        return self.agent.model

    def _create_knowledge(self, pre_state, action, current_state) -> Knowledge | None:
        # Penalize game over heavily
        if self.game_manager.state == GameState.GAME_OVER:
            return Knowledge(pre_state, action, -100, None)

        # Reward if bird is closer to the target
        pre_distance_to_target = abs(
            pre_state.bird_vert_pos / SCREEN_HEIGHT - pre_state.next_pipe_gap_pos / SCREEN_HEIGHT
        )
        post_distance_to_target = abs(
            current_state.bird_vert_pos / SCREEN_HEIGHT - current_state.next_pipe_gap_pos / SCREEN_HEIGHT
        )
        delta_distance = pre_distance_to_target - post_distance_to_target
        reward = delta_distance * 100

        return Knowledge(pre_state, action, reward, current_state)

    def _apply_action(self, action: Action):
        if action == Action.FLAP:
            self.game_manager.bird.flap()

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
