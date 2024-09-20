import pygame as pg

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
