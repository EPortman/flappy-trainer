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

from flappy_trainer.ai.ai_utils import Action, Knowledge, get_current_state, record_training_output
from flappy_trainer.ai.reinforcement_learning_agent import ReinforcementLearningAgent
from flappy_trainer.game_managers.game_manager import GameManager
from flappy_trainer.utils import GameState


class AITrainer:
    def __init__(self, model_path: str = None):
        self.agent = ReinforcementLearningAgent(model_path)
        self.action_tick = 15  # 4 actions per second (60 fps)
        self.replay_interval = 45  # Replay every 3 actions
        self.batch_size = 32  # Replay 32 memories at a time

    def train_gravity(self, csv_file_name: str):
        num_episodes = 2
        max_frames_per_episode = 1000
        explore_rate = 0.7
        explore_rate_decay = 0.9937
        min_explore_rate = 0.25
        self.agent.set_exploration_rate(explore_rate)
        game_manager = GameManager(is_pipes=False)

        print(f"Begin Gravity Training: {num_episodes} episodes total")
        for i in range(num_episodes):
            frames_survived = self._run_training_episode(game_manager, max_frames_per_episode)
            record_training_output(i + 1, explore_rate, frames_survived, csv_file_name)
            explore_rate = max(min_explore_rate, explore_rate * explore_rate_decay)
            self.agent.set_exploration_rate(explore_rate)

    def train_full_game(
        self,
        num_curricula: int,
        episodes_per_curricula: int,
        init_explore_rate: float,
        explore_rate_decay: float,
        min_explore_rate: float,
        csv_file_name: str,
    ):
        max_frames_per_episode = 3000
        explore_rate = init_explore_rate
        self.agent.set_exploration_rate(explore_rate)
        game_manager = GameManager(is_pipes=True)

        print(f"Begin Full Game Training: {num_curricula} curricula at {episodes_per_curricula} episodes each.")
        for curricula in range(num_curricula):
            print(f"Being Curricula {curricula + 1} of full game training. Reset Exploration Rate")
            for i in range(episodes_per_curricula):
                frames_survived = self._run_training_episode(game_manager, max_frames_per_episode)
                record_training_output(i + 1, explore_rate, frames_survived, csv_file_name, curricula)
                explore_rate = max(min_explore_rate, explore_rate * explore_rate_decay)
                self.agent.set_exploration_rate(explore_rate)

    def _create_knowledge(self, pre_state, action, current_state, game_manager) -> Knowledge | None:
        # Reward is based on if the action from the pre_state caused death in the current_state
        if game_manager.state == GameState.GAME_OVER or current_state is None:
            reward = -1
        else:
            reward = 1
        return Knowledge(pre_state, action, reward, current_state)

    def _run_training_episode(self, game_manager: GameManager, max_frames: int) -> int:
        game_manager.start_game()
        current_frame = 0
        pending_knowledge = []
        while game_manager.state is GameState.RUNNING and current_frame < max_frames:
            # Update the game (60 fps)
            game_manager.update(1 / 60)
            current_frame += 1

            # Assess game on the first frame and every action tick
            if current_frame == 1 or current_frame % self.action_tick == 0:
                # Agent makes an action and action is stored to create knowledge for later
                current_state = get_current_state(game_manager)
                action = self.agent.choose_action(current_state)
                if action == Action.FLAP:
                    game_manager.bird.flap()
                pending_knowledge.append((current_state, action, current_frame))

                # If an action tick has occured since an action, create and store knowledge
                for action_made in pending_knowledge[:]:
                    pre_state, action, action_frame = action_made
                    if current_frame - action_frame >= self.action_tick:
                        post_state = get_current_state(game_manager)
                        knowledge = self._create_knowledge(pre_state, action, post_state, game_manager)
                        self.agent.remember(knowledge)
                        pending_knowledge.remove(action_made)

                # Train the agent on the memories at set intervals
                if current_frame % self.replay_interval == 0:
                    self.agent.replay(self.batch_size)

                if current_frame < max_frames:
                    # Always remember the move that caused death
                    if pending_knowledge is not None:
                        pre_state, action, action_frame = pending_knowledge[-1]
                        knowledge = self._create_knowledge(pre_state, action, None, game_manager)
                        self.agent.remember(knowledge)
        return current_frame
