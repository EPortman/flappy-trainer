"""
AITrainer

This class manages the training process for the Flappy Bird AI, coordinating the interaction between
the reinforcement learning agent and the game environment. Training is structured into curricula,
progressing from simple to complex scenarios to build the agent's skills over time.

Key Features:
- Oversees the GameManager and Reinforcement Learning Agent interactions
- Structures training into progressively harder curricula
- Simulates gameplay by applying the agent's actions to the game
- Generates training data (knowledge) based on game events
"""

import os

import yaml
from tensorflow.keras.models import Sequential

from flappy_trainer.ai.ai_utils import (
    Action,
    Knowledge,
    get_curr_pipe_velocity,
    get_nearest_pipe_details,
    get_second_nearest_pipe_details,
    print_debug_output,
)
from flappy_trainer.ai.environment_state import EnvironmentState
from flappy_trainer.ai.reinforcement_learning_agent import ReinforcementLearningAgent
from flappy_trainer.game_managers.game_manager import GameManager
from flappy_trainer.utils import GameState

TRAINING_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "training_curricula.yaml")


class AITrainer:
    def __init__(self):
        self.agent = ReinforcementLearningAgent()
        self.batch_size = 32

    def train(self) -> Sequential:
        # Load the curriculum file
        with open(TRAINING_FILE_PATH, "r") as training_file:
            curricula = yaml.safe_load(training_file)

        # Iterate through each curriculum and train
        for curriculum in curricula:
            print(f"\n{curriculum['name']}")
            self._train_curriculum(
                num_episodes=curriculum["num_episodes"],
                action_tick=curriculum["action_tick"],
                target_frames=curriculum["target_frames"],
                is_pipes_active=curriculum["is_pipes_active"],
                pipe_gap_size_mode=curriculum.get("pipe_gap_size_mode"),
                pipe_distance_mode=curriculum.get("pipe_distance_mode"),
                is_pipe_gaps_alternating=curriculum.get("is_pipe_gaps_alternating"),
            )
            self.agent.reset()

        return self.agent.model

    def _train_curriculum(
        self,
        num_episodes: int,
        action_tick: int,
        target_frames: int,
        is_pipes_active: bool = True,
        pipe_gap_size_mode: str = "random",
        pipe_distance_mode: str = "random",
        is_pipe_gaps_centered: bool = False,
        is_pipe_gaps_alternating: bool = False,
    ):
        self.game_manager = GameManager(
            is_pipes_active, pipe_gap_size_mode, pipe_distance_mode, is_pipe_gaps_centered, is_pipe_gaps_alternating
        )
        replay_interval = action_tick * 3
        num_correct_in_a_row = 0

        for episode in range(num_episodes):
            self.game_manager.start_game()
            current_frame = 0
            pending_knowledge = []

            while self.game_manager.state is GameState.RUNNING and current_frame < target_frames:
                # Update the game (60 fps)
                self.game_manager.update(1 / 60)
                current_frame += 1

                # Assess game on the first frame and every action tick
                if current_frame == 1 or current_frame % action_tick == 0:
                    # Agent makes an action and action is stored to create knowledge for later
                    current_state = self._get_current_state()
                    action = self.agent.choose_action(current_state)
                    if action == Action.FLAP:
                        self.game_manager.bird.flap()
                    pending_knowledge.append((current_state, action, current_frame))

                    # If an action tick has occured since an action, create and store knowledge
                    for action_made in pending_knowledge[:]:
                        pre_state, action, action_frame = action_made
                        if current_frame - action_frame >= action_tick:
                            post_state = self._get_current_state()
                            knowledge = self._create_knowledge(pre_state, action, post_state)
                            self.agent.remember(knowledge)
                            pending_knowledge.remove(action_made)

                # Train the agent on the memories at set intervals
                if current_frame % replay_interval == 0:
                    self.agent.replay(self.batch_size)

            if current_frame < target_frames:
                # Always remember the move that caused death
                if pending_knowledge is not None:
                    pre_state, action, action_frame = pending_knowledge[-1]
                    knowledge = self._create_knowledge(pre_state, action, None)
                    self.agent.remember(knowledge)
                num_correct_in_a_row = 0
            else:
                num_correct_in_a_row += 1

            print_debug_output(
                episode, num_episodes, self.agent.exploration_rate, current_frame, action_tick, target_frames
            )
            if num_correct_in_a_row >= 10:
                print(f"\tTraining stopped after {episode + 1} episodes. 10 successful episodes in a row!")
                break

    def _create_knowledge(self, pre_state, action, current_state) -> Knowledge | None:
        # Reward is based on if the action from the pre_state caused death in the current_state
        if self.game_manager.state == GameState.GAME_OVER or current_state is None:
            reward = -1
        else:
            reward = 1
        return Knowledge(pre_state, action, reward, current_state)

    def _get_current_state(self) -> EnvironmentState:
        bird_is_alive = self.game_manager.state == GameState.RUNNING
        bird_vert_pos = self.game_manager.bird.y_pos
        bird_vert_velocity = self.game_manager.bird.y_velocity
        pipe_velocity = get_curr_pipe_velocity(self.game_manager)
        distance_to_next_pipe, next_pipe_gap_pos, next_pipe_gap_height = get_nearest_pipe_details(self.game_manager)
        distance_to_second_pipe, second_pipe_gap_pos, second_pipe_gap_height = get_second_nearest_pipe_details(
            self.game_manager
        )

        return EnvironmentState(
            bird_is_alive=bird_is_alive,
            bird_vert_pos=bird_vert_pos,
            bird_vert_velocity=bird_vert_velocity,
            pipe_velocity=pipe_velocity,
            next_pipe_distance=distance_to_next_pipe,
            next_pipe_gap_pos=next_pipe_gap_pos,
            next_pipe_gap_height=next_pipe_gap_height,
            second_pipe_distance=distance_to_second_pipe,
            second_pipe_gap_pos=second_pipe_gap_pos,
            second_pipe_gap_height=second_pipe_gap_height,
        )
