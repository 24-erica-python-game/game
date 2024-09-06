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
        # TODO: 새 타일 생성 대신 맵에서 인근 타일 가져오는 방식으로 변경
        return [ Tile(self.position.q+v.value.q, self.position.r+v.value.r) for v in HexDirectionVectors ]

    def get_path(self, destination: Position) -> List[Position]:
        # TODO: 테스트 필요
        frontier = PriorityQueue()
        frontier.put((self, 0))

        trail = {}
        far_cost = {}

        trail[self] = None
        far_cost[self] = 0

        while not frontier.empty():
            curr = frontier.get()

            if curr[0].position == destination:
                break

            for nxt in curr[0].get_neighbors():
                new_cost = far_cost[self] + self.get_distance(nxt)
                if nxt not in far_cost or new_cost < far_cost[self]:
                    far_cost[self] = new_cost
                    prior = new_cost + nxt.movement_cost
                    frontier.put(nxt, prior)
                    trail[nxt] = self


class SupplyBase(Tile):
    pass


class TileMap(BaseTileMap):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(TileMap, cls).__new__(cls)
            cls.tile_map: List[List[Tile]] = []
        
        return cls.instance
