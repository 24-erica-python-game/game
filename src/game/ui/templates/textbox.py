from typing import Literal

import pygame as pg
from pygame.font import FontType

from game.ui.base import FloatUIPosition, FloatUISize, UIAlignment, IntUISize, convert
from game.ui.color import RGB
from game.ui.templates.interactable import Interactable


class Textbox(Interactable):
    def __init__(self,
                 pos: FloatUIPosition,
                 size: FloatUISize,
                 font: FontType,
                 label: str,
                 color: RGB,
                 alignment: Literal[UIAlignment.left, UIAlignment.center, UIAlignment.right]):
        """
        텍스트박스 객체를 생성함. 주어진 크기 안에서 텍스트를 정렬함.
        :param pos: 텍스트박스의 위치
        :param size: 텍스트박스의 크기
        :param font: 텍스트의 폰트
        :param label: 텍스트의 내용
        :param color: 텍스트의 색상
        :param alignment: 텍스트 정렬 방법
        """
        self.pos = pos
        self.size = size
        self.font = font
        self.label = label
        self.color = color
        self.alignment = alignment
        super().__init__(pos, max([font.render(label, True, color).get_size(), size]))

    def render(self):
        display = pg.display.get_surface()
        pos = convert(self.pos)
        text = self.font.render(self.label, True, self.color)
        text_size = IntUISize(text.get_size()[0], text.get_size()[1])
        label_pos_x = 0

        # DEBUG: 텍스트박스 영역 표시
        # pg.draw.rect(display, RGB(200, 200, 200), (pos.x, pos.y, self.size[0], self.size[1]))

        match self.alignment:
            case UIAlignment.left:
                label_pos_x = pos.x
            case UIAlignment.center:
                label_pos_x = pos.x + (self.size[0] - text_size.x) / 2
            case UIAlignment.right:
                label_pos_x = pos.x + (self.size[0] - text_size.x)

        display.blit(text, (label_pos_x, pos.y))
