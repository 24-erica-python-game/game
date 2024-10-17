from enum import IntEnum
from typing import NamedTuple

from pygame.font import Font


class UIAlignment(IntEnum):
    left = 0
    center = 1
    right = 2
    top = 3
    bottom = 4


class UIPosition[T: int | float](NamedTuple):
    x: T
    y: T


class UISize[T: int | float](NamedTuple):
    x: T
    y: T


class BaseUI:
    @property
    def position(self) -> UIPosition:
        return self.position

    @position.setter
    def position(self, position: UIPosition):
        self.position = position

    @property
    def size(self) -> UISize:
        return self.size

    @size.setter
    def size(self, size: UISize):
        self.size = size

    @property
    def font(self) -> Font:
        return self.font

    @font.setter
    def font(self, font: Font):
        self.font = font

    def render(self, *args, **kwargs):
        raise NotImplementedError
