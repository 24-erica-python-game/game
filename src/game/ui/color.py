from typing import NamedTuple


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


class Color:
    RED   = RGB(255,   0,   0)
    GREEN = RGB(  0, 255,   0)
    BLUE  = RGB(  0,   0, 255)
    WHITE = RGB(255, 255, 255)
    BLACK = RGB(  0,   0,   0)
