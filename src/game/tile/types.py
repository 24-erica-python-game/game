from enum import IntEnum, Enum
from typing import NamedTuple, Optional, Self


class AxialCoordinates:
    """
    대상의 위치를 나타내는 자료형
    """

    def __init__(self, q: int, r: int):
        self.q = q
        self.r = r
        # self.s = -q - r

    def __sub__(self, opposite: Self) -> Self:
        return Position(
            self.q - opposite.q,
            self.r - opposite.r
        )

    def __add__(self, opposite: Self) -> Self:
        return Position(
            self.q + opposite.q,
            self.r + opposite.r
        )

    def distance_to(self, opposite: Self) -> float:
        return (abs(self.q - opposite.q) +
                abs(self.q - opposite.q  +
                    self.r - opposite.r) +
                abs(self.r - opposite.r)) / 2


class CubeCoordinates:
    """
    `q`, `r`, `s` 의 좌표로 위치를 나타내는 자료형.
    """

    def __init__(self, q: int, r: int, s: int):
        self.q = q
        self.r = r
        self.s = s

    def __sub__(self, opposite: Self) -> Self:
        return CubeCoordinates(
            self.q - opposite.q,
            self.r - opposite.r,
            self.s - opposite.s
        )

    def __add__(self, opposite: Self) -> Self:
        return CubeCoordinates(
            self.q + opposite.q,
            self.r + opposite.r,
            self.s + opposite.s
        )

    def distance_to(self, opposite: Self) -> float:
        return (abs(self.q - opposite.q) +
                abs(self.r - opposite.r) +
                abs(self.s - opposite.s)) / 2


def cube_to_axial_coordinates(c: CubeCoordinates) -> AxialCoordinates:
    return AxialCoordinates(q=c.q, r=c.r)


def axial_to_cube_coordinates(c: AxialCoordinates) -> CubeCoordinates:
    return CubeCoordinates(q=c.q, r=c.r, s=(-c.q - c.r))


class Position(AxialCoordinates):
    """
    `AxialCoordinates` 의 별칭
    """
    pass


class HexDirections(IntEnum):
    """
    육각면의 방향을 나타내는 열거형
    """
    __order__ = "EAST SOUTHEAST SOUTHWEST WEST NORTHWEST NORTHEAST"
    EAST = 0
    SOUTHEAST = 1
    SOUTHWEST = 2
    WEST = 3
    NORTHWEST = 4
    NORTHEAST = 5


class Distance(NamedTuple):
    """
    두 점 사이의 거리를 나타내는 자료형
    """
    d_q: float
    d_r: float
    d_s: Optional[float]


class _Direction(NamedTuple):
    q: int
    r: int


class HexDirectionVectors(Enum):
    """
    육각형 방향 벡터
    """
    __order__ = "EAST SOUTHEAST SOUTHWEST WEST NORTHWEST NORTHEAST"
    EAST = _Direction(+1, 0)
    SOUTHEAST = _Direction(0, +1)
    SOUTHWEST = _Direction(-1, +1)
    WEST = _Direction(-1, 0)
    NORTHWEST = _Direction(0, -1)
    NORTHEAST = _Direction(+1, -1)
