import pygame as pg

from game.ui.base import UIPosition, UISize
from game.ui.color import Color, RGB
from game.ui.templates.checkbox import CheckBox


pg.init()

small_font = pg.font.SysFont("malgungothic", 14, False, False)

# 화면 크기 지정
size = (400, 300)
screen = pg.display.set_mode(size)

pg.display.set_caption("Buggy Buddies")

# FPS 관련 설정
running = True
clock = pg.time.Clock()

checkbox = CheckBox(True, RGB(25, 25, 25), "cross", UIPosition(195, 145), UISize(10, 10))

while running:
    screen.fill(Color.WHITE)
    clock.tick(30)

    for event in pg.event.get():
        match event.type:
            case pg.QUIT:
                running = False
            case pg.MOUSEBUTTONDOWN if checkbox.is_mouse_in_area():
                checkbox.state = not checkbox.state

    checkbox.render()

    pg.display.flip()
