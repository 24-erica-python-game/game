from enum import IntEnum
from os import PathLike
from typing import NamedTuple, Optional

import numpy as np
import pygame as pg
from pygame import gfxdraw as gfx, SurfaceType, BLEND_RGBA_MULT

from game.ui.base import UIPosition, UISize
from game.ui.color import RGB, RGBA
from game.ui.templates.interactable import Interactable


class SliderHeadShape(IntEnum):
    CIRCLE = 0
    RECTANGLE = 1
    IMAGE = 2


class SliderHead(Interactable):
    def __init__(self, size: UISize):
        self.primary_color = RGB(230, 230, 230)
        self.secondary_color = RGB(200, 200, 200)
        self.shape = SliderHeadShape.RECTANGLE
        self.img: Optional[SurfaceType] = None
        self.radius: Optional[int] = None
        super().__init__(UIPosition(0, 0), size)

    @classmethod
    def from_circle(cls, radius: int):
        initialized = SliderHead(UISize(radius ** 2, radius ** 2))
        initialized.radius = radius
        initialized.shape = SliderHeadShape.CIRCLE
        return initialized

    @classmethod
    def from_rect(cls, size: UISize):
        initialized = SliderHead(size)
        initialized.size = size
        initialized.shape = SliderHeadShape.RECTANGLE
        return initialized

    @classmethod
    def from_image(cls, path: PathLike, size: UISize):
        initialized = SliderHead(size)
        img = pg.image.load(path).convert_alpha()
        initialized.img = pg.transform.scale(img, size)
        initialized.size = size
        initialized.shape = SliderHeadShape.IMAGE
        return initialized

    def set_color(self, *, primary: RGB | RGBA = None, secondary: RGB | RGBA = None):
        """
        슬라이더 헤드의 색상을 변경함
        :param primary: 슬라이더 헤드의 색상
        :param secondary: 슬라이더 헤드의 테두리 색상
        :return:
        """
        if primary is not None:
            self.primary_color = primary
        if secondary is not None:
            self.secondary_color = secondary

    def update(self):
        display = pg.display.get_surface()
        match self.shape:
            case SliderHeadShape.CIRCLE:
                pg.draw.circle(display, self.primary_color, self.pos, self.radius)
                gfx.aacircle(display, int(self.pos.x), int(self.pos.y), self.radius, RGB(200, 200, 200))
            case SliderHeadShape.RECTANGLE:
                pg.draw.rect(display, self.primary_color, (self.pos, self.size))
                gfx.rectangle(display, (self.pos, self.size), RGB(200, 200, 200))
            case SliderHeadShape.IMAGE:
                screen = pg.display.get_surface()
                screen.blit(self.img, self.pos, special_flags=pg.BLEND_RGBA_MULT)


class Slider[T: int | float]:
    drag = False
    __instances = []

    class ValueRange(NamedTuple):
        min_: T
        max_: T
        step_: T

    def __init__(self,
                 value_range: tuple[T, T, T],
                 head: SliderHead,
                 start_pos: UIPosition,
                 end_pos: UIPosition):
        """
        슬라이더 객체를 생성함, 헤드를 클릭한 상태로 드래그해 값을 조정함

        :param value_range: ``(min_,max_,step_)`` 로 구성됨. 세 값은 모두 ``int`` 또는 ``float`` 이면서 세 값의 타입이 서로 같아야 함
        :param head: 슬라이더의 헤드
        :param start_pos: 슬라이더 바의 시작 위치, ``end_pos`` 보다 x값이 클 수 없다
        :param end_pos: 슬라이더 바의 끝 위치, ``start_pos`` 보다 x값이 작을 수 없다
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
        self.color = RGBA(0, 0, 0, 255)
        range_ = np.arange(self.value_range.min_, self.value_range.max_ + self.value_range.step_,
                           self.value_range.step_)
        self.range_list = list(map(float, range_))
        self.drag_ = False
        Slider.__instances.append(self)

    def clamp_head_pos(self, pos: UIPosition):
        """
        슬라이더 헤드가 슬라이더 바로부터 벗어나지 않도록 고정하는 함수
        :param pos: 슬라이더 헤드의 위치
        :return:
        """
        try:
            a = (self.end_pos.y - self.start_pos.y) / (self.end_pos.x - self.start_pos.x)
            b = self.end_pos.y - a * self.end_pos.x
            x = pg.math.clamp(pos.x, self.start_pos.x, self.end_pos.x)
            y = a * x + b
            match self.head.shape:
                case SliderHeadShape.CIRCLE:
                    return UIPosition(x, y)
                case SliderHeadShape.RECTANGLE | SliderHeadShape.IMAGE:
                    return UIPosition(x - (self.head.size.x / 2), y - (self.head.size.y / 2))
        except ZeroDivisionError:
            if self.start_pos.y < self.end_pos.y:
                y = pg.math.clamp(pos.y, self.start_pos.y, self.end_pos.y)
            else:
                y = pg.math.clamp(pos.y, self.end_pos.y, self.start_pos.y)
            match self.head.shape:
                case SliderHeadShape.CIRCLE:
                    return UIPosition(self.start_pos.x, y)
                case SliderHeadShape.RECTANGLE | SliderHeadShape.IMAGE:
                    return UIPosition(self.start_pos.x - (self.head.size.x / 2), y - (self.head.size.y / 2))

    def set_value_from_pos(self):
        """
        슬라이더 헤드의 위치를 토대로 값을 설정함
        :return:
        """
        try:
            d = (self.end_pos.x - self.start_pos.x)  # 0 <= d_x
            start_pos_ = self.start_pos.x
            head_pos = self.head.pos.x
            min__ = start_pos_ / d
        except ZeroDivisionError:
            d = (self.end_pos.y - self.start_pos.y)  # 0 <= d_y
            head_pos = self.head.pos.y
            start_pos_ = self.start_pos.y
            min__ = start_pos_ / d

        # max__ = end_pos_ / d_y
        # max__ - min__ = 1
        v = ((head_pos / d) - min__) * (self.value_range.max_ - self.value_range.min_)
        # print(f"v: {v}")
        nearest = min(self.range_list, key=lambda i: abs(i - v))
        # print(f"nearest: {nearest}")
        self.value = nearest

    def set_value_from_value(self, value: T):
        """
        주어진 값을 토대로 슬라이더 헤드의 위치를 설정함
        :param value: 설정할 값
        :return:
        """
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
        # print(f"head_pos: {head_pos}")

    def set_color(self, color: RGB | RGBA):
        """
        슬라이더 바의 색상을 변경함, 슬라이더 헤드의 색상을 변경하려면 슬라이더 헤드의 ``set_color`` 메서드를 호출해야함
        :param color: 변경할 색상
        :return:
        """
        self.color = color

    def on_head_clicked(self):
        """
        슬라이더 헤드가 클릭되었을 때 호출되어야 하는 함수, 이 함수를 통해 슬라이더 헤드의 위치를 설정함.
        :return:
        """
        self.head.pos = self.clamp_head_pos(UIPosition(pg.mouse.get_pos()[0],
                                                       pg.mouse.get_pos()[1]))
        self.set_value_from_pos()

    @staticmethod
    def on_mousebutton_down():
        """
        >>> for event in pg.event.get():
        ...     match event.type:
        ...         case pg.QUIT:
        ...             running = False
        ...         case pg.MOUSEBUTTONDOWN:
        ...             Slider.on_mousebutton_down()
        ...         case pg.MOUSEBUTTONUP:
        ...             Slider.on_mousebutton_up()

        슬라이더의 드래그 상태를 조작하기 위해 ``pg.MOUSEBUTTONDOWN`` 이벤트를 수신받으면 호출해야 하는 함수
        :return:
        """
        Slider.drag = True

    @staticmethod
    def on_mousebutton_up():
        """
        >>> for event in pg.event.get():
        ...     match event.type:
        ...         case pg.QUIT:
        ...             running = False
        ...         case pg.MOUSEBUTTONDOWN:
        ...             Slider.on_mousebutton_down()
        ...         case pg.MOUSEBUTTONUP:
        ...             Slider.on_mousebutton_up()

        슬라이더의 드래그 상태를 조작하기 위해 ``pg.MOUSEBUTTONDOWN`` 이벤트를 수신받으면 호출해야 하는 함수
        :return:
        """
        for slider in Slider.__instances:
            slider.drag_ = False

    def update(self):
        # FIXME: 슬라이더를 드래그하면서 다른 슬라이더의 헤드가 마우스 위에 있으면 그 슬라이더까지 값이 변경되는 문제
        if Slider.drag and self.head.is_mouse_in_area():
            self.drag_ = True
        if self.drag_ and pg.mouse.get_pressed()[0]:
            self.on_head_clicked()

        display = pg.display.get_surface()

        # bar
        pg.draw.aaline(display, self.color, self.start_pos, self.end_pos)

        # head
        self.head.update()


if __name__ == "__main__":
    from game.ui.templates.textbox import TextBox

    pg.init()

    small_font = pg.font.SysFont("malgungothic", 14, False, False)

    # 화면 크기 지정
    size = (400, 300)
    screen = pg.display.set_mode(size)

    pg.display.set_caption("Buggy Buddies")

    # FPS 관련 설정
    running = True
    clock = pg.time.Clock()

    screen.fill(RGBA(0, 255, 0, 255), special_flags=BLEND_RGBA_MULT)

    head = SliderHead.from_circle(3)
    slider = Slider((0.0, 100.0, 2.5), head, UIPosition(150.0, 150.0), UIPosition(250.0, 150.0))
    slider.set_color(RGBA(0, 0, 0, 0))
    slider.set_value_from_value(50)

    textbox = TextBox(UIPosition(150, 125), UISize(100, 20), small_font, str(slider.value))

    square_head = SliderHead.from_rect(UISize(10, 20))
    slider_2 = Slider((0, 10, 1), square_head, UIPosition(135, 100), UIPosition(135, 140))
    slider_2.set_value_from_value(2)

    slider_2.head.set_color(primary=RGBA(230, 230, 230, 0))

    while running:
        screen.fill(RGBA(0, 255, 0, 255), special_flags=BLEND_RGBA_MULT)
        clock.tick(30)

        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    running = False
                case pg.MOUSEBUTTONDOWN:
                    Slider.on_mousebutton_down()
                case pg.MOUSEBUTTONUP:
                    Slider.on_mousebutton_up()

        slider.update()
        textbox.label = f"{slider.value:.1f}"
        textbox.update()

        slider_2.update()

        pg.display.flip()
