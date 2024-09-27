import os
import threading
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from enum import IntEnum
from os import PathLike

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


@dataclass
class AnimationData:
    path: PathLike
    data: list[bytes]
    state: AnimationState


class BaseUnit(metaclass=ABCMeta):
    @property
    def anim_state(self) -> AnimationState:
        return self.__anim_state

    @anim_state.setter
    def anim_state(self, anim_state: AnimationState):
        self.__anim_state = anim_state

    @property
    def animations(self) -> list[dict[str, bytes | str] | None]:
        return self.__animations

    @animations.setter
    def animations(self, animations: list[dict[str, bytes | str] | None]):
        self.__animations = animations

    @property
    def action_cost(self) -> int:
        return self.__action_cost

    @action_cost.setter
    def action_cost(self, action_cost: int):
        self.__action_cost = action_cost

    @property
    def position(self) -> Position:
        return self.__position

    @position.setter
    def position(self, position: Position):
        self.__position = position

    @property
    def supply_reserve(self) -> int:
        return self.__supply_reserve

    @supply_reserve.setter
    def supply_reserve(self, supply_reserve: int):
        self.__supply_reserve = supply_reserve

    @property
    def cost(self) -> int:
        return self.__cost

    @cost.setter
    def cost(self, cost: int):
        self.__cost = cost

    @property
    def faction(self) -> int:
        return self.__faction

    @faction.setter
    def faction(self, faction: int):
        self.__faction = faction

    @property
    def hp(self) -> int:
        return self.__hp

    @hp.setter
    def hp(self, hp: int):
        self.__hp = hp

    @abstractmethod
    def __init__(self,
                 x: int,
                 y: int,
                 faction: int,
                 action_cost: int,
                 cost: int,
                 hp: int = 100,
                 supply_reserve: int = 100):
        self.anim_state = AnimationState.IDLE
        self.animations = [None, None, None, None]
        self.action_cost = action_cost
        self.position = Position(x, y)
        self.supply_reserve = supply_reserve
        self.cost = cost
        self.faction = faction
        self.hp = hp


    @abstractmethod
    def _play_animation(self, anim_path: PathLike):
        pass

    def __load_animation(self, parent_dir: PathLike, anim_type: str | AnimationState) -> None:
        """
        | **Animation Directory Hierarchy:**
        | animations/
        | ├── attack.webp
        | ├── defend.webp
        | ├── idle.webp
        | └── move.webp

        :param parent_dir: 애니메이션 파일이 있는 디렉토리
        :param anim_type: 로드할 애니메이션
        """

        # TODO: 테스트 필요
        anim_type = anim_type if isinstance(anim_type, str) else anim_type.name.lower()

        if anim_type.upper() not in AnimationState.__members__:
            raise ValueError(f"Invalid animation type: {anim_type}")

        with open(f"{parent_dir}/{anim_type}.webp", "rb") as f:
            self.animations[AnimationState[anim_type.upper()]] = {
                "path": f"{parent_dir}/{anim_type}.webp",
                "data": f.read()
            }

    def load_animations(self, animation_dir: PathLike):
        for animation_type in AnimationState:
            thread = threading.Thread(target=self.__load_animation, args=(animation_dir, animation_type.name.lower()))
            thread.start()

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
