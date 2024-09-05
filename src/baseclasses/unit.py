from abc import ABCMeta, abstractmethod
from os import PathLike
from baseclasses.interface import *
from dataclasses import dataclass


class BaseUnit(ABCMeta):
    @property
    def anim_state(self) -> AnimationState:
        return self.anim_state

    @property
    def action_cost(self) -> int:
        return self.action_cost

    @property
    def position(self) -> Position:
        return self.position

    @property
    def supply_reserve(self) -> int:
        return self.supply_reserve
    

    @abstractmethod
    def _play_animation(self, anim_path: PathLike):
        pass

    def move(self, destination: Position) -> bool:
        # TODO: 이동 로직 구현
        pass

    def find_path(self, destination: Position) -> list:
        """
        A* 알고리즘으로 구현
        """
        rotation_vecs = [(+1, 0, -1), (0, +1, -1), (-1, +1, 0), 
                         (-1, 0, +1), (0, -1, +1), (+1, -1, 0)]
        open_list = [ self ]
        close_list = []

        for vq, vr, vs in rotation_vecs:
            open_list.append(TileMap[q+vq][r+vr][s+vs])

        # F = G+H
        # G: move_cost
        # H: get_distance


class BaseSupplyUnit(BaseUnit):
    def __init__(self, position: Position):
        pass

    def supply(self, target_unit: BaseUnit):
        target_unit.supply_reserve += 100
        