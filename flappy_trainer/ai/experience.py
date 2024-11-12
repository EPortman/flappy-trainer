from dataclasses import dataclass

from flappy_trainer.ai.ai_utils import Action
from flappy_trainer.ai.game_state import GameState


@dataclass
class Experience:
    state: GameState
    action: Action
    reward: float
    next_state: GameState

    def as_tuple(self) -> tuple:
        return tuple(self.state, self.action, self.reward, self.next_state)
