from typing import Literal, TypeVar

import pygame as pg
from pygame.font import FontType

from game.ui.base import UIPosition, UISize
from game.ui.color import RGB
from game.ui.templates.interactable import Interactable


t_button_id = TypeVar('t_button_id')


class RadioButtonGroup:
    def __init__(self,
                 font: FontType,
                 label_pos: Literal["left", "right"],
                 default_active_id: t_button_id,
                 button_color: RGB,
                 active_color: RGB,
                 active_indicator_type: Literal["circle", "check"]):
        self.buttons = []
        self.font = font
        self.text_pos = label_pos
        self.active_id = default_active_id
        self.button_color = button_color
        self.active_color = active_color
        self.active_indicator_type = active_indicator_type

    def check_buttons_clicked(self):
        for button in self.buttons:
            button.check_button_clicked()

    def render_buttons(self):
        for button in self.buttons:
            button.render()

    def set_active(self, active_id: t_button_id):
        self.active_id = active_id

    def get_current_active(self) -> t_button_id:
        return self.active_id


class RadioButton(Interactable):
    def __init__(self,
                 group: RadioButtonGroup,
                 label: str,
                 pos: UIPosition,
                 radius: float,
                 button_id: t_button_id):
        super().__init__(UIPosition(pos.x - radius, pos.y - radius),
                         UISize(radius * 2, radius * 2))
        self.group = group
        self.label = label
        self.pos = pos
        self.radius = radius
        self.button_id = button_id

        self.tst_pos = UIPosition(pos.x - radius, pos.y - radius)
        self.tst_size = UISize(radius * 2, radius * 2)

        group.buttons.append(self)

    def check_button_clicked(self):
        # FIXME: 클릭 영역은 정사각형 영역으로 의도된 대로 잘 나타나지만 실제 클릭시 일부 영역만 클릭 가능함.
        #        클릭 가능한 영역이 표시된 부분과 다른 문제
        if self.is_mouse_in_area() and pg.mouse.get_pressed()[0]:
            self.group.set_active(self.button_id)

    def render(self):
        display = pg.display.get_surface()
        pg.draw.circle(display, self.group.button_color, self.pos, max(self.radius, 7))

        # TEMP: 클릭 영역 테스트용
        pg.draw.rect(display, RGB(255, 0, 0), (self.tst_pos, self.tst_size))

        # TODO: 레이블 그리기 구현

        if self.group.active_id == self.button_id:
            match self.group.active_indicator_type:
                case "circle":
                    # FIXME: 이미지 등을 이용해 만족스러운 라디오버튼을 구현하는것이 좋을 것으로 보임.
                    #        pygame의 원형은 만족스러운 원형이 나오지 않음.
                    pg.draw.circle(display,
                                   self.group.active_color,
                                   self.pos,
                                   max(self.radius - self.radius * 0.2, 5))
                case "check":
                    pg.draw.aalines(display,
                                    self.group.active_color,
                                    True,
                                    # FIXME: 체크표시 모양이 아래로 향해있으며, 의도된 모양보다 우측이 좀 더 x, y가 길게 표시됨.
                                    [(self.pos.x, self.pos.y), (self.pos.x * 0.95, self.pos.y * 1.05),   # left
                                     (self.pos.x, self.pos.y), (self.pos.x * 1.10, self.pos.y * 1.10)])  # right
