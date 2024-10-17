import pygame as pg

from src.game.ui.base import BaseUI
from src.utils.config import Config


class TileInfo(BaseUI):
    def __init__(self):
        self.font = pg.font.SysFont(Config.get_config("font.default.font"),
                                    Config.get_config("font.default.size"))
        # self.position = UIPosition()  # TODO: 타일 정보 위치
        # self.size = UISize()  # TODO: 타일 정보 크기

    def render(self):
        pass
