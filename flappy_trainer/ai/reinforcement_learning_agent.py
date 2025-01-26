import random
from collections import deque

import numpy as np
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential

from flappy_trainer.ai.ai_utils import Action
from flappy_trainer.ai.environment_state import EnvironmentState
from flappy_trainer.ai.knowledge import Knowledge
from flappy_trainer.config import AGENT_MAX_MEMORY


class ReinforcementLearningAgent:
    """
    A reinforcement learning agent that uses a neural network to predict Q-values
    for state-action pairs and trains via experience replay.
    """

    def __init__(self):
        self.model: Sequential = self._create_model()
        self.memory: deque[Knowledge] = deque(maxlen=AGENT_MAX_MEMORY)
        self.exploration_rate = 1.0
        self.discount_factor = 0.8
        self.min_exploration_rate = 0.01
        self.exploration_decay = 0.997

    def reset(self):
        self.memory: deque[Knowledge] = deque(maxlen=AGENT_MAX_MEMORY)
        self.exploration_rate = 1.0
        self.discount_factor = 0.8
        self.min_exploration_rate = 0.01
        self.exploration_decay = 0.997

    def _create_model(self) -> Sequential:
        """Define and compile the neural network model."""
        model = Sequential(
            [
                Dense(64, input_dim=EnvironmentState.get_num_features(), activation="relu"),
                Dense(32, activation="relu"),
                Dense(2, activation="linear"),  # Output Q-values for both actions
            ]
        )
        model.compile(optimizer="adam", loss="mean_squared_error")
        return model

    def choose_action(self, state: EnvironmentState) -> Action:
        """Choose an action based on exploration vs exploitation."""
        if random.random() < self.exploration_rate:
            return random.choice([Action.FLAP, Action.NO_FLAP])

        state_array = state.to_numpy_array(include_batch_dim=True)
        q_values = self.model.predict(state_array, verbose=0)[0]
        return Action.FLAP if q_values[0] > q_values[1] else Action.NO_FLAP

    def remember(self, knowledge: Knowledge):
        """Store experience in memory with a fixed buffer size."""
        self.memory.append(knowledge)

    def replay(self, batch_size: int):
        """Train the model using a random batch of past experiences."""
        if len(self.memory) < batch_size:
            return
        batch = random.sample(self.memory, batch_size)
        states = []
        targets = []

        for knowledge in batch:
            pre_state_array = knowledge.pre_state.to_numpy_array(include_batch_dim=False)
            q_values = self.model.predict(pre_state_array.reshape(1, -1), verbose=0)[0]

            # Determine action index (0 for FLAP, 1 for NO_FLAP)
            action_index = 0 if knowledge.action == Action.FLAP else 1

            # Compute reward update
            if knowledge.post_state is not None and knowledge.post_state.bird_is_alive:
                next_state_array = knowledge.post_state.to_numpy_array(include_batch_dim=True)
                future_q_values = self.model.predict(next_state_array, verbose=0)[0]
                future_reward = max(future_q_values)  # Max Q-value for the next state
                q_values[action_index] = knowledge.reward + self.discount_factor * future_reward
            else:
                q_values[action_index] = knowledge.reward  # Terminal state

            states.append(pre_state_array)
            targets.append(q_values)

        # Train the model
        self.model.fit(np.array(states), np.array(targets), epochs=1, verbose=0)

        # Decay exploration rate
        self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)
