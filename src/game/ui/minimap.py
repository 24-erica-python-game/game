import pygame as pg

from src.game.ui.base import BaseUI
from src.utils.config import Config


class Minimap(BaseUI):
    def __init__(self):
        self.font = pg.font.SysFont(Config.get_config("font.default_font"),
                                    Config.get_config("font.default_size"))
        # self.position = UIPosition(50, 700)  # TODO: 미니맵 위치
        # self.size = UISize()  # TODO: 미니맵 크기

    def render(self):
        pass
