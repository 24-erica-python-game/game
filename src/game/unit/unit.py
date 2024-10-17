import os
from os import PathLike

from game.unit.base import BaseUnit, AnimationState
from game.tile.types import Position


# class TestUnit(BaseUnit):
#     def __init__(self,
#                  x: int,
#                  y: int,
#                  faction: int,
#                  action_cost: int,
#                  cost: int,
#                  hp: int = 100,
#                  supply_reserve: int = 100):
#         self.position = Position(x, y)
#         self.faction = faction
#         self.action_cost = action_cost
#         self.cost = cost
#         self.hp = hp
#         self.supply_reserve = supply_reserve
#
#         self.animations = []
#         self.load_animations()


class Ant(BaseUnit): # 개미
    def _play_animation(self, anim_path: PathLike):
        pass

    def __init__(self, x: int, y: int, faction: int, action_cost: int, cost: int, hp: int = 100, supply_reserve: int = 100):
        super().__init__(x, y, faction, action_cost, cost, hp, supply_reserve)


class StagBeetle(BaseUnit): # 사슴벌레
    def _play_animation(self, anim_path: PathLike):
        pass

    def __init__(self, x: int, y: int, faction: int, action_cost: int, cost: int, hp: int = 100, supply_reserve: int = 100):
        super().__init__(x, y, faction, action_cost, cost, hp, supply_reserve)


class BombardierBeetle(BaseUnit): # 폭탄먼지벌레
    def _play_animation(self, anim_path: PathLike):
        pass

    def __init__(self, x: int, y: int, faction: int, action_cost: int, cost: int, hp: int = 100, supply_reserve: int = 100):
        super().__init__(x, y, faction, action_cost, cost, hp, supply_reserve)


class Aphid(BaseUnit): # 진딧물
    def _play_animation(self, anim_path: PathLike):
        pass

    def __init__(self, x: int, y: int, faction: int, action_cost: int, cost: int, hp: int = 100, supply_reserve: int = 100):
        super().__init__(x, y, faction, action_cost, cost, hp, supply_reserve)

    def build_supply_base(self):
        pass
