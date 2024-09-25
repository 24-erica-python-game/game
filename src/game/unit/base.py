from abc import ABCMeta, abstractmethod
from os import PathLike
from enum import IntEnum
from dataclasses import dataclass

from game.tile.types import Position

class AnimationState(IntEnum):
    """
    IDLE
        기본 상태 (아무런 행동도 없을 경우)

    MOVE
        이동 시 애니메이션

    ATTACK
        공격 시 애니메이션

    DEFEND
        방어 시 애니메이션
    """
    IDLE = 0
    MOVE = 1
    ATTACK = 2
    DEFEND = 3
    

class BaseUnit(ABCMeta):
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
    def supply_reserve(self) -> int:
        return self.supply_reserve

    @property
    def cost(self) -> int:
        return self.cost

    @property
    def faction(self) -> int:
        return self.faction

    @property
    def hp(self) -> int:
        return self.hp
    
    def __init__(self, x: int, y: int, faction: int, hp: int=100) -> None:
        self.position = Position(x, y)
        self.faction = faction
        self.hp = hp


    @abstractmethod
    def _play_animation(self, anim_path: PathLike):
        pass

    def move(self, path: list[Position]) -> bool:
        """
        `BaseTile.get_path()`의 반환 값 토대로 유닛 이동. \n
        올바른 이동일 경우 `True` 반환
        """
        # TODO: 이동 로직 구현
        try:
            
            # return self.movement_cost >= sum(path.cost)
            return True
        except IndexError:
            return False


class BaseSupplyUnit(BaseUnit):
    def __init__(self, position: Position):
        pass

    def supply(self, target_unit: BaseUnit):
        target_unit.supply_reserve += 100
