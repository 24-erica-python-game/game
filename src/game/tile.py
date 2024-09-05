from baseclasses.tile import BaseTile, BaseTileMap
from typing import List


class TileMap(BaseTileMap):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(TileMap, cls).__new__(cls)
            cls.tile_map: List[List[BaseTile]] = []
        
        return cls.instance


class SupplyBase(BaseTile):
    pass