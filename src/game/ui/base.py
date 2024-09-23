from typing import NamedTuple, overload
from enum import IntEnum

from pygame.font import Font


class UIAlignment(IntEnum):
    left = 0
    center = 1
    right = 2
    top = 3
    bottom = 4


class FloatUIPosition(NamedTuple):
    x: float
    y: float


class IntUIPosition(NamedTuple):
    x: int
    y: int


class FloatUISize(NamedTuple):
    x: float
    y: float


class IntUISize(NamedTuple):
    x: int
    y: int


@overload
def convert(t: FloatUIPosition) -> IntUIPosition: ...

@overload
def convert(t: IntUIPosition) -> FloatUIPosition: ...

@overload
def convert(t: FloatUISize) -> IntUISize: ...

@overload
def convert(t: IntUISize) -> FloatUISize: ...


def convert(t):
    if isinstance(t, FloatUIPosition):
        return IntUIPosition(int(t.x), int(t.y))
    elif isinstance(t, IntUIPosition):
        return FloatUIPosition(float(t.x), float(t.y))
    elif isinstance(t, FloatUISize):
        return IntUISize(int(t.x), int(t.y))
    elif isinstance(t, IntUISize):
        return FloatUISize(int(t.x), int(t.y))


class BaseUI:
    @property
    def position(self) -> FloatUIPosition:
        return self.position

    @position.setter
    def position(self, position: FloatUIPosition):
        self.position = position

    @property
    def size(self) -> FloatUISize:
        return self.size

    @size.setter
    def size(self, size: FloatUISize):
        self.size = size

    @property
    def font(self) -> Font:
        return self.font

    @font.setter
    def font(self, font: Font):
        self.font = font

    def render(self, *args, **kwargs):
        raise NotImplementedError
