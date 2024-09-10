from abc import ABCMeta, abstractmethod
from typing import Optional
from baseclasses.unit import BaseUnit
from baseclasses.types import *


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

    @abstractmethod
    def get_neighbors(self) -> list[AxialCoordinates]:
        pass

    @abstractmethod
    def get_path(self, b: Position) -> list[Position]:
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


class BaseTileMap:
    class Size(NamedTuple):
        width:  int
        height: int
        
    def __init__(cls, size: Size, default_tile: BaseTile):
        cls.size = size
        cls._map = [ [ default_tile(i, j) for j in range(size.width) ] for i in range(size.height) ]

    def __getitem__(self, idx: int) -> BaseTile:
        return self._map[idx]
    
    def __setitem__(self, idx: int, value: BaseTile) -> None:
        self._map[idx] = value
