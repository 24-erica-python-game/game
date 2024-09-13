from tile.structure import *
from tile.types import *
from tile.base import *

from queue import PriorityQueue
import json


class CommonTile(BaseTile):       pass
class HillTile(CommonTile):       pass
class FieldTile(CommonTile):      pass
class MountainTile(CommonTile):   pass


class TileMap(BaseTileMap):
    @staticmethod
    def __parse_map(raw_map_data: list[str]) -> BaseTileMap:
        metadata = raw_map_data["metadata"]
        map_data = raw_map_data["map_data"]

        parsed_map: list[list[BaseTile]] = [ 
            [ CommonTile(i, j) for j in range(metadata["map_size"]) ] \
                for i in range(metadata["map_size"]) ]

        for tile_mod in map_data:
            if tile_mod["position"] >= metadata["map_size"]:
                continue

            x: int = tile_mod["position"][0]
            y: int = tile_mod["position"][1]

            tile = parsed_map[y][x]

            match (tile_mod["tile"]):
                case "hill":
                    parsed_map[y][x] = HillTile(x, y)
                    tile = parsed_map[y][x]
                case "mountain":
                    parsed_map[y][x] = MountainTile(x, y)
                    tile = parsed_map[y][x]

            match (tile_mod["structure"]):
                case "supply_base":
                    tile.construct_structure(SupplyBaseStructure) # TODO: 건설 구현
                case "HQ":
                    tile.construct_structure(HQStructure)

            match (tile_mod["unit"]):
                case "ant":
                    tile.place_unit()
                case "stag_beetle":
                    tile.place_unit()
                case "bombardier_beetle":
                    tile.place_unit()
                case "ahpid":
                    tile.place_unit()

    
    def __new__(cls, map_name: str):
        if not hasattr(cls, "instance"):
            with open(f"assets/maps/{map_name}.json") as file_stream:
                raw_map_data: dict = json.loads(file_stream.read())
                metadata: dict = raw_map_data["metadata"]

                cls.instance = super(TileMap, cls).__new__(cls, metadata["map_size"])
                cls.tile_map: list[BaseTileMap] = cls.__parse_map(raw_map_data)

        return cls.instance


class CommonTile(BaseTile):
    def __init__(self, q: int, r: int) -> None:
        super().__init__(q, r)

    def __repr__(self) -> str:
        return f"Tile({self.position.q}, {self.position.r})"

    def on_arrived(self) -> None:
        pass

    def get_neighbors(self, tile_map: TileMap) -> list[AxialCoordinates]:
        super().get_neighbors()
        # TODO: 새 타일 생성 대신 맵에서 인근 타일 가져오는 방식으로 변경
        return [ tile_map[self.position.q+v.value.q][self.position.r+v.value.r] \
                for v in HexDirectionVectors ]

    def get_path(self, destination: Position) -> list[Position]:
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


class HillTile(CommonTile):
    pass


class FieldTile(CommonTile):
    pass


class MountainTile(CommonTile):
    pass
