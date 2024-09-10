from abc import abstractmethod, ABCMeta
from typing import NamedTuple

from pygame.font import Font


class UIPosition(NamedTuple):
    x: int
    y: int


class UISize(NamedTuple):
    x: int
    y: int


class UI(ABCMeta):
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

    @abstractmethod
    def render(self, *args):
        pass
