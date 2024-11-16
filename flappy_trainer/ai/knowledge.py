from dataclasses import dataclass

from flappy_trainer.ai.ai_utils import Action
from flappy_trainer.ai.environment_state import EnvironmentState


@dataclass
class Knowledge:
    pre_state: EnvironmentState
    action: Action
    reward: float
    post_state: EnvironmentState

    def as_tuple(self) -> tuple:
        return tuple(self.pre_state, self.action, self.reward, self.post_state)
