from typing import NamedTuple

from pygame.font import Font


class UIPosition(NamedTuple):
    x: float
    y: float


class UISize(NamedTuple):
    x: float
    y: float


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
