from dataclasses import dataclass

import pygame as pg

from src.baseclasses.ui.ui import UI, UIPosition, UISize


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
        self.font = pg.font.SysFont('malgungothic', 18, False, False)
        self.position = UIPosition(0, 0)
        self.size = UISize(1280, 50)
        self.game_info = GameInfoData(enemy_unit, player_unit, player_ticket, turn_count)

    def render(self):
        pass
