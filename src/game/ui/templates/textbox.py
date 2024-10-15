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
        pos = self.pos
        text = self.font.render(self.label, True, self.color)
        text_size = UISize(text.get_size()[0], text.get_size()[1])
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

    textbox_aligned_left = TextBox(UIPosition(540, 290),
                                   UISize(200, 20),
                                   small_font,
                                   "left",
                                   RGB(0, 0, 0),
                                   UIAlignment.left)
    textbox_aligned_center = TextBox(UIPosition(540, 265),
                                     UISize(200, 20),
                                     small_font,
                                     "center",
                                     RGB(0, 0, 0),
                                     UIAlignment.center)
    textbox_aligned_right = TextBox(UIPosition(540, 240),
                                    UISize(200, 20),
                                    small_font,
                                    "right",
                                    RGB(0, 0, 0),
                                    UIAlignment.right)

    while running:
        screen.fill(Color.WHITE)
        clock.tick(30)

        textbox_aligned_left.render()
        textbox_aligned_center.render()
        textbox_aligned_right.render()

        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    running = False

        pg.display.flip()
