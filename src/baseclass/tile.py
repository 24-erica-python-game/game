from abc import ABCMeta, abstractmethod
from typing import NamedTuple, Optional
from unit import UnitMeta


class Position(NamedTuple):
    q: int
    r: int
    s: int


class Distance(NamedTuple):
    d_q: int
    d_r: int
    d_s: int


class TileMeta(ABCMeta):
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
    def placed_unit(self) -> Optional[UnitMeta]:
        return self.placed_unit

    @property
    def defence_bonus(self) -> int:
        return self.defence_bonus


    def __sub__(self, a: Position):
        return TileMeta(self.q - a.q, self.r - a.r, self.s - a.s)
        
    def __add__(self, a: Position):
        return TileMeta(self.q + a.q, self.r + a.r, self.s + a.s)

    def __abs__(self):
        return TileMeta(abs(self.q), abs(self.r), abs(self.s))


    @abstractmethod
    def on_arrived(self) -> None:
        pass

    @placed_unit.setter
    def place_unit(self, unit: UnitMeta) -> None:
        self.placed_unit = unit

    @staticmethod
    def get_distance(self, b: Position) -> float:
        vec: Distance = Map[TileMeta.position] # 현재 지도를 나타내는 객체 생길 경우 그 객체로 변경
                                               # __index__() 필요
        return (abs(vec.d_q) + abs(vec.d_r) + abs(vec.d_s)) / 2