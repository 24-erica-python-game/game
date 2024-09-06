from baseclasses.interface import *
from baseclasses.tile import *

from queue import PriorityQueue
from typing import List


class Tile(BaseTile):
    def __init__(self, q: int, r: int) -> None:
        super().__init__(q, r)

    def __repr__(self) -> str:
        return f"Tile({self.position.q}, {self.position.r})"

    def on_arrived(self) -> None:
        pass

    def get_neighbors(self) -> List[AxialCoordinates]:
        super().get_neighbors()
        return [ Tile(self.position.q+v.value.q, self.position.r+v.value.r) for v in HexDirectionVectors ]

    def get_path(self, destination: Position) -> List[Position]:
        frontier = PriorityQueue()
        frontier.put((self, 0))
        
        trail = {}
        far_costs = {}

        trail[self] = None
        far_costs[self] = 0

        while not frontier.empty():
            curr = frontier.get()

            if curr[0].position == destination:
                break

            for nxt in curr[0].get_neighbors():
                pass


class SupplyBase(Tile):
    pass


class TileMap(BaseTileMap):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(TileMap, cls).__new__(cls)
            cls.tile_map: List[List[BaseTile]] = []
        
        return cls.instance
