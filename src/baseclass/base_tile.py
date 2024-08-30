from abc import ABCMeta, abstractmethod
from typing import NamedTuple, Union, Optional
from base_unit import UnitMeta

class Postiion(NamedTuple):
    x: int
    y: int


class TileMeta(ABCMeta):
    @property
    def placed_unit(self) -> Optional[UnitMeta]:
        return self.placed_unit

    @abstractmethod
    def on_arrived(self):
        pass
    