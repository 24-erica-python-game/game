from src.game.unit.base import BaseUnit
from src.game.tile.base import Position


class Ant(BaseUnit): # 개미
    def __init__(self, position: Position):
        super().__init__()


class StagBeetle(BaseUnit): # 사슴벌레
    def __init__(self, position: Position):
        super().__init__()


class BombardierBeetle(BaseUnit): # 폭탄먼지벌레
    def __init__(self, position: Position):
        super().__init__()


class Aphid(BaseUnit): # 진딧물
    def __init__(self, position: Position):
        super().__init__()

    def build_supply_base(self):
        pass
