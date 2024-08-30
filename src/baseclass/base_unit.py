from abc import ABCMeta, abstractmethod
from os import PathLike
from enum import IntEnum
from base_tile import Position

class AnimationState(IntEnum):
    IDLE = 0
    MOVE = 1
    ATTACK = 2
    DEFEND = 3

class UnitMeta(ABCMeta):
    @property
    def anim_state(self) -> AnimationState:
        return self.anim_state

    @property
    def action_cost(self) -> int:
        return self.action_cost

    @property
    def position(self) -> Position:
        return self.position

    @property
    def supply(self) -> int:
        return self.supply
    

    @abstractmethod
    def _play_animation(self, anim_path: PathLike):
        pass

    def move(self, destination: Position) -> bool:
        # TODO: 이동 로직 구현
        pass
