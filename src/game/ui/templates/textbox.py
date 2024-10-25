from typing import Literal

import pygame as pg
from pygame.font import FontType

from game.ui.base import UIPosition, UIAlignment, UISize
from game.ui.color import RGB
from game.ui.templates.interactable import Interactable


class TextBox(Interactable):
    def __init__(self,
                 pos: UIPosition,
                 size: UISize,
                 font: FontType,
                 label: str):
        """
        텍스트박스 템플릿, 주어진 크기 안에서 텍스트를 정렬함.
        :param pos: 텍스트박스의 위치
        :param size: 텍스트박스의 크기
        :param font: 텍스트의 폰트
        :param label: 텍스트의 내용
        """
        self.pos = pos
        self.size = size
        self.font = font
        self.label = label
        self.color = RGB(0, 0, 0)
        self.alignment = UIAlignment.center
        super().__init__(pos, max([font.render(label, True, self.color).get_size(), size]))

    def set_alignment(self, alignment: Literal[UIAlignment.left, UIAlignment.center, UIAlignment.right]):
        """
        텍스트 정렬 방향을 설정함.
        :param alignment: 텍스트 정렬 방향
        :return:
        """
        self.alignment = alignment

    def set_text_color(self, color: RGB):
        """
        텍스트의 색상을 설정함.
        :param color: 텍스트의 색상
        :return:
        """
        self.color = color

    def render(self):
        display = pg.display.get_surface()
        pos = self.pos
        text = self.font.render(self.label, True, self.color)
        text_size = UISize(text.get_size()[0], text.get_size()[1])
        label_pos_x = 0

        match self.alignment:
            case UIAlignment.left:
                label_pos_x = pos.x
            case UIAlignment.center:
                label_pos_x = pos.x + (self.size[0] - text_size.x) / 2
            case UIAlignment.right:
                label_pos_x = pos.x + (self.size[0] - text_size.x)

        display.blit(text, (label_pos_x, pos.y))


if __name__ == "__main__":
    from game.ui.color import Color

    pg.init()

    small_font = pg.font.SysFont("malgungothic", 14, False, False)

    # 화면 크기 지정
    size = (1280, 600)
    screen = pg.display.set_mode(size)

    pg.display.set_caption("Buggy Buddies")

    # FPS 관련 설정
    running = True
    clock = pg.time.Clock()

    textbox_1 = TextBox(UIPosition(540, 290), UISize(200, 20), small_font, "left")
    textbox_1.set_alignment(UIAlignment.left)

    textbox_2 = TextBox(UIPosition(540, 265), UISize(200, 20), small_font, "center")
    textbox_2.set_alignment(UIAlignment.center)

    textbox_3 = TextBox(UIPosition(540, 240), UISize(200, 20), small_font, "right")
    textbox_3.set_alignment(UIAlignment.right)

    while running:
        screen.fill(Color.WHITE)
        clock.tick(30)

        textbox_1.render()
        textbox_2.render()
        textbox_3.render()

        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    running = False

        pg.display.flip()
