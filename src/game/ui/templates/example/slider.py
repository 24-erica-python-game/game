import pygame as pg

from game.ui.base import UIPosition, UISize, UIAlignment
from game.ui.color import Color, RGB
from game.ui.templates.slider import Slider, SliderHead
from game.ui.templates.textbox import TextBox


pg.init()

small_font = pg.font.SysFont("malgungothic", 14, False, False)

# 화면 크기 지정
size = (400, 300)
screen = pg.display.set_mode(size)

pg.display.set_caption("Buggy Buddies")

# FPS 관련 설정
running = True
clock = pg.time.Clock()

drag = False
drag_ = False

head = SliderHead(radius=3)
slider = Slider((0.0, 100.0, 2.5), head, UIPosition(150.0, 150.0), UIPosition(250.0, 150.0), RGB(0, 0, 0))
textbox = TextBox(UIPosition(150, 125), UISize(100, 20), small_font, str(slider.value), RGB(0, 0, 0), UIAlignment.center)

slider.set_value_from_value(50)

while running:
    screen.fill(Color.WHITE)
    clock.tick(30)

    for event in pg.event.get():
        match event.type:
            case pg.QUIT:
                running = False
            case pg.MOUSEBUTTONDOWN:
                drag = True
            case pg.MOUSEBUTTONUP:
                drag = False
                drag_ = False

    # 개선된 조작감을 위해 drag 변수를 2개를 둠. 만약 1개일 경우 조작감이 매우 불편해짐
    if drag and slider.head.is_mouse_in_area():
        drag_ = True
    if drag_ and pg.mouse.get_pressed()[0]:
        slider.on_head_clicked()

    slider.render()
    textbox.label = f"{slider.value:.1f}"
    textbox.render()

    pg.display.flip()
