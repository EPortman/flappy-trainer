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
        self.model: Sequential = None
        self.memory: deque[Knowledge] = deque(maxlen=AGENT_MAX_MEMORY)
        self.exploration_rate = 1.0
        self.discount_factor = 0.9
        self.min_exploration_rate = 0.1
        self.exploration_decay = 0.995

    def create_model(self):
        """Define and compile the neural network model."""
        self.model = Sequential(
            [
                Dense(24, input_dim=EnvironmentState.get_num_features(), activation="relu"),
                Dense(24, activation="relu"),
                Dense(1, activation="sigmoid"),
            ]
        )
        self.model.compile(optimizer="adam", loss="binary_crossentropy")

    def choose_action(self, state: EnvironmentState) -> Action:
        """Choose an action based on exploration vs exploitation."""
        if random.random() < self.exploration_rate:
            return random.choice([Action.FLAP, Action.NO_FLAP])

        state_array = state.to_numpy_array(include_batch_dim=True)
        flap_probability = self.model.predict(state_array, verbose=0)[0][0]
        return Action.FLAP if flap_probability > 0.5 else Action.NO_FLAP

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
            reward_from_action = knowledge.reward
            if knowledge.post_state is not None and knowledge.post_state.bird_is_alive:
                next_state_array = knowledge.post_state.to_numpy_array(include_batch_dim=True)
                future_reward = self.model.predict(next_state_array, verbose=0)[0][0]
                reward_from_action += self.discount_factor * future_reward
            states.append(knowledge.pre_state.to_numpy_array())
            targets.append([reward_from_action])
        # Train the model
        self.model.fit(np.array(states), np.array(targets), epochs=1, verbose=0)
        # Decay exploration rate
        self.exploration_rate = max(
            self.min_exploration_rate, self.exploration_rate * self.exploration_decay
        )
