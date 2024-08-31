from baseclass.base_unit import UnitMeta
from baseclass.base_tile import Position


class Ant(UnitMeta): # 개미
    def __init__(self, position: Position):
        super().__init__()


class StagBeetle(UnitMeta): # 사슴벌레
    def __init__(self, position: Position):
        super().__init__()


class BombardierBeetle(UnitMeta): # 폭탄먼지벌레
    def __init__(self, position: Position):
        super().__init__()


class Aphid(UnitMeta): # 진딧물
    def __init__(self, position: Position):
        super().__init__()

    def build_supply_base(self):
        pass