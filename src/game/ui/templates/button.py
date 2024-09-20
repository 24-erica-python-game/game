from typing import Optional

import pygame as pg
from pygame.font import FontType

from src.game.ui.base import UIPosition, UISize
from src.game.ui.color import RGB


class Button:
    """
    버튼 템플릿 클래스

    이 클래스를 상속받은 후 on_clicked 메서드를 오버라이드해 버튼 클릭시 동작을 정의해 사용
    """
    def __init__(self,
                 label: str,
                 label_font: pg.font.FontType,
                 pos: UIPosition,
                 size: UISize,
                 foreground: RGB,
                 background: RGB):
        self.label = label
        self.font = label_font
        self.pos = pos
        self.size = size
        self.foreground = foreground
        self.background = background

    def set_color(self, foreground: Optional[RGB] = None, background: Optional[RGB] = None):
        """
        버튼의 색상을 설정함
        :param foreground: 글자의 색, None일 경우 변경하지 않음
        :param background: 글자의 배경색, None일 경우 변경하지 않음
        :return:
        """
        if foreground is not None:
            self.foreground = foreground
        if background is not None:
            self.background = background

    def set_size(self, size: UISize):
        """
        버튼의 크기를 결정함
        :param size: 변경할 크기, 만약 x 또는 y값이 -1일 경우 그 값은 변경하지 않음.
        :return:
        """
        x, y = self.size
        if size.x != -1:
            x = size.x
        if size.y != -1:
            y = size.y
        self.size = UISize(x, y)

    def set_pos(self, pos: UIPosition):
        """
        버튼의 위치를 결정함
        :param pos: 변경할 위치, 만약 x 또는 y값이 -1일 경우 그 값은 변경하지 않음.
        :return:
        """
        x, y = self.pos
        if pos.x != -1:
            x = pos.x
        if pos.y != -1:
            y = pos.y
        self.pos = UIPosition(x, y)

    def set_label(self, label: str):
        """
        버튼의 레이블을 변경함
        :param label: 변경할 문자열
        :return:
        """
        self.label = label

    def set_font(self, font: FontType):
        """
        버튼의 폰트를 변경함
        :param font:
        :return:
        """
        self.font = font

    def render(self):
        display = pg.display.get_surface()
        pg.draw.rect(display, self.background, (self.pos, self.size))
        text = self.font.render(self.label, True, self.foreground)
        text_size = text.get_size()
        display.blit(text,
                     (self.pos[0] + (self.size[0] / 2) - (text_size[0] / 2),
                      self.pos[1] + (self.size[1] / 2) - (text_size[1] / 2)))

    def is_mouse_in_area(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        return self.pos.x <= mouse_x <= self.pos.x + self.size.x and \
               self.pos.y <= mouse_y <= self.pos.y + self.size.y

    def on_clicked(self):
        raise NotImplementedError
