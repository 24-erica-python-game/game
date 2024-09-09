import pygame as pg

from src.baseclasses.ui.ui import UI
from src.utils.config import Config


class TopBar(UI):
    def __init__(self):
        self.font = pg.font.SysFont(Config.get_config("font.default_font"),
                                    Config.get_config("font.default_size"))
        # self.position = UIPosition()  # TODO: 상단 바 위치
        # self.size = UISize()  # TODO: 상단 바 크기

    def render(self):
        pass
