import pygame as pg

from src.game.ui.base import BaseUI, UIPosition
from src.game.tile.types import ActualPosition, get_tile_point_position, HexDirections
from src.game.ui.color import Color


class InTileUnitInfo(BaseUI):
    def __init__(self, center_position: UIPosition, size: float):
        self.center_position = center_position
        self._size = size
        self.bar_margin = UIPosition(5, 0)

    def render_health_bar(self, health: int):
        pos = get_tile_point_position(
            ActualPosition(self.center_position.x,
                           self.center_position.y),
            self._size,
            HexDirections.WEST
        )
        rect = []
        screen = pg.display.get_surface()

        pg.draw.rect(screen, Color.WHITE, rect)  # 빈 체력바


    def render_supply_bar(self):
        pass

    def render_building_icon(self):
        pass

    def render_cost(self):
        pass
