from abc import ABCMeta, abstractmethod
from typing import Optional
from baseclasses.unit import BaseUnit
from baseclasses.interface import *

class BaseTile(ABCMeta):
    def __init__(self, q: int, r: int, s: int) -> None:
        self.q = q
        self.r = r
        self.s = s

    @property
    def q(self) -> int:
        return self.q
    
    @property
    def r(self) -> int:
        return self.r
    
    @property
    def s(self) -> int:
        return self.s

    @property
    def placed_unit(self) -> Optional[BaseUnit]:
        return self.placed_unit

    @property
    def defence_bonus(self) -> int:
        return self.defence_bonus


    def __sub__(self, a: Position):
        return BaseTile(self.q - a.q, self.r - a.r, self.s - a.s)
        
    def __add__(self, a: Position):
        return BaseTile(self.q + a.q, self.r + a.r, self.s + a.s)

    def __abs__(self):
        return BaseTile(abs(self.q), abs(self.r), abs(self.s))


    @abstractmethod
    def on_arrived(self) -> None:
        pass

    @placed_unit.setter
    def place_unit(self, unit: BaseUnit) -> None:
        self.placed_unit = unit

    @staticmethod
    def get_distance(self, b: Position) -> float:
        vec: Distance = BaseTileMap[BaseTile.position] # 현재 지도를 나타내는 객체 생길 경우 그 객체로 변경
                                                       # __index__() 필요
        return (abs(vec.d_q) + abs(vec.d_r) + abs(vec.d_s)) / 2
    

class BaseTileMap:
    """
    타일을 1차원으로 배열한 클래스.\n
    2차원 지도로 사용하기 위해서는 List[TileMapMeta] 형태로 사용
    """
    def __new__(cls, size: int):
        cls.size = size
        cls._map: list[BaseTileMap] = []

    def __getitem__(self, idx: int):
        return self._map[idx]
