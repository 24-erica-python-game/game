import pygame as pg

from game.ui.base import UIPosition, UISize


class Interactable:
    """
    마우스가 영역 안에 있는지를 검사할 수 있는 함수를 제공하는 클래스
    """
    def __init__(self, pos: UIPosition, size: UISize):
        self.pos = pos
        self.size = size

    def is_mouse_in_area(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        return self.pos.x <= mouse_x <= self.pos.x + self.size.x and \
            self.pos.y <= mouse_y <= self.pos.y + self.size.y
