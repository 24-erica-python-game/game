from enum import IntEnum, Enum
from typing import NamedTuple


class Position(NamedTuple):
    q: int
    r: int
    s: int


class Distance(NamedTuple):
    d_q: int
    d_r: int
    d_s: int


class AnimationState(IntEnum):
    IDLE = 0
    MOVE = 1
    ATTACK = 2
    DEFEND = 3