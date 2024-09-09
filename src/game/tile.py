from baseclasses.interface import *
from baseclasses.tile import *

from queue import PriorityQueue
from typing import List
import json


class CommonTile(BaseTile):       pass
class SupplyBaseTile(CommonTile): pass
class HQTile(CommonTile):         pass
class HillTile(CommonTile):       pass
class FieldTile(CommonTile):      pass
class MountainTile(CommonTile):   pass


class TileMap(BaseTileMap):
    @staticmethod
    def __parse_map(raw_map_data: list[str]) -> BaseTileMap:
        tile_definition: dict[str, dict[str, str]] = raw_map_data["tile_definition"]
        translate_table = {}
        parsed_tile_map: list = []

        for tile_type in tile_definition.keys():
            tile_type[0] = tile_type[0].capitalize()
            tile_type_class_name = f""
            translate_table.update({ tile_definition[tile_type]["symbol"]: getattr() })
    
    def __new__(cls, map_name: str):
        if not hasattr(cls, "instance"):
            with open(f"assets/maps/{map_name}.json") as file_stream:
                raw_map_data: dict = json.loads(file_stream.read())
                map_data: List[List[str]] = raw_map_data["map_data"]
                
                cls.instance = super(TileMap, cls).__new__(cls, min(map(len, map_data)))
                cls.tile_map: List[BaseTileMap] = cls.__parse_map(raw_map_data)

        return cls.instance


class CommonTile(BaseTile):
    def __init__(self, q: int, r: int) -> None:
        super().__init__(q, r)

    def __repr__(self) -> str:
        return f"Tile({self.position.q}, {self.position.r})"

    def on_arrived(self) -> None:
        pass

    def get_neighbors(self, tile_map: TileMap) -> List[AxialCoordinates]:
        super().get_neighbors()
        # TODO: 새 타일 생성 대신 맵에서 인근 타일 가져오는 방식으로 변경
        return [ tile_map[self.position.q+v.value.q][self.position.r+v.value.r] for v in HexDirectionVectors ]

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


class SupplyBase(CommonTile):
    pass


class HQTile(CommonTile):
    pass


class HillTile(CommonTile):
    pass


class FieldTile(CommonTile):
    pass


class MountainTile(CommonTile):
    pass
