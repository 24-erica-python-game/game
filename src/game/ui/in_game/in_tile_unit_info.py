from typing import Literal

import pygame as pg

from src.game.ui.base import BaseUI, FloatUIPosition
from src.game.tile.types import ActualPosition, get_hex_vertex_position, HexDirections
from src.game.ui.color import Color


class InTileUnitInfo(BaseUI):
    def __init__(self,
                 center_position: FloatUIPosition,
                 radius: float,
                 bar_padding: FloatUIPosition,
                 bar_fill_margin: FloatUIPosition, ):
        """
        :param center_position: 타일의 중점의 위치
        :param radius: 타일의 한 모서리의 크기
        :param bar_padding: 바를 그릴 때 타일의 모서리에서 얼마나 띄울지의 값
        :param bar_fill_margin: 바를 채울 때 빈 바를 보이게 할 지의 값
        """
        self.center_position = center_position
        self._size = radius
        self.bar_padding = bar_padding
        self.bar_fill_margin = bar_fill_margin

    def render_bar(self,
                   value: int,
                   value_max: int,
                   color_empty: Color,
                   color_filler: Color,
                   direction: Literal[HexDirections.WEST, HexDirections.EAST],):
        """
        체력바, 보급바와 같이 타일의 왼쪽 또는 오른쪽에 배치할 수 있는 바를 렌더링함.
        :param value: 현재 체력과 같은 변수
        :param value_max: value의 최댓값
        :param color_empty: 빈 바의 색
        :param color_filler: 바가 채워질 때의 채워진 부분의 색
        :param direction: 바가 있는 방향, HexDirections.WEST 또는 HexDirections.EAST만 될 수 있음
        :return:
        """
        # TODO: 테스트 필요

        multiplier = 1 if direction == HexDirections.WEST else -1

        pos = get_hex_vertex_position(ActualPosition(self.center_position.x,
                                                     self.center_position.y, ),
                                      self._size,
                                      direction, )
        bar_width = 20
        empty_bar_rect = [pos.x + (multiplier * self.bar_padding.x),                        # (좌측 바 기준) 좌측 상단 x
                          pos.y + self._size + self.bar_padding.y,                          # (좌측 바 기준) 좌측 상단 y
                          pos.x + (multiplier * (self.bar_padding.x + bar_width)),          # (좌측 바 기준) 우측 하단 x
                          pos.y - self.bar_padding.y,]                                      # (좌측 바 기준) 우측 하단 y

        filler_rect = [pos.x + (multiplier * self.bar_padding.x) + self.bar_fill_margin.x,  # (좌측 바 기준) 좌측 하단 x
                       pos.y - self.bar_fill_margin.y,                                      # (좌측 바 기준) 좌측 하단 y
                       pos.x + (multiplier * (self.bar_padding.x + bar_width)),             # (좌측 바 기준) 우측 상단 x
                       pos.y - self.bar_padding.y + (value / value_max) * self._size,]      # (좌측 바 기준) 우측 상단 y, value 값에 따라 이 값도 바뀜

        screen = pg.display.get_surface()

        pg.draw.rect(screen, color_empty, empty_bar_rect)
        pg.draw.rect(screen, color_filler, filler_rect)

    def render_building(self):
        pass

    def render_cost(self):
        pass
