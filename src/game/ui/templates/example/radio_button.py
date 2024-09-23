import pygame as pg

from game.ui.base import FloatUIPosition, UIAlignment
from game.ui.color import Color, RGB
from game.ui.templates.radio_button import RadioButtonGroup, RadioButton

pg.init()

small_font = pg.font.SysFont("malgungothic", 14, False, False)

# 화면 크기 지정
size = (1280, 600)
screen = pg.display.set_mode(size)

pg.display.set_caption("Buggy Buddies")

# FPS 관련 설정
running = True
clock = pg.time.Clock()

radio_group = RadioButtonGroup(font=small_font,
                               label_pos=UIAlignment.right,
                               label_alignment=UIAlignment.center,
                               label_color=RGB(0,0,0),
                               label_distance=20,
                               default_active_id='radio_button_1',
                               button_color=RGB(77, 77, 77),
                               active_color=RGB(35, 188, 35))
radio_button_1 = RadioButton(radio_group, "테스트", FloatUIPosition(500, 100), 6.5, 'radio_button_1')
radio_button_2 = RadioButton(radio_group, "label_pos와 label_alignment 값을 변경해", FloatUIPosition(500, 120), 6.5, 'radio_button_2')
radio_button_3 = RadioButton(radio_group, "레이블 위치를 변경 가능하다", FloatUIPosition(500, 140), 6.5, 'radio_button_3')


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
