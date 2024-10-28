from typing import Optional

import pygame as pg
from pygame.font import FontType

from game.ui.base import UIPosition, UISize
from game.ui.color import RGB
from game.ui.templates.interactable import Interactable


class Button(Interactable):
    """
    버튼 템플릿.

    이 클래스를 상속받은 후 on_clicked 메서드를 오버라이드해 버튼 클릭시 동작을 정의해 사용함.
    """
    def __init__(self,
                 label: str,
                 label_font: pg.font.FontType,
                 pos: UIPosition,
                 size: UISize,
                 *,
                 foreground: RGB,
                 background: RGB):
        """
        :param label: 버튼의 레이블
        :param label_font: 레이블의 폰트
        :param pos: 버튼의 위치
        :param size: 버튼의 크기
        :param foreground: (keyword-only) 레이블의 색
        :param background: (keyword-only) 버튼의 배경색
        """
        super().__init__(pos, size)
        self.label = label
        self.font = label_font
        self.pos = pos
        self.size = size
        self.foreground = foreground
        self.background = background

    def set_color(self, foreground: Optional[RGB] = None, background: Optional[RGB] = None):
        """
        버튼의 색상을 설정함.
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
        버튼의 크기를 결정함.
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
        버튼의 위치를 결정함.
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
        버튼의 레이블을 변경함.
        :param label: 변경할 문자열
        :return:
        """
        self.label = label

    def set_font(self, font: FontType):
        """
        버튼의 폰트를 변경함.
        :param font:
        :return:
        """
        self.font = font

    def update(self):
        display = pg.display.get_surface()
        pg.draw.rect(display, self.background, (self.pos, self.size))
        text = self.font.render(self.label, True, self.foreground)
        text_size = text.get_size()
        display.blit(text,
                     (self.pos[0] + (self.size[0] / 2) - (text_size[0] / 2),
                      self.pos[1] + (self.size[1] / 2) - (text_size[1] / 2)))

    def on_click(self):
        """
        버튼이 클릭되었을 때 호출되는 함수, 상속받은 버튼 클래스는 이 메서드를 오버라이딩해 버튼 클릭 시의 동작을 정의해야 함.
        :return:
        """
        raise NotImplementedError


if __name__ == "__main__":
    from game.ui.color import Color

    pg.init()

    small_font = pg.font.SysFont("malgungothic", 14, False, False)

    # 화면 크기 지정
    size = (400, 300)
    screen = pg.display.set_mode(size)

    pg.display.set_caption("Buggy Buddies")

    # FPS 관련 설정
    running = True
    clock = pg.time.Clock()


    class ButtonTest(Button):
        def __init__(self,
                     label: str,
                     label_font: pg.font.FontType,
                     pos: UIPosition,
                     size: UISize,
                     *,
                     foreground: RGB,
                     background: RGB):
            super().__init__(label, label_font, pos, size, foreground=foreground, background=background)

        def on_clicked(self):
            self.set_pos(UIPosition(-1, self.pos.y - 1))
            self.set_label(f"pos: ({self.pos.x}, {self.pos.y})")
            print("button clicked")


    button = ButtonTest("button_label", small_font, UIPosition(100, 143), UISize(200, 14),
                        foreground=RGB(0, 0, 0), background=RGB(199, 199, 199))

    while running:
        screen.fill(Color.WHITE)
        clock.tick(30)

        button.update()

        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    running = False
                case pg.MOUSEBUTTONDOWN if button.is_mouse_in_area():
                    button.on_clicked()

        pg.display.flip()
