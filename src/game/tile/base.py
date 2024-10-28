from abc import ABCMeta, abstractmethod
from typing import Any

from src.game.tile.types import *
from src.game.unit.base import BaseUnit


class BaseTile(metaclass=ABCMeta):
    """
    https://www.redblobgames.com/grids/hexagons/ \n
    기본: `Axial Coordinates` 사용 \n
    필요 시 `Cube Coordinates` 사용
    """

    @property
    def placed_unit(self) -> Optional[BaseUnit]:
        return self._placed_unit

    @property
    def placed_structure(self) -> Optional['BaseStructure']:
        return self._placed_structure

    def __init__(self, q: int, r: int,
                 defence_bonus: int = 0,
                 movement_cost: int = 1) -> None:
        self.position = Position(q, r)
        self.defence_bonus = defence_bonus
        self.movement_cost = movement_cost
        self._placed_unit = None
        self._placed_structure = None

    @placed_unit.setter
    def placed_unit(self, unit: BaseUnit) -> None:
        self._placed_unit = unit

    @placed_structure.setter
    def placed_structure(self, structure: 'BaseStructure') -> None:
        self._placed_structure = structure

    def on_unit_arrived(self) -> Any:
        """
        유닛이 도착했을 때 유닛은 현재 타일의 이 메서드를 호출해야 함.

        구조물이 있는 경우 구조물의 `on_unit_arrived()` 메서드를 호출하게 됨, \n
        따라서 상속된 타일 클래스에서 구조물의 `on_unit_arrived()` 메서드를 호출하는 대신 `super().on_unit_arrived()` 구문을 추가하면 됨.

        :return: 상속된 타일 클래스에서 구현한 메서드의 반환값
        """
        if self._placed_structure is not None:
            return self._placed_structure.on_unit_arrived(self)

    def place_unit(self, unit: BaseUnit) -> None:
        """
        타일에 유닛을 배치함
        :param unit:
        :return:
        """
        self._placed_unit = unit

    def place_structure(self, structure: 'BaseStructure') -> None:
        """
        타일에 구조물을 배치함
        :param structure:
        :return:
        """
        self._placed_structure = structure

    def get_neighbors(self) -> list[Self]:
        """
        현재 타일의 이웃 타일 리스트 반환
        :return: 유효한 이웃 타일 리스트
        """
        # 이 import 문을 최상단으로 이동하면 순환참조 오류가 발생해 이곳으로 이동함.
        from src.game.rule import GameSystem

        map_data = GameSystem().map_data
        def is_valid_position(p: Position) -> bool:
            q_size, r_size = GameSystem().ruleset.map_size
            return 0 <= p.q < q_size and 0 <= p.r < r_size

        return [
            map_data[self.position.q + v.value.q][self.position.r + v.value.r] \
            for v in HexDirectionVectors
            if is_valid_position(
                map_data[self.position.q + v.value.q][self.position.r + v.value.r].position
            )
        ]


class BaseStructure(metaclass=ABCMeta):
    def __init__(self, faction: int, parent_tile: BaseTile) -> None:
        self.faction = faction
        self.parent_tile = parent_tile

    @abstractmethod
    def on_unit_arrived(self) -> Any:
        """
        유닛이 도착했을 때 호출되어야 하는 메서드

        :return: 상속된 구조물 클래스에서 구현한 메서드의 반환값
        """
        pass
