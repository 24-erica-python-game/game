from typing import Literal, TypeVar

import pygame as pg
from pygame import gfxdraw as gfx
from pygame.font import FontType

from game.ui.base import UIPosition, UISize, UIAlignment
from game.ui.color import RGB
from game.ui.templates.interactable import Interactable
from game.ui.templates.textbox import TextBox

t_button_id = TypeVar('t_button_id')


class RadioButtonGroup:
    def __init__(self,
                 font: FontType,
                 label_pos: Literal[UIAlignment.left, UIAlignment.right],
                 label_alignment: Literal[UIAlignment.left, UIAlignment.center, UIAlignment.right, "test"],
                 label_color: RGB,
                 label_distance: int,
                 default_active_id: t_button_id,
                 button_color: RGB,
                 active_color: RGB):
        """
        라디오버튼 그룹을 생성함. 그룹당 하나의 활성화된 라디오버튼만 존재할 수 있다.
        :param font: 라디오버튼 레이블의 폰트
        :param label_pos: 라디오버튼 레이블의 위치
        :param label_alignment: 라디오버튼 레이블의 정렬 위치
        :param label_color: 라디오버튼 레이블의 색상
        :param label_distance: 라디오버튼 레이블이 버튼과 떨어져 있는 간격
        :param default_active_id: 처음 상태에서 활성화될 버튼의 ID
        :param button_color: 버튼의 기본 색상
        :param active_color: 활성화 되었을 경우 버튼의 색상
        """
        self.buttons = []
        self.font = font
        self.label_pos = label_pos
        self.label_alignment = label_alignment
        self.label_color = label_color
        self.label_distance = label_distance
        self.active_id = default_active_id
        self.button_color = button_color
        self.active_color = active_color

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

    def get_longest_text_size(self) -> UISize:
        longest = max([self.font.render(button.label, True, self.label_color).get_size()
                       for button in self.buttons])
        return UISize(longest[0], longest[1])


class RadioButton(Interactable):
    def __init__(self,
                 group: RadioButtonGroup,
                 label: str,
                 pos: UIPosition,
                 radius: float,
                 button_id: t_button_id):
        """
        라디오버튼을 생성함. 라디오버튼은 라디오버튼 그룹에 속해있어야 함.
        :param group: 버튼이 속해있는 그룹
        :param label: 라디오버튼의 레이블
        :param pos: 버튼의 위치
        :param radius: 버튼의 반지름
        :param button_id: 버튼의 ID
        """
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
        if self.is_mouse_in_area() and pg.mouse.get_pressed()[0]:
            self.group.set_active(self.button_id)

    def render(self):
        display = pg.display.get_surface()
        pos = self.pos
        gfx.aacircle(display,
                     pos.x,
                     pos.y,
                     int(max(self.radius, 2)),
                     self.group.button_color)

        # DEBUG: 클릭 영역 테스트용
        # pg.draw.rect(display, RGB(255, 0, 0), (self.tst_pos, self.tst_size))

        label = self.group.font.render(self.label, True, self.group.label_color)
        longest_text_size = self.group.get_longest_text_size()
        text_size = UISize(label.get_size()[0], label.get_size()[1])
        textbox_pos_x = 0

        match self.group.label_pos:
            case UIAlignment.left:
                textbox_pos_x = pos.x - self.group.label_distance - longest_text_size.x
            case UIAlignment.right:
                textbox_pos_x = pos.x + self.group.label_distance

        textbox = TextBox(UIPosition(textbox_pos_x, pos.y - text_size.y / 2),
                          longest_text_size,
                          self.group.font,
                          self.label,
                          self.group.label_color,
                          self.group.label_alignment)

        textbox.render()

        if self.group.active_id == self.button_id:
            gfx.aacircle(display,
                         pos.x,
                         pos.y,
                         int(max(self.radius, 2)) - 2,
                         self.group.active_color)
            gfx.filled_circle(display,
                         pos.x,
                         pos.y,
                         int(max(self.radius, 2)) - 2,
                         self.group.active_color)
