from abc import ABCMeta, abstractmethod
from typing import Optional
from unit.base import BaseUnit
from tile.types import *


class BaseTile: pass
class BaseTile(metaclass=ABCMeta):
    """
    | https://www.redblobgames.com/grids/hexagons/
    | 기본: `Axial Coordinates` 사용
    | 필요 시 `Cube Coordinates` 사용
    """
    @property
    def placed_unit(self) -> Optional[BaseUnit]:
        return self.placed_unit

    @property
    def defence_bonus(self) -> int:
        return self.defence_bonus
    
    @property
    def movement_cost(self) -> int:
        return self.movement_cost

    def __init__(self, q: int, r: int) -> None:
        self.position = Position(q, r)


    @abstractmethod
    def on_arrived(self) -> None:
        pass

    @placed_unit.setter
    def place_unit(self, unit: BaseUnit) -> None:
        self.placed_unit = unit

    def get_distance(self, opposite: BaseTile) -> float:
        vec: Position = self.position - opposite.position
        return Distance((
            abs(vec.q) +
            abs(vec.r) +
            abs(vec.q  + vec.r)) / 2)

    @abstractmethod
    def get_neighbors(self) -> list[AxialCoordinates]:
        pass

    @abstractmethod
    def get_path(self, b: Position) -> list[Position]:
        """
        a -> b로 이동하는 경로 리스트 반환
        """
        # 경로 탐색 구현
        # TileMeta.get_path() 에서 경로 계산 결과 반환 
        # UnitMeta.move() 에서 결과 값을 토대로 이동
    

class BaseTileMap:
    """
    | 타일을 1차원으로 배열한 클래스.
    | 2차원 지도로 사용하기 위해서는 `List[BaseTileMap]` 형태로 사용
    """
    def __new__(cls, size: int):
        cls.size = size
        cls._map: list[BaseTileMap] = []

    def __getitem__(self, idx: int):
        return self._map[idx]
