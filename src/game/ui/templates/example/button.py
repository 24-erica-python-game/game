import pygame as pg

from game.ui.base import UIPosition, UISize
from game.ui.color import Color, RGB
from game.ui.templates.button import Button


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
                 foreground: RGB,
                 background: RGB):
        super().__init__(label, label_font, pos, size, foreground, background)

    def on_clicked(self):
        self.set_pos(UIPosition(-1, self.pos.y - 1))
        print("button clicked")


button = ButtonTest("button_label", small_font, UIPosition(100, 143), UISize(200, 14), RGB(0, 0, 0), RGB(199, 199, 199))

while running:
    screen.fill(Color.WHITE)
    clock.tick(30)

    button.render()

    for event in pg.event.get():
        match event.type:
            case pg.QUIT:
                running = False
            case pg.MOUSEBUTTONDOWN if button.is_mouse_in_area():
                button.on_clicked()

    pg.display.flip()
