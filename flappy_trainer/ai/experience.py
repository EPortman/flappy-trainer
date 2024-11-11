from dataclasses import dataclass

from ai.game_state import GameState
from ai.utils import Action


@dataclass
class Experience:
    state: GameState
    action: Action
    reward: float
    next_state: GameState

    def as_tuple(self) -> tuple:
        return tuple(self.state, self.action, self.reward, self.next_state)
