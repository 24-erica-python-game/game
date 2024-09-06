from enum import IntEnum, Enum
from typing import NamedTuple, Optional


class AxialCoordinates: pass
class CubeCoordinates: pass


class Position(AxialCoordinates):
    """
    대상의 위치를 나타내는 자료형
    """
    def __init__(self, q: int, r: int):
        self.q = q
        self.r = r

    def __sub__(self, opposite: AxialCoordinates) -> AxialCoordinates:
        return Position(
            self.q-opposite.q, 
            self.r-opposite.r
        )

    def __add__(self, opposite: AxialCoordinates) -> AxialCoordinates:
        return Position(
            self.q+opposite.q, 
            self.r+opposite.r
        )
    
    @staticmethod
    def _axial_to_cube_coordinates(c: AxialCoordinates) -> CubeCoordinates:
        return CubeCoordinates(q=c.q, r=c.r, s=(-c.q - c.r))


class CubeCoordinates:
    """
    | `q, r, s`의 좌표로 위치를 나타내는 자료형.
    | `s = -q - r`
    """
    def __init__(self, q: int, r: int, s: int):
        self.q = q
        self.r = r
        self.s = s

    def __sub__(self, opposite: CubeCoordinates) -> CubeCoordinates:
        return CubeCoordinates(
            self.q-opposite.q,
            self.r-opposite.r,
            self.s-opposite.s
        )

    def __add__(self, opposite: CubeCoordinates) -> CubeCoordinates:
        return CubeCoordinates(
            self.q+opposite.q,
            self.r+opposite.r,
            self.s+opposite.s
        )
    
    @staticmethod
    def _cube_to_axial_coordinates(c: CubeCoordinates) -> AxialCoordinates:
        return AxialCoordinates(q=c.q, r=c.r)

class HexDirections(IntEnum):
    """
    육각형에서 각 면을 나타내는 방향을 나타내는 열거형
    """
    __order__ = "EAST SOUTHEAST SOUTHWEST WEST NORTHWEST NORTHEAST"
    EAST      = 0
    SOUTHEAST = 1
    SOUTHWEST = 2
    WEST      = 3
    NORTHWEST = 4
    NORTHEAST = 5


class Distance(NamedTuple):
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
    EAST      = _Direction(+1,  0)
    SOUTHEAST = _Direction( 0, +1)
    SOUTHWEST = _Direction(-1, +1)
    WEST      = _Direction(-1,  0)
    NORTHWEST = _Direction( 0, -1)
    NORTHEAST = _Direction(+1, -1)


class AnimationState(IntEnum):
    """
    IDLE
        기본 상태 (아무런 행동도 없을 경우)

    MOVE
        이동 시 애니메이션

    ATTACK
        공격 시 애니메이션

    DEFEND
        방어 시 애니메이션
    """
    IDLE = 0
    MOVE = 1
    ATTACK = 2
    DEFEND = 3