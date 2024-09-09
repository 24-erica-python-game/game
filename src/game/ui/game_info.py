from dataclasses import dataclass

import pygame as pg

from src.baseclasses.ui.ui import UI, UIPosition, UISize
from src.utils.config import Config


@dataclass
class GameInfoData:
    enemy_unit: int
    player_unit: int
    player_ticket: int
    turn_count: int


class GameInfo(UI):
    def __init__(self,
                 enemy_unit: int,
                 player_unit: int,
                 player_ticket: int,
                 turn_count: int):
        self.font = pg.font.SysFont(Config.get_config("font.default_font"),
                                    Config.get_config("font.default_size"))
        self.position = UIPosition(640, 10)
        self.size = UISize(1280, 50)
        self.game_info = GameInfoData(enemy_unit, player_unit, player_ticket, turn_count)

    def render(self):
        pass
