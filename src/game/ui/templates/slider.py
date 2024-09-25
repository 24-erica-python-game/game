from typing import NamedTuple

import pygame as pg
from pygame import gfxdraw as gfx
import numpy as np

from game.ui.base import UIPosition, UISize
from game.ui.color import RGB
from game.ui.templates.interactable import Interactable


class SliderHead(Interactable):
    def __init__(self, *, radius: int):
        """
        슬라이더의 헤드 객체
        :param radius: (keyword-only) 원형 모양 헤드의 반지름
        """
        self.radius = radius
        super().__init__(UIPosition(0, 0), UISize(radius * 2, radius * 2))

    def render(self):
        display = pg.display.get_surface()
        pg.draw.circle(display, RGB(230, 230, 230), self.pos, self.radius)
        gfx.aacircle(display, int(self.pos.x), int(self.pos.y), self.radius, RGB(200, 200, 200))


class Slider[T: int | float]:
    class ValueRange(NamedTuple):
        min_: T
        max_: T
        step_: T

    def __init__(self,
                 value_range: tuple[T, T, T],
                 head: SliderHead,
                 start_pos: UIPosition,
                 end_pos: UIPosition,
                 color: RGB):
        """
        슬라이더 객체를 생성함, 헤드를 클릭한 상태로 드래그해 값을 조정함

        :param value_range: ``(min_,max_,step_)`` 로 구성됨. 세 값은 모두 ``int`` 또는 ``float`` 이면서 세 값의 타입이 서로 같아야 함
        :param head: 슬라이더의 헤드
        :param start_pos: 슬라이더 바의 시작 위치, ``end_pos`` 보다 x값이 클 수 없다
        :param end_pos: 슬라이더 바의 끝 위치, ``start_pos`` 보다 x값이 작을 수 없다
        :param color: 슬라이더 바의 색상
        """
        if start_pos.x > end_pos.x:
            raise ValueError(f"start_pos value must be less than end_pos value\n"
                             f"current start_pos value : {start_pos.x}\n"
                             f"current end_pos value   : {end_pos.x}")
        self.value_range = Slider.ValueRange(value_range[0], value_range[1], value_range[2])
        self.value = 0
        self.head = head
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.color = color
        range_ = np.arange(self.value_range.min_, self.value_range.max_ + self.value_range.step_, self.value_range.step_)
        self.range_list = list(map(float, range_))

    def clamp_head_pos(self, pos: UIPosition):
        try:
            a = (self.end_pos.y - self.start_pos.y) / (self.end_pos.x - self.start_pos.x)
            b = self.end_pos.y - a * self.end_pos.x
            x = pg.math.clamp(pos.x, self.start_pos.x, self.end_pos.x)
            y = a*x + b
            return UIPosition(x, y)
        except ZeroDivisionError:
            if self.start_pos.y < self.end_pos.y:
                y = pg.math.clamp(pos.y, self.start_pos.y, self.end_pos.y)
            else:
                y = pg.math.clamp(pos.y, self.end_pos.y, self.start_pos.y)
            return UIPosition(self.start_pos.x, y)

    def set_value_from_pos(self):
        try:
            d = (self.end_pos.x - self.start_pos.x)  # 0 <= d_x
            start_pos_ = self.start_pos.x
            head_pos = self.head.pos.x
        except ZeroDivisionError:
            d = (self.end_pos.y - self.start_pos.y)  # 0 <= d_y
            head_pos = self.head.pos.y
            start_pos_ = self.start_pos.y

        min__ = start_pos_ / d
        # max__ = end_pos_ / d_y
        # max__ - min__ = 1
        v = ((head_pos / d) - min__) * (self.value_range.max_ - self.value_range.min_)
        print(f"v: {v}")
        nearest = min(self.range_list, key=lambda i: abs(i - v))
        print(f"nearest: {nearest}")
        self.value = nearest

    def set_value_from_value(self, value: T):
        self.value = pg.math.clamp(value, self.value_range.min_, self.value_range.max_)
        try:
            d = (self.end_pos.x - self.start_pos.x)  # 0 <= d_x
            start_pos_ = self.start_pos.x
            min__ = start_pos_ / d
            head_pos = ((value / (self.value_range.max_ - self.value_range.min_)) + min__) * d
            self.head.pos = self.clamp_head_pos(UIPosition(head_pos, 0.0))
        except ZeroDivisionError:
            d = (self.end_pos.y - self.start_pos.y)  # 0 <= d_y
            start_pos_ = self.start_pos.y
            min__ = start_pos_ / d
            head_pos = ((value / (self.value_range.max_ - self.value_range.min_)) + min__) * d
            self.head.pos = self.clamp_head_pos(UIPosition(0.0, head_pos))
        print(f"head_pos: {head_pos}")

    def on_head_clicked(self):
        self.head.pos = self.clamp_head_pos(UIPosition(pg.mouse.get_pos()[0],
                                                       pg.mouse.get_pos()[1]))
        self.set_value_from_pos()

    def render(self):
        display = pg.display.get_surface()

        # bar
        pg.draw.aaline(display, RGB(200, 200, 200), self.start_pos, self.end_pos)

        # head
        self.head.render()
