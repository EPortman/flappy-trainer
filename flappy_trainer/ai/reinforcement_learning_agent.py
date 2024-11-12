import random

from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential

from flappy_trainer.ai.ai_utils import Action
from flappy_trainer.ai.experience import Experience
from flappy_trainer.ai.game_state import GameState


class ReinforcementLearningAgent:
    NUM_INPUTS = 6

    def __init__(self):
        self.model: Sequential = None
        self.memory: list[Experience] = []
        self.exploration_rate = 1.0

    def create_model(self):
        self.model = Sequential(
            [
                Dense(24, input_dim=self.NUM_INPUTS, activation="relu"),
                Dense(24, activation="relu"),
                Dense(1, activation="sigmoid"),
            ]
        )
        self.model.compile(optimizer="adam", loss="binary_crossentropy")

    def choose_action(self, state: GameState) -> Action:
        if random.random() < self.exploration_rate:
            action = random.choice([Action.FLAP, Action.NO_FLAP])
        else:
            flap_probability = self.model.predict(state.to_numpy_array())[0][0]
            action = Action.FLAP if flap_probability > 0.5 else Action.NO_FLAP
        return action
