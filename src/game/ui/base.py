from abc import abstractmethod, ABCMeta
from typing import NamedTuple

from pygame import Surface
from pygame.font import Font


class UIPosition(NamedTuple):
    x: int
    y: int


class UISize(NamedTuple):
    x: int
    y: int


class RGB(NamedTuple):
    r: int
    g: int
    b: int


class RGBA(NamedTuple):
    r: int
    g: int
    b: int
    a: int


def to_rgba(color: RGB) -> RGBA:
    return RGBA(color.r, color.g, color.b, 0)

def to_rgb(color: RGBA) -> RGB:
    return RGB(color.r, color.g, color.b)


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
