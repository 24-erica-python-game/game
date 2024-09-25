import pygame as pg

from game.ui.base import UIPosition, UIAlignment, UISize
from game.ui.color import Color, RGB
from game.ui.templates.textbox import TextBox

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
