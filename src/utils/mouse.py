from typing import NamedTuple

import pygame as pg
from pygame.rect import RectType


# double_click()
__dbclk_first_clicked = False
__timer = 0
__timerset = False
event_double_clicked = pg.USEREVENT + 1
double_click_time = 500


# drag()
__drag_clicked = False
__drag_drag = False


class DragResult(NamedTuple):
    drag_clicked: bool
    drag: bool


def double_click():
    # TODO: 테스트 필요
    global __dbclk_first_clicked, event_double_clicked, __timer, __timerset
    for event in pg.event.get():
        match event.type:
            case pg.MOUSEBUTTONDOWN:
                if __timer == 0:
                    pg.time.set_timer(event_double_clicked, 500)
                    __timerset = True
                else:
                    if __timer == 1:
                        pg.time.set_timer(event_double_clicked, 0)
                        double_click()
                        __timerset = False

                if __timerset:
                    __timer = 1
                    return
                else:
                    __timer = 0
                    return

def drag(detection_area: RectType) -> DragResult:
    # TODO: 테스트 필요
    global __drag_clicked, __drag_drag
    for event in pg.event.get():
        match event.type:
            case pg.MOUSEBUTTONDOWN:
                __drag_clicked = True
            case pg.MOUSEBUTTONUP:
                __drag_clicked = False
                __drag_drag = False

    mouse_pos = pg.mouse.get_pos()
    if detection_area.collidepoint(mouse_pos):
        __drag_drag = True

    return DragResult(__drag_clicked, __drag_drag)
