from abc import ABCMeta, abstractmethod
from typing import Any, Optional, TYPE_CHECKING

from game.rule import GameSystem
from src.game.unit.base import BaseUnit
from src.game.tile.types import *

if TYPE_CHECKING:
    from src.game.tile.base import BaseTile


class BaseStructure(metaclass=ABCMeta):
    def __init__(self, faction: int) -> None:
        self.faction = faction

    @abstractmethod
    def on_arrived(self, base_tile: BaseTile) -> None:
        pass


class BaseTile(metaclass=ABCMeta):
    """
    https://www.redblobgames.com/grids/hexagons/
    기본: `Axial Coordinates` 사용,
    필요 시 `Cube Coordinates` 사용
    """

    @property
    def placed_unit(self) -> Optional[BaseUnit]:
        return self.placed_unit

    @property
    def placed_structure(self) -> Optional[BaseStructure]:
        return self.placed_structure

    @property
    def defence_bonus(self) -> int:
        return self.defence_bonus

    @property
    def movement_cost(self) -> int:
        return self.movement_cost

    def __init__(self, q: int, r: int) -> None:
        self.position = Position(q, r)

    @placed_unit.setter
    def placed_unit(self, unit: BaseUnit) -> None:
        self.placed_unit = unit

    @placed_structure.setter
    def placed_structure(self, structure: BaseStructure) -> None:
        self.placed_structure = structure

    def get_distance(self, opposite: BaseTile) -> float:
        vec: Position = self.position - opposite.position
        return (abs(vec.q) +
                abs(vec.r) +
                abs(vec.q + vec.r)) / 2

    def on_unit_arrived(self) -> Any:
        if self.placed_structure is not None:
            self.placed_structure.on_arrived(self)

    def place_unit(self, unit: BaseUnit) -> None:
        self.placed_unit = unit

    def place_structure(self, structure: BaseStructure) -> None:
        self.placed_structure = structure

    def get_neighbors(self) -> list[AxialCoordinates]:
        map_data = GameSystem().map_data
        return [
            map_data[self.position.q + v.value.q][self.position.r + v.value.r].position \
            for v in HexDirectionVectors
        ]

    def get_path(self, b: Position) -> list[Position]:
        """
        a -> b로 이동하는 경로 리스트 반환
        """
        # 경로 탐색 구현
        # TileMeta.get_path() 에서 경로 계산 결과 반환 
        # UnitMeta.move() 에서 결과 값을 토대로 이동
        pass
