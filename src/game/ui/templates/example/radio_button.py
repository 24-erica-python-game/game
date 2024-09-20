import pygame as pg

from game.ui.base import UIPosition, UISize
from game.ui.color import Color, RGB
from game.ui.templates.radio_button import RadioButtonGroup, RadioButton

pg.init()

small_font = pg.font.SysFont("malgungothic", 14, False, False)

# 화면 크기 지정
size = (400, 300)
screen = pg.display.set_mode(size)

pg.display.set_caption("Buggy Buddies")

# FPS 관련 설정
running = True
clock = pg.time.Clock()

radio_group = RadioButtonGroup(small_font, "right", 'radio_button_1', RGB(77, 77, 77), RGB(35, 188, 35), "circle")
radio_button_1 = RadioButton(radio_group, "button1", UIPosition(200, 100), 8.0, 'radio_button_1')
radio_button_2 = RadioButton(radio_group, "button1", UIPosition(200, 120), 8.0, 'radio_button_2')

while running:
    screen.fill(Color.WHITE)
    clock.tick(30)

    radio_group.check_buttons_clicked()
    radio_group.render_buttons()

    for event in pg.event.get():
        match event.type:
            case pg.QUIT:
                running = False

    pg.display.flip()
