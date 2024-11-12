from dataclasses import dataclass

from flappy_trainer.ai.ai_utils import Action
from flappy_trainer.ai.environment_state import EnvironmentState


@dataclass
class Knowledge:
    state: EnvironmentState
    action: Action
    reward: float
    next_state: EnvironmentState

    def as_tuple(self) -> tuple:
        return tuple(self.state, self.action, self.reward, self.next_state)
