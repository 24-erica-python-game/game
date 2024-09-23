import pygame as pg
from pygame.rect import RectType, Rect

from src.game.tile.base import BaseTileMap
from src.game.tile.types import HexDirections, get_hex_vertex_position, ActualPosition
from src.game.ui.base import BaseUI, FloatUISize
from src.game.ui.color import Color
from src.utils.config import Config


class Minimap(BaseUI):
    def __init__(self, tilemap: BaseTileMap):
        self.font = pg.font.SysFont(Config.get_config("font.default_font"),
                                    Config.get_config("font.default_size"))
        self.map_size = tilemap.size

    def __get_regularized_coordinates(self):
        """
        정규화된 타일 좌표를 반환함
        :return: 타일 좌표, 정규화 되었기 때문에 타일 좌표의 범위는 0이상 1이하임
        """
        w, h = self.map_size
        coordinates = [[(x / w, y / h) for x in range(1, self.map_size[0] + 1)]
                                       for y in range(1, self.map_size[1] + 1)]
        return coordinates

    def __draw_hexagon(self,
                       surface: pg.SurfaceType,
                       color: Color | tuple[int, int, int],
                       center_pos: tuple[float, float],
                       radius: float) -> Rect | RectType:
        _center_pos = ActualPosition(center_pos[0], center_pos[1])
        points = [get_hex_vertex_position(_center_pos, radius, direction) for direction in HexDirections]
        hexagon = pg.draw.polygon(surface, color, points)
        return hexagon

    def render(self, map_data: list):
        # TODO: 테스트 필요함
        w, h = pg.display.get_window_size()
        minimap_size = FloatUISize(int(w * (1 / 4)), int(h * (1 / 4)))
        minimap = pg.Surface((minimap_size.x, minimap_size.y))
        for l_coordinates in self.__get_regularized_coordinates():
            for coordinates in l_coordinates:
                self.__draw_hexagon(minimap,
                                    (83, 153, 83),
                                    coordinates,
                                    min(int(w * (1/4))/w, int(h * (1/4))/h))  # 연두색 육각형을 그림
        minimap.blit(pg.display.get_surface(), (w, h - minimap_size.y))
