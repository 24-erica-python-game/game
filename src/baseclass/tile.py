from abc import ABCMeta, abstractmethod
from typing import NamedTuple, Union, Optional
from unit import UnitMeta


class Position(NamedTuple):
    q: int
    r: int
    s: int


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


    @abstractmethod
    def on_arrived(self) -> None:
        pass

    @placed_unit.setter
    def place_unit(self, unit: UnitMeta) -> None:
        self.placed_unit = unit
