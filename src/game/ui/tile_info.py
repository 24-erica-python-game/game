import pygame as pg

from src.game.ui.base import UI
from src.utils.config import Config


class TileInfo(UI):
    def __init__(self):
        self.font = pg.font.SysFont(Config.get_config("font.default_font"),
                                    Config.get_config("font.default_size"))
        # self.position = UIPosition()  # TODO: 타일 정보 위치
        # self.size = UISize()  # TODO: 타일 정보 크기

    def render(self):
        pass
