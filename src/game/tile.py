from baseclass.tile import TileMeta
from typing import List


class TileMap:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(TileMap, cls).__new__(cls)
            cls.tile_map: List[List[TileMeta]] = []
        
        return cls.instance


class SupplyBase(TileMeta):
    pass