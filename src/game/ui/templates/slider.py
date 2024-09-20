from typing import Literal

from game.ui.base import UIPosition, UISize
from game.ui.color import RGBA
from game.ui.templates.interactable import Interactable


class SliderHead(Interactable):
    def __init__(self, pos: UIPosition, size: UISize):
        super().__init__(pos, size)


class Slider[T: int | float]:
    def __init__(self,
                 value_range: tuple[T, T, T],
                 default_value: T,
                 head_type: Literal["bar", "triangle", "inv_triangle", "circle"],
                 head_size: UISize,
                 head_color: RGBA,
                 pos: UIPosition,
                 size: UISize,
                 color: RGBA,
                 interpolation=None,):
        """
        슬라이더 객체를 생성함, 헤드를 클릭한 상태로 드래그해 값을 조정함
        :param value_range: (min, max, multiplier)로 구성됨. 세 값은 모두 int 또는 float형이면서 세 값의 타입이 서로 같아야 함.
        :param default_value: 슬라이더가 생성될 때 기본값
        :param head_type: ``"bar"``, ``"triangle"``, ``"inv_triangle"``, ``"circle"`` 이 될 수 있음
        :param head_size: 헤드의 크기
        :param head_color: 헤드의 색상
        :param pos: 슬라이더의 위치
        :param size: 슬라이더의 크기
        :param color: 슬라이더 바의 색상
        """
        self.value_range = value_range
        self.value = default_value
        self.head_type = head_type
        self.head_size = head_size
        self.head_color = head_color
        self.pos = pos
        self.size = size
        self.color = color


class Scrollbar(Slider):
    pass
